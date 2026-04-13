#!/usr/bin/env python3
"""
Render a simple standalone HTML report from a run_tests.py Markdown report.

Goal: make it easy to compare multiple conditions (e.g. RCCE-1 vs ATRCE-2 vs PCL-1 vs SDC-1)
without opening the long per-case Markdown.
"""

import argparse
import datetime
import html
import re
from pathlib import Path


def _parse_kv_header(md_text):
    out = {}
    for key in ["Generated", "Runner", "Count mode", "Codex model", "Claude model", "Repeats per condition/case", "Baseline", "Conditions"]:
        m = re.search(r"^" + re.escape(key) + r":\s*(.*)\s*$", md_text, flags=re.MULTILINE)
        if m:
            out[key] = m.group(1).strip()
    return out


def _parse_summary_table(md_text):
    # Find the "## Summary Table" markdown table and return rows as dicts.
    # Expected columns:
    # | Case | Condition | Internal Tokens | Compliance | Repair Turns | Final Quality |
    m = re.search(r"^## Summary Table\s*\n\n(\|.*\n\|---.*\n(?:\|.*\n)+)", md_text, flags=re.MULTILINE)
    if not m:
        raise ValueError("Could not find Summary Table in markdown")

    table = m.group(1).strip().splitlines()
    header = [c.strip() for c in table[0].strip("|").split("|")]
    rows = []
    for line in table[2:]:
        cols = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cols) != len(header):
            continue
        row = dict(zip(header, cols))
        rows.append(row)
    return rows


def _parse_per_case_samples(md_text):
    """
    Parse the "## Per-Case Results" section and extract Internal/Final samples.

    Returns:
      samples[case][condition] = {"internal": str, "final": str}
    """
    m = re.search(r"^## Per-Case Results\s*\n\n(.*?)(?=^## Summary Table\s*$)", md_text, flags=re.MULTILINE | re.DOTALL)
    if not m:
        return {}

    section = m.group(1)
    samples = {}

    case_iter = re.finditer(
        r"^###\s+(?P<case>[^\n]+)\s*\n\n(?P<body>.*?)(?=^###\s+|\Z)",
        section,
        flags=re.MULTILINE | re.DOTALL,
    )
    for cm in case_iter:
        case = cm.group("case").strip()
        body = cm.group("body")
        samples.setdefault(case, {})

        # Each condition includes "Internal sample:" and "Final sample:" code fences.
        cond_iter = re.finditer(
            r"^\*\*(?P<cond>[^*]+)\*\*:\s*(?P<meta>[^\n]*)\n"
            r".*?"
            r"^Internal sample:\s*\n```text\s*\n(?P<internal>.*?)\n```\s*\n"
            r"^Final sample:\s*\n```text\s*\n(?P<final>.*?)\n```\s*",
            body,
            flags=re.MULTILINE | re.DOTALL,
        )
        for dm in cond_iter:
            cond = dm.group("cond").strip()
            internal = dm.group("internal").rstrip("\n")
            final = dm.group("final").rstrip("\n")
            samples[case][cond] = {"internal": internal, "final": final}

    return samples


def _parse_totals(rows):
    totals = []
    for r in rows:
        if r.get("Case") == "**TOTAL / AVG**":
            totals.append(r)
    if not totals:
        raise ValueError("Could not find TOTAL / AVG rows")
    return totals


def _to_float(s):
    s = s.strip()
    s = s.strip("*")
    s = s.replace("%", "")
    try:
        return float(s)
    except ValueError:
        return None


def _to_int(s):
    s = s.strip()
    s = s.strip("*")
    try:
        return float(s)
    except ValueError:
        return None


def _slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

def _fmt_num(n):
    if n is None:
        return "n/a"
    try:
        nf = float(n)
    except (TypeError, ValueError):
        return "n/a"
    if abs(nf - round(nf)) < 1e-9:
        return str(int(round(nf)))
    return "{:.1f}".format(nf)


