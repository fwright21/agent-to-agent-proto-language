#!/usr/bin/env python3
"""
Render a single HTML dashboard comparing multiple run_tests.py markdown reports.

Input: one or more markdown reports that include a "## Summary Table" section with
"**TOTAL / AVG**" rows.

Usage:
  python render_multi_dashboard.py \
    --report "Round 4 Prompt 2 exact=round_04/.../10_...md" \
    --report "Round 5 r2 strict=round_05/.../11_...md" \
    --output dashboard.html
"""

from __future__ import annotations

import argparse
import datetime
import html
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple


@dataclass(frozen=True)
class TotalsRow:
    condition: str
    internal_tokens: Optional[int]
    compliance: Optional[float]
    repair_turns: Optional[float]
    final_quality: Optional[float]


@dataclass(frozen=True)
class Report:
    label: str
    path: str
    meta: Dict[str, str]
    totals: List[TotalsRow]
    samples: Dict[str, Dict[str, Dict[str, str]]]


def _parse_per_case_samples(md_text: str) -> Dict[str, Dict[str, Dict[str, str]]]:
    """
    Parse "## Per-Case Results" and extract Internal/Final samples.

    Returns:
      samples[case][condition] = {"internal": str, "final": str}
    """
    m = re.search(
        r"^## Per-Case Results\s*\n\n(.*?)(?=^## Summary Table\s*$)",
        md_text,
        flags=re.MULTILINE | re.DOTALL,
    )
    if not m:
        return {}

    section = m.group(1)
    samples: Dict[str, Dict[str, Dict[str, str]]] = {}

    case_iter = re.finditer(
        r"^###\s+(?P<case>[^\n]+)\s*\n\n(?P<body>.*?)(?=^###\s+|\Z)",
        section,
        flags=re.MULTILINE | re.DOTALL,
    )
    for cm in case_iter:
        case = cm.group("case").strip()
        body = cm.group("body")
        samples.setdefault(case, {})

        # Condition blocks with Internal sample / Final sample code fences.
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


def _parse_kv_header(md_text: str) -> Dict[str, str]:
    out: Dict[str, str] = {}
    keys = [
        "Generated",
        "Runner",
        "Count mode",
        "Codex model",
        "Claude model",
        "Repeats per condition/case",
        "Baseline",
        "Conditions",
    ]
    for key in keys:
        m = re.search(r"^" + re.escape(key) + r":\s*(.*)\s*$", md_text, flags=re.MULTILINE)
        if m:
            out[key] = m.group(1).strip()
    return out


def _parse_summary_table(md_text: str) -> List[Dict[str, str]]:
    m = re.search(r"^## Summary Table\s*\n\n(\|.*\n\|---.*\n(?:\|.*\n)+)", md_text, flags=re.MULTILINE)
    if not m:
        raise ValueError("Could not find Summary Table in markdown")
    table = m.group(1).strip().splitlines()
    header = [c.strip() for c in table[0].strip("|").split("|")]
    rows: List[Dict[str, str]] = []
    for line in table[2:]:
        cols = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cols) != len(header):
            continue
        rows.append(dict(zip(header, cols)))
    return rows


def _to_float(s: str) -> Optional[float]:
    s = (s or "").strip().strip("*").replace("%", "")
    try:
        return float(s)
    except ValueError:
        return None


def _to_int(s: str) -> Optional[int]:
    s = (s or "").strip().strip("*")
    try:
        return int(float(s))
    except ValueError:
        return None


def _slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", (s or "").lower()).strip("-") or "x"


def _read_report(label: str, path: str) -> Report:
    md_text = Path(path).read_text(encoding="utf-8")
    meta = _parse_kv_header(md_text)
    rows = _parse_summary_table(md_text)
    samples = _parse_per_case_samples(md_text)

    totals: List[TotalsRow] = []
    for r in rows:
        if r.get("Case") != "**TOTAL / AVG**":
            continue
        totals.append(
            TotalsRow(
                condition=(r.get("Condition") or "").strip("`"),
                internal_tokens=_to_int(r.get("Internal Tokens") or ""),
                compliance=_to_float(r.get("Compliance") or ""),
                repair_turns=_to_float(r.get("Repair Turns") or ""),
                final_quality=_to_float(r.get("Final Quality") or ""),
            )
        )
    if not totals:
        raise ValueError(f"No TOTAL / AVG rows found in {path}")
    return Report(label=label, path=path, meta=meta, totals=totals, samples=samples)


