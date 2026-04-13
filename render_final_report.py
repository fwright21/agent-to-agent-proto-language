#!/usr/bin/env python3
"""
Render a single compiled HTML report from one or more `run_tests.py` markdown reports.

Goal:
- One shareable page with: prompts, per-protocol results, examples, conclusions, and token amounts.
- No dependency on external packages.

Input:
- Markdown reports produced by `run_tests.py` that contain:
  - "## Per-Case Results" with per-case blocks and samples
  - "## Summary Table" with a "TOTAL / AVG" row per condition
"""

from __future__ import annotations

import argparse
import datetime as _dt
import html
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple


def esc(s: str) -> str:
    return html.escape(s, quote=True)


@dataclass(frozen=True)
class ConditionTotals:
    condition: str
    internal_tokens: Optional[float]
    compliance: Optional[float]
    repair_turns: Optional[float]
    final_quality: Optional[float]


@dataclass(frozen=True)
class ConditionCase:
    condition: str
    internal_tokens: Optional[float]
    compliance: Optional[float]
    repair_turns: Optional[float]
    final_quality: Optional[float]
    internal_sample: str
    final_sample: str


@dataclass(frozen=True)
class CaseBlock:
    case: str
    task: str
    by_condition: Dict[str, ConditionCase]


@dataclass(frozen=True)
class Report:
    label: str
    path: str
    meta: Dict[str, str]
    totals: Dict[str, ConditionTotals]
    cases: List[CaseBlock]


def _parse_meta(md_text: str) -> Dict[str, str]:
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


def _parse_summary_totals(md_text: str) -> Dict[str, ConditionTotals]:
    m = re.search(
        r"^## Summary Table\s*\n\n(\|.*\n\|---.*\n(?:\|.*\n)+)",
        md_text,
        flags=re.MULTILINE,
    )
    if not m:
        return {}

    table = m.group(1).strip().splitlines()
    header = [c.strip() for c in table[0].strip("|").split("|")]
    rows = []
    for line in table[2:]:
        cols = [c.strip() for c in line.strip("|").split("|")]
        if len(cols) != len(header):
            continue
        rows.append(dict(zip(header, cols)))

    totals: Dict[str, ConditionTotals] = {}
    for r in rows:
        if r.get("Case") != "TOTAL / AVG":
            continue
        cond = r.get("Condition", "")
        if not cond:
            continue

        def fnum(key: str) -> Optional[float]:
            raw = (r.get(key) or "").strip()
            if not raw:
                return None
            try:
                return float(raw)
            except ValueError:
                return None

        totals[cond] = ConditionTotals(
            condition=cond,
            internal_tokens=fnum("Internal Tokens"),
            compliance=fnum("Compliance"),
            repair_turns=fnum("Repair Turns"),
            final_quality=fnum("Final Quality"),
        )
    return totals


_COND_LINE_RE = re.compile(
    r"^\*\*(?P<cond>[^*]+)\*\*:\s*(?P<tok>[0-9.]+)\s+avg internal tokens.*?;"
    r"\s*compliance\s+(?P<comp>[0-9.]+)%\s*;\s*repair turns\s+(?P<rep>[0-9.]+)\s*;\s*final quality\s+(?P<q>[0-9.]+)",
    re.IGNORECASE | re.MULTILINE,
)