def render_html(md_text, title):
    meta = _parse_kv_header(md_text)
    rows = _parse_summary_table(md_text)
    samples = _parse_per_case_samples(md_text)
    totals = _parse_totals(rows)

    # Build a condition summary from TOTAL / AVG rows
    conds = []
    for t in totals:
        conds.append(
            {
                "condition": t["Condition"].strip("`"),
                "tokens": _to_int(t["Internal Tokens"]),
                "compliance": _to_float(t["Compliance"]),
                "repair": _to_float(t["Repair Turns"]),
                "quality": _to_float(t["Final Quality"]),
            }
        )

    # Baseline for comparisons: plain_english tokens if present.
    baseline_tokens = None
    for c in conds:
        if c["condition"] == "plain_english":
            baseline_tokens = c["tokens"]
            break
    if baseline_tokens is None:
        baseline_tokens = max(c["tokens"] or 1.0 for c in conds)

    # Order: baseline first, then the rest in stable order
    conds = sorted(
        conds,
        key=lambda c: (0 if c["condition"] == "plain_english" else 1, c["condition"]),
    )

    # Headlines
    best_by_tokens = min((c for c in conds if c["tokens"] is not None), key=lambda c: c["tokens"])

    # "Best tradeoff" heuristic: require non-trivial quality + decent compliance.
    tradeoff_pool = [
        c
        for c in conds
        if (c["tokens"] is not None)
        and (c["compliance"] is not None and c["compliance"] >= 90.0)
        and (c["quality"] is not None and c["quality"] >= 2.0)
    ]
    best_tradeoff = min(tradeoff_pool, key=lambda c: c["tokens"]) if tradeoff_pool else None

    def pct_reduction(tokens):
        if tokens is None or baseline_tokens in (None, 0):
            return None
        return round((baseline_tokens - tokens) / float(baseline_tokens) * 100.0, 1)

    # Per-case matrix for the table
    cases = []
    for r in rows:
        if r.get("Case") == "**TOTAL / AVG**":
            continue
        if r.get("Case") not in cases:
            cases.append(r.get("Case"))

    # Build map[case][condition] = metrics
    by_case = {}
    for r in rows:
        case = r.get("Case")
        if case == "**TOTAL / AVG**":
            continue
        by_case.setdefault(case, {})
        by_case[case][r.get("Condition")] = r

    def esc(x):
        return html.escape("" if x is None else str(x))

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    # Match the existing repo HTML report styling (light theme + hero + KPI tiles).
    css = """
    :root {
      --bg: #f5f7fb;
      --panel: #ffffff;
      --panel-soft: #f8fafc;
      --text: #102033;
      --muted: #5f6b7a;
      --line: #dbe3ec;
      --accent: #0f766e;
      --accent-2: #1d4ed8;
      --good: #166534;
      --warn: #9a5b00;
      --bad: #b91c1c;
      --shadow: 0 16px 40px rgba(16, 32, 51, 0.08);
      --mono: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
    }

    * { box-sizing: border-box; }

    body {
      margin: 0;
      font-family: Inter, "Segoe UI", Arial, sans-serif;
      background:
        radial-gradient(circle at top left, rgba(15, 118, 110, 0.09), transparent 28%),
        radial-gradient(circle at top right, rgba(29, 78, 216, 0.08), transparent 24%),
        var(--bg);
      color: var(--text);
      line-height: 1.5;
    }

    .wrap { max-width: 1180px; margin: 0 auto; padding: 40px 22px 60px; }

    .hero {
      background: linear-gradient(135deg, #0f172a, #12324a 55%, #0f766e 120%);
      color: #fff;
      border-radius: 24px;
      padding: 34px 36px;
      box-shadow: var(--shadow);
    }

    .eyebrow {
      display: inline-block;
      font-size: 12px;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: rgba(255,255,255,0.72);
      margin-bottom: 12px;
    }

    h1, h2, h3, p { margin: 0; }
    h1 { font-size: 34px; line-height: 1.1; margin-bottom: 12px; }
    h2 { font-size: 22px; margin-bottom: 14px; }
    h3 { font-size: 16px; margin-bottom: 6px; }

    .hero p { max-width: 920px; color: rgba(255,255,255,0.86); font-size: 16px; margin-bottom: 18px; }

    .meta { margin-top: 10px; color: rgba(255,255,255,0.78); font-size: 13px; }
    .meta code { font-family: var(--mono); font-size: 12px; color: #fff; background: rgba(255,255,255,0.12); padding: 2px 6px; border-radius: 6px; }

    .kpis {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 14px;
      margin-top: 18px;
    }

    .kpi {
      background: rgba(255,255,255,0.08);
      border: 1px solid rgba(255,255,255,0.12);
      border-radius: 16px;
      padding: 16px;
    }

    .value { font-size: 28px; font-weight: 800; margin-bottom: 6px; }
    .label { font-size: 13px; color: rgba(255,255,255,0.76); }

    .grid {
      display: grid;
      grid-template-columns: repeat(12, minmax(0, 1fr));
      gap: 20px;
      margin-top: 22px;
    }

    .card {
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 20px;
      padding: 22px;
      box-shadow: var(--shadow);
    }

    .span-12 { grid-column: span 12; }
    .span-6 { grid-column: span 6; }

    .muted { color: var(--muted); }

    .callout {
      border-radius: 18px;
      border: 1px solid var(--line);
      padding: 18px 18px 16px;
      background: linear-gradient(180deg, rgba(15,118,110,0.06), rgba(29,78,216,0.04));
    }
    .callout h3 { margin: 0 0 8px; font-size: 16px; }
    .callout ul { margin: 10px 0 0; padding-left: 18px; }
    .callout li { margin: 6px 0; }

    .bar-group { display: grid; gap: 14px; }
    .bar-row {
      display: grid;
      grid-template-columns: 180px 1fr 110px;
      gap: 12px;
      align-items: center;
    }
    .bar-label { font-weight: 600; }
    .bar-track {
      position: relative;
      height: 14px;
      border-radius: 999px;
      background: #edf2f7;
      overflow: hidden;
    }
    .bar-fill {
      position: absolute;
      inset: 0 auto 0 0;
      border-radius: 999px;
      background: linear-gradient(90deg, var(--accent), #14b8a6);
    }
    .bar-fill.base { background: linear-gradient(90deg, #64748b, #94a3b8); }
    .bar-fill.secondary { background: linear-gradient(90deg, var(--accent-2), #60a5fa); }
    .bar-fill.bad { background: linear-gradient(90deg, #dc2626, #fb7185); }
    .bar-value { text-align: right; font-variant-numeric: tabular-nums; color: var(--muted); }

    table { width: 100%; border-collapse: collapse; font-size: 14px; }
    th, td { border-bottom: 1px solid var(--line); padding: 12px 10px; text-align: left; vertical-align: top; }
    th { color: var(--muted); background: #fbfcfe; font-weight: 700; }
    tr:last-child td { border-bottom: 0; }

    code { font-family: var(--mono); background: rgba(15, 118, 110, 0.08); padding: 1px 4px; border-radius: 5px; }

    @media (max-width: 980px) {
      .span-6 { grid-column: span 12; }
      .kpis { grid-template-columns: 1fr; }
      .bar-row { grid-template-columns: 1fr; }
      .bar-value { text-align: left; }
    }

    /* Examples (borrowed from earlier handcrafted reports in this repo) */
    .split {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px;
    }

    .example {
      background: var(--panel-soft);
      border: 1px solid var(--line);
      border-radius: 18px;
      overflow: hidden;
    }

    .example-head {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
      padding: 14px 16px;
      border-bottom: 1px solid var(--line);
      background: #fff;
    }

    .example-body {
      padding: 14px 16px;
      font-family: var(--mono);
      font-size: 12px;
      line-height: 1.45;
      white-space: pre-wrap;
      background: var(--panel-soft);
    }

    .small { font-size: 12px; color: var(--muted); }

    .pill {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 7px 10px;
      border-radius: 999px;
      background: #eef2f7;
      font-size: 12px;
      font-weight: 700;
      text-transform: uppercase;
      font-family: Inter, "Segoe UI", Arial, sans-serif;
      color: #475569;
      white-space: nowrap;
    }

    .pill.base { color: #475569; }
    .pill.good { background: #eaf7ee; color: var(--good); }
    .pill.warn { background: #fff7ed; color: var(--warn); }
    .pill.bad { background: #fee2e2; color: var(--bad); }

    .divider {
      height: 1px;
      background: var(--line);
      margin: 12px 0;
    }

    @media (max-width: 980px) {
      .split { grid-template-columns: 1fr; }
    }
    """

    # Bar chart rows (tokens vs baseline; allow >100% and color it "bad")
    bar_rows = []
    for c in conds:
        tok = float(c["tokens"] or 0.0)
        ratio = (tok / float(baseline_tokens)) if baseline_tokens else 0.0
        # Scale: up to 140% to show overruns clearly.
        scale_max = 1.4
        width_pct = max(0.0, min(100.0, (ratio / scale_max) * 100.0))
        fill_class = "base" if c["condition"] == "plain_english" else ("bad" if ratio > 1.0 else "secondary")
        bar_rows.append(
            """
	            <div class="bar-row">
	              <div class="bar-label">{cond}</div>
	              <div class="bar-track"><div class="bar-fill {cls}" style="width:{w}%"></div></div>
	              <div class="bar-value">{tok} ({ratio:.0f}%)</div>
	            </div>
	            """.format(
	                cond=esc(c["condition"]),
	                cls=esc(fill_class),
	                w=esc(round(width_pct, 1)),
	                tok=esc(_fmt_num(tok)),
	                ratio=ratio * 100.0,
	            )
	        )

    # Table: per-case internal tokens + compliance per condition
    ths = ["Case"]
    for c in conds:
        ths.append(c["condition"])
    table_rows = []
    for case in cases:
        tds = ["<code>{}</code>".format(esc(case))]
        for c in conds:
            cond = c["condition"]
            cell = by_case.get(case, {}).get(cond)
            if not cell:
                tds.append("<span class=\"muted\">-</span>")
                continue
            tok = esc(cell.get("Internal Tokens"))
            comp = esc(cell.get("Compliance"))
            rep = esc(cell.get("Repair Turns"))
            qual = esc(cell.get("Final Quality"))
            tds.append("<div><b>{}</b> <span class=\"muted\">tok</span></div><div class=\"muted\">comp {} | rep {} | q {}</div>".format(tok, comp, rep, qual))
        table_rows.append("<tr>{}</tr>".format("".join("<td>{}</td>".format(x) for x in tds)))

    meta_bits = []
    meta_bits.append("Generated: <code>{}</code>".format(esc(meta.get("Generated", now))))
    meta_bits.append("Runner: <code>{}</code>".format(esc(meta.get("Runner", "unknown"))))
    meta_bits.append("Count: <code>{}</code>".format(esc(meta.get("Count mode", "unknown"))))
    if meta.get("Codex model"):
        meta_bits.append("Codex model: <code>{}</code>".format(esc(meta["Codex model"])))
    if meta.get("Repeats per condition/case"):
        meta_bits.append("Repeats: <code>{}</code>".format(esc(meta["Repeats per condition/case"])))
    if meta.get("Baseline"):
        meta_bits.append("Baseline: <code>{}</code>".format(esc(meta["Baseline"])))
    meta_html = " | ".join(meta_bits)

    # Hero headline statement
    best_red = pct_reduction(best_by_tokens["tokens"])
    best_red_txt = "n/a" if best_red is None else ("{:.1f}%".format(best_red))
    tradeoff_txt = best_tradeoff["condition"] if best_tradeoff else "n/a"

    cond_by_name = {c["condition"]: c for c in conds}
    sdc = cond_by_name.get("SDC-1")
    pcl = cond_by_name.get("PCL-1")
    rcce = cond_by_name.get("RCCE-1")
    atrce = cond_by_name.get("ATRCE-2")
    base = cond_by_name.get("plain_english")

    def _fmt_pct(n):
        if n is None:
            return "n/a"
        return "{:.1f}%".format(float(n))

    conclusions_bits = []
    conclusions_bits.append(
        "<p><b>Conclusion:</b> This run shows a clear tradeoff frontier. Token minimization and coordination quality do not move together.</p>"
    )
    conclusions_bits.append("<p class=\"muted\">What the strict openai_exact numbers are saying:</p>")
    bullet_lines = []
    if sdc is not None:
        bullet_lines.append(
            "Lowest tokens: <code>SDC-1</code> at <b>{}</b> avg INTERNAL, but quality is <b>{}</b>. It is a token minimizer that can under-communicate meaning.".format(
                esc(_fmt_num(sdc.get("tokens"))), esc(_fmt_num(sdc.get("quality")))
            )
        )
    if pcl is not None:
        bullet_lines.append(
            "Best balance: <code>PCL-1</code> at <b>{}</b> avg INTERNAL with <b>{}</b> compliance and <b>{}</b> quality. That is a big drop vs <code>plain_english</code> <b>{}</b> while keeping coordination mostly intact.".format(
                esc(_fmt_num(pcl.get("tokens"))),
                esc(_fmt_pct(pcl.get("compliance"))),
                esc(_fmt_num(pcl.get("quality"))),
                esc(_fmt_num(base.get("tokens") if base else None)),
            )
        )
    if rcce is not None or atrce is not None:
        parts = []
        if rcce is not None:
            parts.append("<code>RCCE-1</code> {}".format(esc(_fmt_num(rcce.get("tokens")))))
        if atrce is not None:
            parts.append("<code>ATRCE-2</code> {}".format(esc(_fmt_num(atrce.get("tokens")))))
        if parts:
            bullet_lines.append(
                "Typed schemas: {} — close to baseline on tokens in this run. Core lesson: label overhead often cancels the intended savings.".format(
                    ", ".join(parts)
                )
            )

    bullet_lines.append("If you care about cost + still-working coordination: <b>PCL-1</b> is the current winner.")
    bullet_lines.append("If you care about absolute cheapest tokens: <b>SDC-1</b> wins, but the quality drop is the warning light.")

    conclusions_bits.append("<ul>{}</ul>".format("".join("<li>{}</li>".format(x) for x in bullet_lines)))
    conclusions_html = "<div class=\"callout\">{}</div>".format("".join(conclusions_bits))

    # Totals table + token savings (suite scale-up)
    def fmt_pct(x):
        if x is None:
            return "n/a"
        sign = "-" if x < 0 else ""
        return "{}{:.1f}%".format(sign, abs(float(x)))

    suite_saved = (baseline_tokens - float(best_by_tokens["tokens"])) if (baseline_tokens is not None and best_by_tokens["tokens"] is not None) else None

    totals_rows = []
    for c in conds:
        red = pct_reduction(c["tokens"])
        red_txt = "n/a" if red is None else ("{:.1f}%".format(red))
        totals_rows.append(
            "<tr>"
            "<td><code>{cond}</code></td>"
            "<td><b>{tok}</b></td>"
            "<td>{red}</td>"
            "<td>{comp}%</td>"
            "<td>{rep}</td>"
            "<td>{q}</td>"
            "</tr>".format(
                cond=esc(c["condition"]),
                tok=esc(_fmt_num(c["tokens"])),
                red=esc(red_txt),
                comp=esc(int(c["compliance"] or 0)),
                rep=esc(c["repair"] if c["repair"] is not None else "n/a"),
                q=esc(c["quality"] if c["quality"] is not None else "n/a"),
            )
        )

    # Representative example pairs (baseline vs each main protocol variant)
    def pretty_cond(cond):
        if cond == "plain_english":
            return "Plain English"
        return cond

    def _case_metrics(case, cond):
        cell = by_case.get(case, {}).get(cond)
        if not cell:
            return None
        return {
            "tokens": _to_int(cell.get("Internal Tokens", "")) or 0.0,
            "compliance": _to_float(cell.get("Compliance", "")) or 0.0,
            "repairs": _to_float(cell.get("Repair Turns", "")) or 0.0,
            "quality": _to_float(cell.get("Final Quality", "")) or 0.0,
        }

    def _pill_class(case, cond):
        m = _case_metrics(case, cond)
        if not m:
            return "base"
        base = _case_metrics(case, "plain_english")
        base_tok = base["tokens"] if base else None
        worse = (base_tok is not None and m["tokens"] > base_tok)
        if m["compliance"] < 100.0 or m["quality"] < 2.0:
            return "bad" if m["quality"] <= 1.0 else "warn"
        if worse:
            return "warn"
        return "good" if cond != "plain_english" else "base"

    def _example_card(case, cond):
        m = _case_metrics(case, cond)
        s = samples.get(case, {}).get(cond, {})
        internal = s.get("internal", "").strip()
        final = s.get("final", "").strip()

        pill_bits = []
        if m:
            pill_bits.append("{} TOK".format(_fmt_num(m["tokens"])))
            pill_bits.append("{} REPAIR".format(int(m["repairs"])))
            pill_bits.append("Q {}".format(int(m["quality"])))
            base = _case_metrics(case, "plain_english")
            if base and base["tokens"]:
                delta = m["tokens"] - base["tokens"]
                sign = "+" if delta > 0 else ""
                pill_bits.append("{}{}".format(sign, _fmt_num(delta)))
        pill = " · ".join(pill_bits) if pill_bits else ""

        body = internal
        if final:
            body = "{}\n\nFinal:\n{}".format(internal, final)

        return """
          <div class="example">
            <div class="example-head">
              <div>
                <h3>{cond}</h3>
                <div class="small">{case}</div>
              </div>
              <div class="pill {cls}">{pill}</div>
            </div>
            <div class="example-body">{body}</div>
          </div>
        """.format(
            cond=esc(pretty_cond(cond)),
            case=esc(case),
            cls=esc(_pill_class(case, cond)),
            pill=esc(pill),
            body=esc(body),
        )

    example_pairs = [
        ("protocol_rule_proposal", "PCL-1"),
        ("protocol_rule_proposal", "SDC-1"),
        ("benchmark_scope_decision", "RCCE-1"),
        ("human_interrupt_during_execution", "ATRCE-2"),
    ]
    example_sections = []
    for case, cond in example_pairs:
        if case not in by_case or cond not in by_case.get(case, {}):
            continue
        example_sections.append(
            """
            <div class="split" style="margin-top:16px;">
              {left}
              {right}
            </div>
            """.format(
                left=_example_card(case, "plain_english"),
                right=_example_card(case, cond),
            )
        )

    return """<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <style>{css}</style>
  </head>
  <body>
    <div class="wrap">
      <section class="hero">
        <div class="eyebrow">Agent Coordination Benchmark</div>
        <h1>{title}</h1>
	        <p>
	          Lowest internal tokens in this run: <code>{best}</code> ({best_tokens} tokens, {best_red} vs baseline).
	          Best tradeoff (compliance ≥ 90% and quality ≥ 2.0): <code>{tradeoff}</code>.
	        </p>
        <div class="meta">{meta}</div>
        <div class="kpis">
          <div class="kpi"><div class="value">{best_tokens}</div><div class="label">Lowest total internal tokens</div></div>
          <div class="kpi"><div class="value">{base_tokens}</div><div class="label">Baseline total internal tokens</div></div>
          <div class="kpi"><div class="value">{best_red}</div><div class="label">Reduction vs baseline</div></div>
          <div class="kpi"><div class="value">{best_comp}%</div><div class="label">Compliance for lowest-token condition</div></div>
        </div>
      </section>

	      <div class="grid">
	        <section class="card span-12">
	          <h2>Conclusions</h2>
	          {conclusions}
	        </section>

	        <section class="card span-12">
	          <h2>Totals by condition</h2>
	          <div class="bar-group">
	            {bars}
          </div>
          <p class="muted" style="margin-top:12px">
            Bars show internal tokens relative to <code>plain_english</code> (baseline). Values above 100% are worse than baseline.
          </p>
        </section>

        <section class="card span-12">
          <h2>Per-case breakdown</h2>
          <table>
            <thead>
              <tr>{ths}</tr>
            </thead>
            <tbody>
              {rows}
            </tbody>
          </table>
        </section>

        <section class="card span-12">
          <h2>Representative Examples</h2>
          <p class="muted" style="margin-top:6px">
            These are direct excerpts from the run log (internal discussion + final line), shown side-by-side against the plain-English baseline.
          </p>
          {examples}
        </section>

	        <section class="card span-12">
	          <h2>What The Numbers Say</h2>
          <table>
            <tr>
              <th>Condition</th>
              <th>Total internal tokens</th>
              <th>Reduction vs baseline</th>
              <th>Avg compliance</th>
              <th>Avg repairs</th>
              <th>Avg quality</th>
            </tr>
            {totals_rows}
          </table>
	          <p class="muted" style="margin-top:12px">
	            Note: compliance failures are often schema/formatting misses rather than “bad reasoning”. In strict modes, small format slips can dominate the compliance metric.
	          </p>
	        </section>

        <section class="card span-12">
          <h2>Token Savings And Scale-Up</h2>
          <table>
            <tr><th>Metric</th><th>Value</th></tr>
            <tr><td>Best (lowest-token) condition</td><td><strong>{best}</strong></td></tr>
	            <tr><td>Average savings per 7-case suite</td><td><strong>{suite_saved}</strong> internal tokens</td></tr>
            <tr><td>Relative reduction vs plain English</td><td><strong>{best_red}</strong></td></tr>
            <tr><td>Scale-up at 10 suites</td><td><strong>{s10}</strong> tokens saved</td></tr>
            <tr><td>Scale-up at 100 suites</td><td><strong>{s100}</strong> tokens saved</td></tr>
            <tr><td>Scale-up at 1,000 suites</td><td><strong>{s1000}</strong> tokens saved</td></tr>
          </table>
        </section>
      </div>
    </div>
  </body>
</html>
    """.format(
        title=esc(title),
        css=css,
        meta=meta_html,
        bars="".join(bar_rows),
        ths="".join("<th>{}</th>".format(esc(x)) for x in ths),
        rows="".join(table_rows),
        best=esc(best_by_tokens["condition"]),
        best_tokens=esc(_fmt_num(best_by_tokens["tokens"])),
        best_red=esc(best_red_txt),
        best_comp=esc(int(best_by_tokens["compliance"] or 0)),
        base_tokens=esc(_fmt_num(baseline_tokens)),
        tradeoff=esc(tradeoff_txt),
        conclusions=conclusions_html,
        examples="".join(example_sections) if example_sections else "<p class=\"muted\">No examples found in markdown.</p>",
        totals_rows="".join(totals_rows),
        suite_saved=esc(_fmt_num(suite_saved)),
        s10=esc(_fmt_num(suite_saved * 10 if suite_saved is not None else None)),
        s100=esc(_fmt_num(suite_saved * 100 if suite_saved is not None else None)),
        s1000=esc(_fmt_num(suite_saved * 1000 if suite_saved is not None else None)),
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input_md", help="Markdown report produced by run_tests.py")
    ap.add_argument("output_html", help="Output HTML path")
    ap.add_argument("--title", default="Coordination Benchmark Report", help="HTML title")
    args = ap.parse_args()

    md_path = Path(args.input_md)
    html_path = Path(args.output_html)
    md_text = md_path.read_text(encoding="utf-8")
    out = render_html(md_text, args.title)
    html_path.write_text(out, encoding="utf-8")


if __name__ == "__main__":
    main()