def _baseline_tokens(report: Report) -> Optional[int]:
    for t in report.totals:
        if t.condition == "plain_english":
            return t.internal_tokens
    return None


def _pct_reduction(baseline: Optional[int], tokens: Optional[int]) -> Optional[float]:
    if baseline in (None, 0) or tokens is None:
        return None
    return round((baseline - tokens) / float(baseline) * 100.0, 1)


def _best_tradeoff(report: Report) -> Optional[TotalsRow]:
    pool = [
        t
        for t in report.totals
        if t.internal_tokens is not None
        and (t.compliance is None or t.compliance >= 90.0)
        and (t.final_quality is None or t.final_quality >= 2.0)
    ]
    return min(pool, key=lambda t: t.internal_tokens) if pool else None


def _best_tokens(report: Report) -> TotalsRow:
    return min([t for t in report.totals if t.internal_tokens is not None], key=lambda t: t.internal_tokens)


def render_dashboard(reports: List[Report], title: str) -> str:
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    css = """
    :root{
      --bg:#0b1220; --panel:#0f172a; --text:#e5e7eb; --muted:#94a3b8; --line:#22304a;
      --good:#22c55e; --blue:#60a5fa; --warn:#fbbf24; --bad:#fb7185;
      --mono: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
    }
    body{margin:0;font-family:Inter,system-ui,-apple-system,Segoe UI,Arial,sans-serif;background:radial-gradient(circle at 15% 10%,rgba(96,165,250,.18),transparent 35%),radial-gradient(circle at 85% 10%,rgba(34,197,94,.14),transparent 35%),var(--bg);color:var(--text);}
    .wrap{max-width:1240px;margin:0 auto;padding:34px 20px 70px;}
	    .hero{background:linear-gradient(120deg,rgba(96,165,250,.22),rgba(34,197,94,.18));border:1px solid rgba(255,255,255,.08);border-radius:18px;padding:18px 18px 16px;}
	    h1{margin:0;font-size:22px;letter-spacing:-.02em;}
	    .sub{margin-top:6px;color:var(--muted);font-size:13px;}
	    .toolbar{position:sticky;top:0;z-index:10;margin-top:12px;background:rgba(11,18,32,.72);backdrop-filter: blur(10px);border:1px solid rgba(255,255,255,.08);border-radius:14px;padding:10px 10px 8px;}
	    .tools{display:flex;flex-wrap:wrap;gap:10px;align-items:center;justify-content:space-between;}
	    .tools-left{display:flex;flex-wrap:wrap;gap:10px;align-items:center;}
	    .tools-right{display:flex;flex-wrap:wrap;gap:10px;align-items:center;}
	    .search{display:flex;align-items:center;gap:8px}
	    .search input{width:min(420px,70vw);padding:9px 10px;border-radius:10px;border:1px solid rgba(255,255,255,.10);background:rgba(15,23,42,.78);color:var(--text);font-size:13px;outline:none}
	    .search input::placeholder{color:rgba(148,163,184,.85)}
	    .btn{padding:9px 10px;border-radius:10px;border:1px solid rgba(255,255,255,.10);background:rgba(15,23,42,.78);color:var(--text);font-size:13px;cursor:pointer}
	    .btn:hover{border-color:rgba(96,165,250,.40)}
	    .nav{display:flex;flex-wrap:wrap;gap:8px;margin-top:8px}
	    .nav a{display:inline-block;padding:7px 9px;border:1px solid rgba(255,255,255,.10);border-radius:999px;background:rgba(15,23,42,.55);color:#cbd5e1;font-size:12px}
	    .nav a:hover{border-color:rgba(96,165,250,.40);text-decoration:none}
	    .grid{display:grid;grid-template-columns:1fr;gap:16px;margin-top:16px;}
	    .card{background:rgba(15,23,42,.82);border:1px solid rgba(255,255,255,.08);border-radius:16px;padding:16px;}
	    .card h2{margin:0 0 8px;font-size:16px;}
    .meta{margin:0 0 10px;padding-left:18px;color:var(--muted);font-size:12px;}
    .meta .k{color:#cbd5e1;}
    code{font-family:var(--mono);font-size:12px;color:#e2e8f0;}
    a{color:var(--blue);text-decoration:none;}
    a:hover{text-decoration:underline;}
	    .tbl{width:100%;border-collapse:collapse;overflow:hidden;border-radius:12px;}
	    .tbl th,.tbl td{border-bottom:1px solid rgba(255,255,255,.08);padding:10px 10px;text-align:left;font-size:13px;}
	    .tbl th{color:#cbd5e1;font-weight:600;background:rgba(255,255,255,.03);}
	    .hidden{display:none !important;}
	    .bars{margin:12px 0 10px;display:grid;gap:8px;}
	    .bar-row{display:grid;grid-template-columns:190px 1fr 88px;gap:10px;align-items:center;}
	    .bar-label{color:#cbd5e1;font-size:12px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
    .bar-track{position:relative;height:10px;border-radius:999px;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.08);overflow:hidden;}
    .bar-fill{height:100%;border-radius:999px;background:linear-gradient(90deg, rgba(96,165,250,.9), rgba(34,197,94,.9));}
    .bar-num{font-variant-numeric:tabular-nums;color:var(--muted);font-size:12px;text-align:right;}
    details{margin-top:10px;border:1px solid rgba(255,255,255,.08);border-radius:12px;padding:10px 12px;background:rgba(255,255,255,.02);}
    summary{cursor:pointer;color:#cbd5e1;font-size:13px;}
    .ex-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:10px;}
    .ex-card{border:1px solid rgba(255,255,255,.08);border-radius:12px;padding:10px;background:rgba(15,23,42,.5);}
    .ex-h{display:flex;justify-content:space-between;gap:10px;align-items:baseline;margin-bottom:6px;}
    .ex-h .name{font-size:12px;color:#e2e8f0;}
    .ex-h .case{font-size:11px;color:var(--muted);font-family:var(--mono);}
    pre{margin:8px 0 0;white-space:pre-wrap;word-break:break-word;background:rgba(0,0,0,.22);border:1px solid rgba(255,255,255,.08);border-radius:10px;padding:10px;color:#e5e7eb;font-size:12px;line-height:1.45;}
    .pill{display:inline-block;padding:2px 8px;border-radius:999px;border:1px solid rgba(255,255,255,.12);font-size:11px;color:var(--muted);margin-left:8px;}
    .pill.good{color:#bbf7d0;border-color:rgba(34,197,94,.35);background:rgba(34,197,94,.08);}
    .pill.warn{color:#fde68a;border-color:rgba(251,191,36,.35);background:rgba(251,191,36,.08);}
    .footer{margin-top:14px;color:var(--muted);font-size:12px;}
    @media (max-width: 960px){.wrap{padding:26px 14px 60px;}}
    @media (max-width: 960px){.bar-row{grid-template-columns:1fr 1fr 70px;}.ex-grid{grid-template-columns:1fr;}}
    """

    def esc(x: object) -> str:
        return html.escape("" if x is None else str(x))

    def meta_block(meta: Dict[str, str]) -> str:
        keys = ["Generated", "Runner", "Count mode", "Repeats per condition/case", "Baseline", "Conditions"]
        lis = []
        for k in keys:
            if k in meta:
                lis.append(f"<li><span class=\"k\">{esc(k)}:</span> <code>{esc(meta[k])}</code></li>")
        return "<ul class=\"meta\">" + "".join(lis) + "</ul>"

    def totals_table(report: Report) -> str:
        base = _baseline_tokens(report)
        best_tok = _best_tokens(report)
        best_tr = _best_tradeoff(report)

        columns = ["Condition", "Tokens", "Δ vs plain_english", "Compliance", "Repair", "Quality"]
        ths = "".join(f"<th>{esc(c)}</th>" for c in columns)

        def row_class(t: TotalsRow) -> str:
            if best_tr is not None and t.condition == best_tr.condition:
                return "good"
            if t.condition == best_tok.condition:
                return "warn" if best_tr is None or best_tok.condition != best_tr.condition else "good"
            return ""

        trs = []
        for t in sorted(report.totals, key=lambda x: (0 if x.condition == "plain_english" else 1, x.condition)):
            red = _pct_reduction(base, t.internal_tokens)
            red_txt = "" if red is None else (f"{red:+.1f}%")
            cls = row_class(t)
            pill = ""
            if cls == "good":
                pill = "<span class=\"pill good\">best tradeoff</span>"
            elif cls == "warn":
                pill = "<span class=\"pill warn\">lowest tokens</span>"
            trs.append(
                "<tr>"
                f"<td><code>{esc(t.condition)}</code>{pill}</td>"
                f"<td>{'' if t.internal_tokens is None else esc(t.internal_tokens)}</td>"
                f"<td>{esc(red_txt)}</td>"
                f"<td>{'' if t.compliance is None else esc(f'{t.compliance:.1f}%')}</td>"
                f"<td>{'' if t.repair_turns is None else esc(f'{t.repair_turns:.1f}')}</td>"
                f"<td>{'' if t.final_quality is None else esc(f'{t.final_quality:.1f}')}</td>"
                "</tr>"
            )

        note = ""
        if base is None:
            note = "<div class=\"footer\">No <code>plain_english</code> baseline found; Δ column is blank.</div>"
        return (
            "<table class=\"tbl\">"
            f"<thead><tr>{ths}</tr></thead>"
            f"<tbody>{''.join(trs)}</tbody>"
            "</table>"
            + note
        )

    def token_bars(report: Report) -> str:
        rows = [t for t in report.totals if t.internal_tokens is not None]
        if not rows:
            return ""
        max_tokens = max(t.internal_tokens for t in rows if t.internal_tokens is not None) or 1

        best_tok = _best_tokens(report)
        best_tr = _best_tradeoff(report)

        def tag(t: TotalsRow) -> str:
            if best_tr is not None and t.condition == best_tr.condition:
                return " best tradeoff"
            if t.condition == best_tok.condition:
                return " lowest tokens"
            return ""

        bar_rows = []
        for t in sorted(rows, key=lambda x: (0 if x.condition == "plain_english" else 1, x.condition)):
            width = int((t.internal_tokens / float(max_tokens)) * 100) if t.internal_tokens else 0
            bar_rows.append(
                "<div class=\"bar-row\">"
                f"<div class=\"bar-label\"><code>{esc(t.condition)}</code>{esc(tag(t))}</div>"
                f"<div class=\"bar-track\"><div class=\"bar-fill\" style=\"width:{width}%;\"></div></div>"
                f"<div class=\"bar-num\">{esc(t.internal_tokens)}</div>"
                "</div>"
            )
        return "<div class=\"bars\">" + "".join(bar_rows) + "</div>"

    def examples_block(report: Report) -> str:
        # Show a small set of representative cases if available.
        if not report.samples:
            return ""

        preferred_cases = ["missing_evidence_repair", "benchmark_scope_decision"]
        available_cases = [c for c in preferred_cases if c in report.samples] or list(report.samples.keys())[:1]
        if not available_cases:
            return ""

        best_tok = _best_tokens(report).condition
        best_tr = (_best_tradeoff(report).condition if _best_tradeoff(report) is not None else best_tok)

        def pick_cond_map(case: str, cond: str) -> Optional[Dict[str, str]]:
            # samples are keyed by display names (e.g., "PCL-1") not internal condition ids.
            return report.samples.get(case, {}).get(cond)

        # Determine the display-name keys present in this report for plain/protocols.
        # Try common display names used by run_tests.py.
        cond_keys = set()
        for case in report.samples:
            cond_keys.update(report.samples[case].keys())

        def resolve_display(condition_key: str) -> str:
            # condition_key here is internal (plain_english, pcl_1, ...)
            # We want the display name used in the markdown report.
            # Most markdown uses display_condition output: plain_english, RCCE-1, ATRCE-2, PCL-1, SDC-1.
            mapping = {
                "plain_english": "plain_english",
                "rcce_1": "RCCE-1",
                "atrce_2": "ATRCE-2",
                "pcl_1": "PCL-1",
                "sdc_1": "SDC-1",
            }
            return mapping.get(condition_key, condition_key)

        # best_tok/best_tr are internal ids in TotalsRow; markdown samples use display names.
        best_tok_disp = resolve_display(best_tok)
        best_tr_disp = resolve_display(best_tr)
        plain_disp = "plain_english"

        blocks = []
        for case in available_cases:
            left = pick_cond_map(case, plain_disp)
            right = pick_cond_map(case, best_tr_disp) or pick_cond_map(case, best_tok_disp)
            if left is None or right is None:
                continue
            blocks.append(
                "<div class=\"ex-grid\">"
                "<div class=\"ex-card\">"
                f"<div class=\"ex-h\"><div class=\"name\"><code>{esc(plain_disp)}</code></div><div class=\"case\">{esc(case)}</div></div>"
                f"<pre>{esc(left['internal'])}\n\nFINAL:\n{esc(left['final'])}</pre>"
                "</div>"
                "<div class=\"ex-card\">"
                f"<div class=\"ex-h\"><div class=\"name\"><code>{esc(best_tr_disp)}</code></div><div class=\"case\">{esc(case)}</div></div>"
                f"<pre>{esc(right['internal'])}\n\nFINAL:\n{esc(right['final'])}</pre>"
                "</div>"
                "</div>"
            )

        if not blocks:
            return ""

        return (
            "<details>"
            "<summary>Examples (plain_english vs best tradeoff)</summary>"
            + "".join(blocks)
            + "</details>"
        )

    cards = []
    for r in reports:
        rid = _slug(r.label)
        cards.append(
            f"<section class=\"card\" id=\"{rid}\" data-label=\"{esc(r.label).lower()}\">"
            f"<h2>{esc(r.label)}</h2>"
            f"<div class=\"sub\"><a href=\"{esc(r.path)}\">{esc(r.path)}</a></div>"
            f"{meta_block(r.meta)}"
            f"{token_bars(r)}"
            f"{totals_table(r)}"
            f"{examples_block(r)}"
            "</section>"
        )

    nav_links = "".join(
        f"<a href=\"#{_slug(r.label)}\" title=\"Jump to {esc(r.label)}\">{esc(r.label)}</a>" for r in reports
    )

    js = r"""
    <script>
      (function(){
        const q = document.getElementById('q');
        const cards = Array.from(document.querySelectorAll('.card[data-label]'));
        const details = Array.from(document.querySelectorAll('details'));
        const btnExamples = document.getElementById('toggle-examples');
        const btnClear = document.getElementById('clear-filter');

        function applyFilter() {
          const term = (q.value || '').trim().toLowerCase();
          cards.forEach(card => {
            const label = card.getAttribute('data-label') || '';
            card.classList.toggle('hidden', term && !label.includes(term));
          });
        }

        function setExamples(open) {
          details.forEach(d => { d.open = !!open; });
          btnExamples.setAttribute('data-open', open ? '1' : '0');
          btnExamples.textContent = open ? 'Collapse examples' : 'Expand examples';
        }

        q.addEventListener('input', applyFilter);
        btnClear.addEventListener('click', () => { q.value=''; applyFilter(); q.focus(); });
        btnExamples.addEventListener('click', () => {
          const open = btnExamples.getAttribute('data-open') !== '1';
          setExamples(open);
        });

        applyFilter();
        setExamples(false);
      })();
    </script>
    """

    return f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{esc(title)}</title>
  <style>{css}</style>