def _parse_case_blocks(md_text: str) -> List[CaseBlock]:
    # Limit parsing to the per-case section.
    start = md_text.find("## Per-Case Results")
    if start == -1:
        return []
    section = md_text[start:]

    # Stop at Summary Table.
    end = section.find("\n## Summary Table")
    if end != -1:
        section = section[:end]

    case_splits = re.split(r"^###\s+", section, flags=re.MULTILINE)
    # First chunk is header text before first case.
    case_chunks = case_splits[1:]

    out: List[CaseBlock] = []
    for chunk in case_chunks:
        lines = chunk.splitlines()
        if not lines:
            continue
        case = lines[0].strip()
        body = "\n".join(lines[1:])

        task_m = re.search(r"^Task:\s*_(.*?)_\s*$", body, flags=re.MULTILINE | re.DOTALL)
        task = task_m.group(1).strip() if task_m else ""

        by_condition: Dict[str, ConditionCase] = {}

        # Split by condition header lines that start with **COND**:
        cond_parts = re.split(r"^\*\*(?P<cond>[^*]+)\*\*:\s+", body, flags=re.MULTILINE)
        # cond_parts alternates: [pre, cond, rest, cond, rest, ...]
        if len(cond_parts) < 3:
            continue
        for i in range(1, len(cond_parts), 2):
            cond = cond_parts[i].strip()
            rest = cond_parts[i + 1]

            # Reconstruct the original first line for regex parsing.
            first_line = f"**{cond}**: " + (rest.splitlines()[0] if rest.splitlines() else "")
            line_m = _COND_LINE_RE.search(first_line)
            tok = float(line_m.group("tok")) if line_m else None
            comp = float(line_m.group("comp")) if line_m else None
            rep = float(line_m.group("rep")) if line_m else None
            q = float(line_m.group("q")) if line_m else None

            internal = ""
            final = ""
            im = re.search(r"Internal sample:\s*```text\s*(.*?)\s*```", rest, flags=re.DOTALL)
            if im:
                internal = im.group(1).rstrip()
            fm = re.search(r"Final sample:\s*```text\s*(.*?)\s*```", rest, flags=re.DOTALL)
            if fm:
                final = fm.group(1).rstrip()

            by_condition[cond] = ConditionCase(
                condition=cond,
                internal_tokens=tok,
                compliance=comp,
                repair_turns=rep,
                final_quality=q,
                internal_sample=internal,
                final_sample=final,
            )

        out.append(CaseBlock(case=case, task=task, by_condition=by_condition))

    return out


def _infer_best_tradeoff(totals: Dict[str, ConditionTotals]) -> Optional[str]:
    # Heuristic: compliance >= 90 and quality >= 2, then lowest tokens.
    eligible: List[Tuple[float, str]] = []
    for cond, t in totals.items():
        if t.internal_tokens is None or t.compliance is None or t.final_quality is None:
            continue
        if t.compliance >= 90.0 and t.final_quality >= 2.0:
            eligible.append((t.internal_tokens, cond))
    if not eligible:
        return None
    return sorted(eligible, key=lambda x: (x[0], x[1]))[0][1]


def _infer_lowest_tokens(totals: Dict[str, ConditionTotals]) -> Optional[str]:
    items = [(t.internal_tokens, cond) for cond, t in totals.items() if t.internal_tokens is not None]
    if not items:
        return None
    return sorted(items, key=lambda x: (x[0], x[1]))[0][1]


def _sorted_conditions(totals: Dict[str, ConditionTotals]) -> List[str]:
    return [c for _, c in sorted(((t.internal_tokens or 10**18, c) for c, t in totals.items()))]


