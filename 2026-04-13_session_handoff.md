# Session Handoff — 2026-04-13

## 0) What this project is (one paragraph)

This repo is a small research/engineering project about **making multi-agent coordination cheaper**. The target is not “shorter answers to humans”. The target is **shorter INTERNAL agent-to-agent conversation** while keeping coordination reliable (claims, objections, evidence, revisions, next actions) and keeping the human-facing output readable.

Every benchmark run forces this shape:

```text
INTERNAL:
(agent coordination transcript — measured + compressed)
FINAL:
(human-facing recommendation — kept readable)
```

---

## 1) What changed in this session (2026-04-13)

### 1.1 GitHub-facing docs were upgraded

- `README.md` was rewritten to be a comprehensive “project homepage” narrative:
  - project goal and INTERNAL vs FINAL framing
  - linguist-panel methodology (debate → spec → benchmark)
  - protocols tested, including tradeoffs and “unsuccessful directions”
  - round-by-round summary
  - strict-run results with concrete numbers
  - one “before vs after” internal-sample example (plain English vs PCL-1)
- `WORKFLOW.md` is now the canonical long-form writeup (moved from `WORKFLOW_REPORT.md`), and includes a repo map and artifact policy.
- `CONTRIBUTING.md` was added with “how to run”, “how to add a protocol”, and “how to add a benchmark case”.

### 1.2 Dashboards and rendering got more usable

- `render_multi_dashboard.py` got UX improvements:
  - sticky toolbar
  - filter-by-label
  - jump links to reports
  - expand/collapse examples
- `scripts/regenerate_dashboards.sh` was added so dashboards are regenerated from saved markdown reports with one command.

### 1.3 Artifact policy was clarified

- The repo checks in a small set of “shareable” HTML outputs:
  - `dashboard_trusted.html`
  - `combined_round4_round5_dashboard.html`
- Larger or mixed historical HTML outputs are meant to be regenerated locally and are ignored by git:
  - `dashboard_historical.html`
  - `benchmark_report_round5_codex_strict.html`
- `.codex_tmp/` remains ignored (Codex last-message capture directory).

### 1.4 Token counting clarity improved

- `run_tests.py` now prints a clearer warning when `--count-mode openai_exact` is requested but `tiktoken` is unavailable, and falls back to `estimate`.
- `requirements.txt` was added to document the intended dependency (`tiktoken` requires Python >= 3.8).

### 1.5 Git status contradiction was reconciled

- `2026-04-08_round4_handoff_and_git_prep.md` was corrected to note that the repo *is* a git repo now.

---

## 2) What’s now on GitHub

Two commits were pushed to `origin/main`:

- `0252301` — Docs + dashboards: comprehensive README/workflow
- `e46b5cd` — Polish README structure and linguist detail

If anything looks “missing” on GitHub, check whether it was intentionally ignored by `.gitignore` (historical dashboards) or is intended to be regenerated locally.

---

## 3) How to reproduce (copy/paste)

Sanity check (no model calls; uses local stored outputs):

```bash
python run_tests.py --runner local --output test_results.md
```

Live run with Codex:

```bash
python run_tests.py --runner codex --repeats 3 --count-mode auto --output test_results.md
```

Regenerate the repo’s main dashboards from saved markdown reports:

```bash
bash scripts/regenerate_dashboards.sh
```

---

## 4) Remaining TODOs (the “real work” left)

### 4.1 PCL-1 brittleness hardening

Known weakness from strict runs: compact formats amplify small mistakes (missing an argument) into non-compliance and repair. Next step is to harden PCL-1 on the weaker cases by:

- stronger self-check/repair loop in the prompt
- tighter id/topic conventions and stable reference patterns
- (optional) a targeted few-shot example for the weakest case

### 4.2 Token counting portability

In this environment, `tiktoken` was not installed, so `openai_exact` counting cannot be reproduced locally without upgrading to Python >= 3.8 and installing deps.

### 4.3 Benchmark expansion

Add 1–2 more realistic coordination cases (PR review, incident triage) to stress:

- interrupts
- reference clarity
- “repair cancels savings” scenarios

### 4.4 Presentation improvements

If you want dashboards to render directly in GitHub, consider GitHub Pages (otherwise GitHub shows HTML as source; local browser open works fine).