</head>
<body>
  <div class="wrap">
    <div class="hero">
      <h1>{esc(title)}</h1>
      <div class="sub">Generated {esc(now)} · Each panel is one benchmark report; within each panel, tokens and deltas are only comparable to that report’s own <code>plain_english</code> baseline.</div>
    </div>
    <div class="toolbar">
      <div class="tools">
        <div class="tools-left">
          <div class="search">
            <input id="q" type="search" placeholder="Filter reports by label…" autocomplete="off" />
            <button class="btn" id="clear-filter" type="button">Clear</button>
          </div>
        </div>
        <div class="tools-right">
          <button class="btn" id="toggle-examples" data-open="0" type="button">Expand examples</button>
        </div>
      </div>
      <div class="nav">{nav_links}</div>
    </div>
    <div class="grid">
      {''.join(cards)}
    </div>
    <div class="footer">This dashboard adds token bars + a small set of examples per report. For full per-case breakdowns, open the per-round HTML reports.</div>
  </div>
  {js}
</body>
</html>
"""


def _parse_report_arg(arg: str) -> Tuple[str, str]:
    if "=" not in arg:
        raise ValueError("--report must look like 'Label=path/to/report.md'")
    # Labels may contain '=' (e.g., "repeats=3"), but paths should not.
    label, path = arg.rsplit("=", 1)
    label = label.strip()
    path = path.strip()
    if not label or not path:
        raise ValueError("--report must have non-empty label and path")
    return label, path


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", action="append", default=[], help="Report spec: Label=path/to/report.md (repeatable)")
    ap.add_argument("--title", default="Benchmark Dashboard")
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    if not args.report:
        raise SystemExit("No --report provided")

    reports: List[Report] = []
    for spec in args.report:
        label, path = _parse_report_arg(spec)
        reports.append(_read_report(label, path))

    out = render_dashboard(reports, args.title)
    Path(args.output).write_text(out, encoding="utf-8")


if __name__ == "__main__":
    main()