def render(reports: List[Report], title: str) -> str:
    now = _dt.datetime.now().strftime("%Y-%m-%d %H:%M")

    css = """
    :root{
      --bg:#0b1220; --panel:#0f172a; --panel2:#0b1326; --text:#e5e7eb; --muted:#94a3b8; --line:#22304a;
      --blue:#60a5fa; --green:#22c55e; --warn:#fbbf24; --bad:#fb7185;
      --mono: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
    }
    *{box-sizing:border-box}
    body{margin:0;font-family:Inter,system-ui,-apple-system,Segoe UI,Arial,sans-serif;background:radial-gradient(circle at 15% 10%,rgba(96,165,250,.18),transparent 35%),radial-gradient(circle at 85% 10%,rgba(34,197,94,.14),transparent 35%),var(--bg);color:var(--text);line-height:1.45}
    .wrap{max-width:1180px;margin:0 auto;padding:34px 18px 80px}
    .hero{background:linear-gradient(120deg,rgba(96,165,250,.22),rgba(34,197,94,.18));border:1px solid rgba(255,255,255,.08);border-radius:18px;padding:18px 18px 14px}
    h1{margin:0;font-size:22px;letter-spacing:-.02em}
    .sub{margin-top:6px;color:var(--muted);font-size:13px}
    .pill{display:inline-flex;gap:8px;align-items:center;padding:6px 10px;border:1px solid rgba(255,255,255,.10);border-radius:999px;background:rgba(255,255,255,.02);font-size:12px;color:#cbd5e1}
    .pill b{font-variant-numeric:tabular-nums}
    .pills{display:flex;flex-wrap:wrap;gap:8px;margin-top:10px}
    .card{margin-top:14px;background:rgba(15,23,42,.82);border:1px solid rgba(255,255,255,.08);border-radius:16px;padding:16px}
    .card h2{margin:0 0 10px;font-size:16px}
    .muted{color:var(--muted)}
    a{color:var(--blue);text-decoration:none}
    a:hover{text-decoration:underline}
    code, pre{font-family:var(--mono)}
    pre{background:rgba(2,6,23,.55);border:1px solid rgba(255,255,255,.08);border-radius:14px;padding:12px;overflow:auto;margin:10px 0 0}
    .tbl{width:100%;border-collapse:collapse;overflow:hidden;border-radius:12px}
    .tbl th,.tbl td{border-bottom:1px solid rgba(255,255,255,.08);padding:10px 10px;text-align:left;font-size:13px;vertical-align:top}
    .tbl th{color:#cbd5e1;font-weight:600;background:rgba(255,255,255,.03)}
    .tbl td:nth-child(2), .tbl td:nth-child(3), .tbl td:nth-child(4), .tbl td:nth-child(5){font-variant-numeric:tabular-nums}
    details{margin-top:10px}
    summary{cursor:pointer;color:#cbd5e1;font-size:13px}
    .case{padding:14px;border:1px solid rgba(255,255,255,.08);border-radius:14px;background:rgba(2,6,23,.20);margin-top:12px}
    .case h3{margin:0;font-size:14px}
    .grid2{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:10px}
    @media (max-width: 980px){ .grid2{grid-template-columns:1fr} }
    """

    # Conclusions: derive from the report that contains PCL-1 if possible.
    conclusion_lines: List[str] = []
    for r in reports:
        if "PCL-1" in r.totals:
            best = _infer_best_tradeoff(r.totals) or "PCL-1"
            low = _infer_lowest_tokens(r.totals)
            t_best = r.totals.get(best)
            t_low = r.totals.get(low) if low else None
            base = r.meta.get("Baseline", "`plain_english`")
            conclusion_lines.append(
                f"<li><b>Best balance:</b> <code>{esc(best)}</code>"
                + (f" ({t_best.internal_tokens:.1f} internal tokens; {t_best.compliance:.1f}% compliance)" if t_best and t_best.internal_tokens is not None and t_best.compliance is not None else "")
                + f", compared to baseline {esc(base)}.</li>"
            )
            if low and t_low and t_low.internal_tokens is not None:
                conclusion_lines.append(
                    f"<li><b>Lowest tokens:</b> <code>{esc(low)}</code> ({t_low.internal_tokens:.1f} internal tokens) — but ultra-compression can under-communicate meaning in this suite.</li>"
                )
            conclusion_lines.append(
                "<li><b>Typed schemas:</b> easy to validate, but label overhead often cancels intended savings on short messages.</li>"
            )
            break
    if not conclusion_lines:
        conclusion_lines.append("<li>See totals and per-case breakdown below.</li>")

    conclusions_html = (
        "<div class=\"card\">"
        "<h2>Conclusions</h2>"
        "<ul>"
        + "".join(conclusion_lines)
        + "</ul>"
        "</div>"
    )

    report_cards: List[str] = []
    for r in reports:
        best = _infer_best_tradeoff(r.totals)
        low = _infer_lowest_tokens(r.totals)

        pills = []
        if best:
            pills.append(f"<span class=\"pill\">Best balance: <code>{esc(best)}</code></span>")
        if low:
            pills.append(f"<span class=\"pill\">Lowest tokens: <code>{esc(low)}</code></span>")

        # Totals table
        conds = _sorted_conditions(r.totals)
        base = r.meta.get("Baseline", "plain_english").strip("`")
        base_tok = r.totals.get(base).internal_tokens if base in r.totals else None

        rows = []
        for c in conds:
            t = r.totals[c]
            tok = "" if t.internal_tokens is None else f"{t.internal_tokens:.1f}"
            delta = ""
            if base_tok and t.internal_tokens is not None:
                delta = f"{((base_tok - t.internal_tokens) / base_tok * 100):.1f}%"
            comp = "" if t.compliance is None else f"{t.compliance:.1f}%"
            rep = "" if t.repair_turns is None else f"{t.repair_turns:.1f}"
            q = "" if t.final_quality is None else f"{t.final_quality:.1f}"
            rows.append(
                "<tr>"
                f"<td><code>{esc(c)}</code></td>"
                f"<td>{esc(tok)}</td>"
                f"<td>{esc(delta)}</td>"
                f"<td>{esc(comp)}</td>"
                f"<td>{esc(rep)}</td>"
                f"<td>{esc(q)}</td>"
                "</tr>"
            )

        totals_table = (
            "<table class=\"tbl\">"
            "<thead><tr>"
            "<th>Condition</th><th>Internal Tokens</th><th>Δ vs baseline</th><th>Compliance</th><th>Repair</th><th>Quality</th>"
            "</tr></thead>"
            "<tbody>"
            + "".join(rows)
            + "</tbody></table>"
        )

        # Per-case blocks
        case_html = []
        for cb in r.cases:
            by = cb.by_condition
            best_cond = best if best in by else None
            base_cond = base if base in by else None

            # Per-case quick table
            case_rows = []
            for c in _sorted_conditions({k: ConditionTotals(k, v.internal_tokens, v.compliance, v.repair_turns, v.final_quality) for k, v in by.items()}):
                v = by[c]
                tok = "" if v.internal_tokens is None else f"{v.internal_tokens:.1f}"
                comp = "" if v.compliance is None else f"{v.compliance:.1f}%"
                rep = "" if v.repair_turns is None else f"{v.repair_turns:.1f}"
                q = "" if v.final_quality is None else f"{v.final_quality:.1f}"
                case_rows.append(
                    "<tr>"
                    f"<td><code>{esc(c)}</code></td>"
                    f"<td>{esc(tok)}</td>"
                    f"<td>{esc(comp)}</td>"
                    f"<td>{esc(rep)}</td>"
                    f"<td>{esc(q)}</td>"
                    "</tr>"
                )

            case_table = (
                "<table class=\"tbl\">"
                "<thead><tr><th>Condition</th><th>Internal Tokens</th><th>Compliance</th><th>Repair</th><th>Quality</th></tr></thead>"
                "<tbody>" + "".join(case_rows) + "</tbody></table>"
            )

            # Examples: default show baseline vs best. Others in details.
            examples = []
            if base_cond and best_cond and base_cond != best_cond:
                left = by[base_cond]
                right = by[best_cond]
                examples.append(
                    "<div class=\"grid2\">"
                    "<div>"
                    f"<div class=\"muted\"><b>Baseline</b> <code>{esc(base_cond)}</code></div>"
                    f"<div class=\"muted\" style=\"margin-top:8px\">INTERNAL</div>"
                    f"<pre>{esc(left.internal_sample or '')}</pre>"
                    f"<div class=\"muted\" style=\"margin-top:8px\">FINAL</div>"
                    f"<pre>{esc(left.final_sample or '')}</pre>"
                    "</div>"
                    "<div>"
                    f"<div class=\"muted\"><b>Best balance</b> <code>{esc(best_cond)}</code></div>"
                    f"<div class=\"muted\" style=\"margin-top:8px\">INTERNAL</div>"
                    f"<pre>{esc(right.internal_sample or '')}</pre>"
                    f"<div class=\"muted\" style=\"margin-top:8px\">FINAL</div>"
                    f"<pre>{esc(right.final_sample or '')}</pre>"
                    "</div>"
                    "</div>"
                )
            elif best_cond:
                right = by[best_cond]
                examples.append(
                    f"<div class=\"muted\">INTERNAL</div><pre>{esc(right.internal_sample or '')}</pre>"
                    f"<div class=\"muted\" style=\"margin-top:8px\">FINAL</div><pre>{esc(right.final_sample or '')}</pre>"
                )

            other_details = []
            for c, v in by.items():
                if c in {base_cond, best_cond}:
                    continue
                other_details.append(
                    "<details>"
                    f"<summary>Example: <code>{esc(c)}</code></summary>"
                    f"<div class=\"muted\" style=\"margin-top:8px\">INTERNAL</div>"
                    f"<pre>{esc(v.internal_sample or '')}</pre>"
                    f"<div class=\"muted\" style=\"margin-top:8px\">FINAL</div>"
                    f"<pre>{esc(v.final_sample or '')}</pre>"
                    "</details>"
                )

            case_html.append(
                "<div class=\"case\">"
                f"<h3><code>{esc(cb.case)}</code></h3>"
                + (f"<div class=\"muted\" style=\"margin-top:6px\">{esc(cb.task)}</div>" if cb.task else "")
                + "<div style=\"margin-top:10px\"></div>"
                + case_table
                + "<details>"
                "<summary>Internal examples (baseline vs best balance)</summary>"
                + "".join(examples)
                + "".join(other_details)
                + "</details>"
                + "</div>"
            )

        report_cards.append(
            "<div class=\"card\">"
            f"<h2>{esc(r.label)}</h2>"
            f"<div class=\"muted\">Source: <code>{esc(r.path)}</code></div>"
            f"<div class=\"pills\">{''.join(pills)}</div>"
            "<div style=\"margin-top:12px\"></div>"
            + totals_table
            + "<div style=\"margin-top:12px\"></div>"
            + "<h2 style=\"margin-top:18px\">Prompts + per-case results</h2>"
            + "".join(case_html)
            + "</div>"
        )

    return f"""<!doctype html>
<html lang="en">
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
        <div class="sub">Generated {esc(now)} · One compiled page with prompts, results, examples, conclusions, and token amounts.</div>
      </div>
      {conclusions_html}
      {''.join(report_cards)}
      <div class="card">
        <h2>Notes</h2>
        <div class="muted">
          Metrics come from the saved markdown reports. “Compliance” is a simple format-adherence check; “Quality” is a lightweight proxy.
          For full methodology and the debate rounds, see <code>WORKFLOW.md</code> in the repo root.
        </div>
      </div>
    </div>
  </body>
</html>
"""


def _load_report(spec: str) -> Report:
    if "=" not in spec:
        raise SystemExit("Each --report must be LABEL=PATH")
    label, path = spec.split("=", 1)
    md = Path(path).read_text(encoding="utf-8")
    meta = _parse_meta(md)
    totals = _parse_summary_totals(md)
    cases = _parse_case_blocks(md)
    return Report(label=label.strip(), path=path.strip(), meta=meta, totals=totals, cases=cases)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--title", default="Agent-to-Agent Protocol Compression — Final Report")
    ap.add_argument("--report", action="append", default=[], help="Add a markdown report as LABEL=PATH. Can be repeated.")
    ap.add_argument("--output", default="docs/final_report.html")
    args = ap.parse_args()

    if not args.report:
        raise SystemExit("Provide at least one --report LABEL=PATH")

    reports = [_load_report(r) for r in args.report]
    html_out = render(reports, title=args.title)
    Path(args.output).write_text(html_out, encoding="utf-8")
    print(f"Wrote: {args.output}")


if __name__ == "__main__":
    main()
