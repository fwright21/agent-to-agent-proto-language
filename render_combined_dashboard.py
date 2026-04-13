#!/usr/bin/env python3
"""
Render a small combined HTML dashboard that compares two run_tests.py markdown reports.

This intentionally stays lightweight: it reuses the markdown structure produced by run_tests.py
("## Summary Table" with "**TOTAL / AVG**" rows).
"""

import argparse
import datetime
import html
import re
from pathlib import Path


def _parse_kv_header(md_text):
    out = {}
    for key in [
        "Generated",
        "Runner",
        "Count mode",
        "Codex model",
        "Claude model",
        "Repeats per condition/case",
        "Baseline",
        "Conditions",
    ]:
        m = re.search(r"^" + re.escape(key) + r":\s*(.*)\s*$", md_text, flags=re.MULTILINE)
        if m:
            out[key] = m.group(1).strip()
    return out


def _parse_summary_table(md_text):
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
        rows.append(dict(zip(header, cols)))
    return rows


def _extract_totals(rows):
    out = []
    for r in rows:
        if r.get("Case") == "**TOTAL / AVG**":
            out.append(r)
    if not out:
        raise ValueError("Could not find TOTAL / AVG rows")
    return out


def _to_float(s):
    s = (s or "").strip().strip("*").replace("%", "")
    try:
        return float(s)
    except ValueError:
        return None


def _to_int(s):
    s = (s or "").strip().strip("*")
    try:
        return int(float(s))
    except ValueError:
        return None


def _slug(s):
    return re.sub(r"[^a-z0-9]+", "-", (s or "").lower()).strip("-") or "x"


def _render_totals_table(totals):
    # totals: list[dict] from summary table TOTAL/AVG rows
    columns = ["Condition", "Internal Tokens", "Compliance", "Repair Turns", "Final Quality"]
    ths = "".join(f"<th>{html.escape(c)}</th>" for c in columns)
    trs = []
    for t in totals:
        cond = t.get("Condition", "")
        tok = _to_int(t.get("Internal Tokens"))
        comp = _to_float(t.get("Compliance"))
        rep = _to_float(t.get("Repair Turns"))
        qual = _to_float(t.get("Final Quality"))
        trs.append(
            "<tr>"
            f"<td><code>{html.escape(cond)}</code></td>"
            f"<td>{'' if tok is None else tok}</td>"
            f"<td>{'' if comp is None else comp:.1f}%</td>"
            f"<td>{'' if rep is None else rep:.1f}</td>"
            f"<td>{'' if qual is None else qual:.1f}</td>"
            "</tr>"
        )
    return (
        "<table class=\"tbl\">"
        f"<thead><tr>{ths}</tr></thead>"
        f"<tbody>{''.join(trs)}</tbody>"
        "</table>"
    )


def render_dashboard(md_a, label_a, md_b, label_b, title):
    text_a = Path(md_a).read_text(encoding="utf-8")
    text_b = Path(md_b).read_text(encoding="utf-8")

    meta_a = _parse_kv_header(text_a)
    meta_b = _parse_kv_header(text_b)

    rows_a = _parse_summary_table(text_a)
    rows_b = _parse_summary_table(text_b)

    totals_a = _extract_totals(rows_a)
    totals_b = _extract_totals(rows_b)

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    def meta_block(meta):
        keys = ["Generated", "Runner", "Count mode", "Repeats per condition/case", "Baseline", "Conditions"]
        lis = []
        for k in keys:
            if k in meta:
                lis.append(f"<li><span class=\"k\">{html.escape(k)}:</span> <code>{html.escape(meta[k])}</code></li>")
        return "<ul class=\"meta\">" + "".join(lis) + "</ul>"

    css = """
    :root { --bg:#0b1220; --panel:#0f172a; --text:#e5e7eb; --muted:#94a3b8; --line:#22304a; --accent:#22c55e; --accent2:#60a5fa; --mono: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }
    body{ margin:0; font-family: Inter, system-ui, -apple-system, Segoe UI, Arial, sans-serif; background: radial-gradient(circle at 15% 10%, rgba(96,165,250,.18), transparent 35%), radial-gradient(circle at 85% 10%, rgba(34,197,94,.14), transparent 35%), var(--bg); color:var(--text); }
    .wrap{ max-width:1200px; margin:0 auto; padding:34px 20px 60px; }
    .hero{ background: linear-gradient(120deg, rgba(96,165,250,.22), rgba(34,197,94,.18)); border:1px solid rgba(255,255,255,.08); border-radius:18px; padding:18px 18px 16px; }
    h1{ margin:0; font-size:22px; letter-spacing:-.02em; }
    .sub{ margin-top:6px; color:var(--muted); font-size:13px; }
    .grid{ display:grid; grid-template-columns: 1fr 1fr; gap:16px; margin-top:16px; }
    .card{ background:rgba(15,23,42,.82); border:1px solid rgba(255,255,255,.08); border-radius:16px; padding:16px; }
    .card h2{ margin:0 0 10px; font-size:16px; }
    .meta{ margin:0 0 10px; padding-left:18px; color:var(--muted); font-size:12px; }
    .meta .k{ color:#cbd5e1; }
    code{ font-family: var(--mono); font-size: 12px; color: #e2e8f0; }
    .tbl{ width:100%; border-collapse: collapse; overflow:hidden; border-radius: 12px; }
    .tbl th, .tbl td{ border-bottom:1px solid rgba(255,255,255,.08); padding:10px 10px; text-align:left; font-size:13px; }
    .tbl th{ color:#cbd5e1; font-weight:600; background: rgba(255,255,255,.03); }
    .tbl td:nth-child(2){ font-variant-numeric: tabular-nums; }
    .footer{ margin-top:14px; color:var(--muted); font-size:12px; }
    a{ color: var(--accent2); text-decoration: none; }
    a:hover{ text-decoration: underline; }
    @media (max-width: 960px){ .grid{ grid-template-columns: 1fr; } }
    """

    def section(md_path, label, meta, totals):
        safe_id = _slug(label)
        return (
            f"<section class=\"card\" id=\"{safe_id}\">"
            f"<h2>{html.escape(label)}</h2>"
            f"<div class=\"sub\"><a href=\"{html.escape(md_path)}\">{html.escape(md_path)}</a></div>"
            f"{meta_block(meta)}"
            f"{_render_totals_table(totals)}"
            "</section>"
        )

    html_out = f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{html.escape(title)}</title>
  <style>{css}</style>
</head>
<body>
  <div class="wrap">
    <div class="hero">
      <h1>{html.escape(title)}</h1>
      <div class="sub">Generated {html.escape(now)} · Side-by-side totals/averages from two benchmark reports.</div>
    </div>

    <div class="grid">
      {section(md_a, label_a, meta_a, totals_a)}
      {section(md_b, label_b, meta_b, totals_b)}
    </div>

    <div class="footer">Note: this dashboard only compares the <code>**TOTAL / AVG**</code> rows; open the per-case reports for samples and details.</div>
  </div>
</body>
</html>
"""
    return html_out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("report_a_md")
    ap.add_argument("report_b_md")
    ap.add_argument("output_html")
    ap.add_argument("--label-a", default="Report A")
    ap.add_argument("--label-b", default="Report B")
    ap.add_argument("--title", default="Combined Benchmark Dashboard")
    args = ap.parse_args()

    out = render_dashboard(args.report_a_md, args.label_a, args.report_b_md, args.label_b, args.title)
    Path(args.output_html).write_text(out, encoding="utf-8")


if __name__ == "__main__":
    main()

