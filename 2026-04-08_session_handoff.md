# Session Handoff — 2026-04-08

## Repository
- GitHub: `https://github.com/fwright21/agent-to-agent-proto-language`
- Branch: `main`

## Status (what’s pending)
Status: **Round 5 is complete locally, not yet committed/pushed**.

Where we left off:
- `PCL-1` and `SDC-1` benchmarked (strict Codex run)
- `PCL-1` = best compression candidate (~44% token savings) but has a compliance hole on `benchmark_scope_decision`
- `SDC-1` = most compressed (~51%) but quality too low (1.4)
- HTML report renderer upgraded with excerpts + savings tables

## What was completed

1. Round 4 workflow created in dedicated folder (no overwrites):
- `round_04_linguistic_revision_2026-04-08/01_round_brief_minimal.md`
- `round_04_linguistic_revision_2026-04-08/02_agents.md`
- `round_04_linguistic_revision_2026-04-08/03_debate.md`
- `round_04_linguistic_revision_2026-04-08/04_round4_debate_test_results_prompt1_baseline.md`
- `round_04_linguistic_revision_2026-04-08/05_round4_benchmark_report_prompt1_baseline.html`
- `round_04_linguistic_revision_2026-04-08/06_round4_output_naming.md`
- `round_04_linguistic_revision_2026-04-08/07_round4_debate_test_results_prompt2.md`
- `round_04_linguistic_revision_2026-04-08/08_round4_benchmark_report_prompt2.html`

2. Protocol naming updated across project language:
- `RCCE-1` = Relevance-Core Coordination English
- `ATRCE-2` = Act-Typed Relevance Coordination English

3. `README.md` updated:
- Removed origin/history filler sections
- Added methodology framing
- Added debate-system explanation

4. Benchmark harness `run_tests.py` updated:
- Supports 3 conditions: `plain_english`, `RCCE-1`, `ATRCE-2`
- Output display names are human-readable (`RCCE-1`, `ATRCE-2`)
- Summary wording fixed for 7-case suites

5. Prompt 2 report significantly expanded:
- Added richer visuals/structure inspired by `linguists_debate` report style
- Added explicit natural-language baseline comparison section
- Added more plain-English vs protocol examples
- Added token/cost table including natural-language baseline

6. Round 5 workflow added (proto-language + semantically dense code):
- `round_05_proto_language_and_dense_code_2026-04-08/01_round_brief_proto_language.md`
- `round_05_proto_language_and_dense_code_2026-04-08/02_round_brief_semantically_dense_code.md`
- `round_05_proto_language_and_dense_code_2026-04-08/03_shared_evaluation_plan.md`
- `round_05_proto_language_and_dense_code_2026-04-08/04_pcl_1_candidate.md` (PCL-1)
- `round_05_proto_language_and_dense_code_2026-04-08/05_sdc_1_candidate.md` (SDC-1)
- `round_05_proto_language_and_dense_code_2026-04-08/06_round5_local_results.md`
- `round_05_proto_language_and_dense_code_2026-04-08/07_round5_codex_results_r1.md`
- `round_05_proto_language_and_dense_code_2026-04-08/09_round5_codex_results_r1_strict.md`
- `round_05_proto_language_and_dense_code_2026-04-08/10_round5_codex_benchmark_report_r1_strict.html`

7. HTML report renderer upgraded to include excerpts + savings tables:
- `render_benchmark_html.py` now parses per-case `Internal sample` and `Final sample` blocks and renders:
  - `Representative Examples`
  - `What The Numbers Say`
  - `Token Savings And Scale-Up`
- Generated a standalone copy for quick opening:
  - `benchmark_report_round5_codex_strict.html`

## Latest benchmark snapshot (Prompt 2, Codex run)
Source: `round_04_linguistic_revision_2026-04-08/07_round4_debate_test_results_prompt2.md`

- `plain_english`: 556 tokens, repair 0.1, quality 2.4
- `RCCE-1`: 384 tokens, repair 0.4, quality 2.3
- `ATRCE-2`: 362 tokens, repair 0.0, quality 2.3

Interpretation:
- ATRCE-2 beats RCCE-1 on token cost and repairs in this benchmark run.
- Quality unchanged vs RCCE-1 in this run.

## Latest benchmark snapshot (Round 5, Codex strict run)
Source: `round_05_proto_language_and_dense_code_2026-04-08/09_round5_codex_results_r1_strict.md`

Count mode: `openai_exact` (tokenizer-native for OpenAI models)

- `plain_english`: 858 tokens, compliance 100%, repairs 0.1, quality 2.9 (baseline)
- `RCCE-1`: 863 tokens (worse than baseline), compliance 100%, repairs 0.1, quality 2.4
- `ATRCE-2`: 914 tokens (worse than baseline), compliance 100%, repairs 0.3, quality 3.0
- `PCL-1`: 482 tokens (43.8% lower), compliance 85.7%, repairs 0.1, quality 2.6
- `SDC-1`: 421 tokens (50.9% lower), compliance 100%, repairs 0.1, quality 1.4

Interpretation:
- Lowest tokens: `SDC-1` (saves 437 tokens per 7-case suite vs baseline) but quality is too low to recommend as-is.
- Best “usable” compression candidate: `PCL-1` (big savings, acceptable quality) but needs compliance hardening (one 0%-compliance case).
- In this strict run, the “best tradeoff” heuristic (compliance ≥ 90% and quality ≥ 2.0) selects `plain_english`.

## Compliance hardening (for PCL-1)
Goal: prevent “format misses” that score as 0% compliance even if reasoning is fine.

- Tighten output constraints: fixed number of lines, each line starts with an allowed tag (`CLM|OBJ|EVD|ASK|REV|CNF|NXT|ESC`), no extra prose/markdown/blank lines.
- Require stable IDs and references: e.g. `c1`, `e1` so validators can reliably connect moves to targets.
- Add a self-check + repair loop in the prompt: “validate against rules; if any rule fails, reprint corrected output only”.
- Add 1–2 few-shot examples specifically for the case that failed (in this run: `benchmark_scope_decision` for `PCL-1`).
- Optionally harden the validator: tolerate whitespace/casing if you care about semantics more than exact formatting; otherwise keep strict and rely on the self-check loop.

One-line takeaway: `SDC-1` is a token-minimizer but not a solution yet (quality too low); `PCL-1` is the best direction if compliance is made robust.

## Commits pushed in this session
- `ea34229` Round 4: add ATRCE-2 debate outputs, benchmark updates, and protocol naming
- `ac487e5` README: add methodology framing and debate system section
- `552919d` Round 4 report: expand natural-language comparisons and token-cost table

## Important caveat
- Round 4 Prompt 2 report uses estimated token counts (`ceil(word_count * 1.33)`), not tokenizer-native.
- Round 5 strict run uses tokenizer-native counts (`openai_exact`) and is the better source for token-savings claims.
- The compliance and “final quality” metrics are simplistic and can be gamed by format mistakes (e.g., a schema miss can produce 0% compliance even if the reasoning is fine).

## Pending tasks (open TODOs)

### Repo hygiene / completeness (as of 2026-04-12)
- [ ] Commit + push the Round 5 artifacts folder: `round_05_proto_language_and_dense_code_2026-04-08/`
- [ ] Commit + push report-rendering artifacts:
  - `render_benchmark_html.py`
  - `benchmark_report_round5_codex_strict.html`
  - `round_04_linguistic_revision_2026-04-08/09_round4_benchmark_report_prompt2_from_md.html`
- [ ] Commit + push the current `run_tests.py` changes (working tree is not clean).
- [ ] Decide whether generated HTML reports are “tracked outputs” (committed) or “build artifacts” (regenerated + ignored); make it consistent across rounds.
- [ ] Reconcile the git-state contradiction with `2026-04-08_round4_handoff_and_git_prep.md` (it states “not a git repo”, but this directory is a git repo with `origin` set).

### Benchmark next runs
- [ ] Add/confirm true token counting everywhere you report “tokens”:
  - Prefer tokenizer-native counting (`openai_exact` via `tiktoken`) when comparing OpenAI/Codex runs.
  - Keep `estimate` only as an explicitly-labeled fallback.
- [ ] Re-run Round 4 Prompt 2 benchmark using tokenizer-native counts and refresh:
  - `round_04_linguistic_revision_2026-04-08/07_round4_debate_test_results_prompt2.md`
  - `round_04_linguistic_revision_2026-04-08/08_round4_benchmark_report_prompt2.html`
- [ ] Re-run Round 5 with `repeats=3` and treat compliance deltas as unstable until replicated.

### Protocol work
- [ ] Harden `PCL-1` compliance on `benchmark_scope_decision` (the 0%-compliance case in the strict run) by adding a self-check/repair loop + 1–2 few-shot examples targeted to that case.
- [ ] (Optional) Add a portability run on a second backend (e.g., Claude) to see whether token-savings patterns/general compliance hold.
- [ ] (Optional) Produce a single dashboard HTML that compares Round 4 (RCCE-1 vs ATRCE-2) and Round 5 (PCL-1 vs SDC-1) under the same tokenization mode + metric definitions.

## Recommended next actions
1. Add true token-count mode (e.g., `tiktoken`) in `run_tests.py` with fallback to proxy.
2. Re-run Prompt 2 benchmark using true tokenization and refresh `07` + `08` files.
3. Optionally run second backend comparison (e.g., Claude) for portability check.
4. Produce a single “compare all 4 prompts” report that merges Round 4 (RCCE-1 vs ATRCE-2) with Round 5 (PCL-1 vs SDC-1) into one HTML dashboard.
5. Re-run Round 5 with `repeats=3` and fix `PCL-1` compliance on `benchmark_scope_decision` (the 0% case) before treating compliance as stable.

## Next actions (short list)
1. Fix `PCL-1` compliance on `benchmark_scope_decision`.
2. Re-run Round 5 with `repeats=3`.
3. Ensure `tiktoken`/tokenizer-native counts are used for “token” claims in `run_tests.py`.
4. Re-run Round 4 Prompt 2 benchmark with true tokenization.
5. Build a combined Round 4+5 HTML dashboard.
