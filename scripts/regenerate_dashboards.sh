#!/usr/bin/env bash
set -euo pipefail

# Regenerates HTML dashboards from the saved markdown reports.
#
# Note: by default, the repo keeps a small set of “shareable” HTML outputs.
# Larger / historical dashboards can be regenerated locally and are ignored by git.

python render_multi_dashboard.py \
  --title "Dashboard (Historical: mixed runs)" \
  --report "Round 4 Prompt 1 baseline (local, estimate)=round_04_linguistic_revision_2026-04-08/04_round4_debate_test_results_prompt1_baseline.md" \
  --report "Round 4 Prompt 2 (local, estimate)=round_04_linguistic_revision_2026-04-08/07_round4_debate_test_results_prompt2.md" \
  --report "Round 4 Prompt 2 (local, openai_exact)=round_04_linguistic_revision_2026-04-08/10_round4_debate_test_results_prompt2_openai_exact.md" \
  --report "Round 5 Codex r1 (repeats=1, openai_exact)=round_05_proto_language_and_dense_code_2026-04-08/07_round5_codex_results_r1.md" \
  --report "Round 5 Codex strict r1 (repeats=1, openai_exact)=round_05_proto_language_and_dense_code_2026-04-08/09_round5_codex_results_r1_strict.md" \
  --report "Round 5 Codex strict r2 (repeats=3, openai_exact)=round_05_proto_language_and_dense_code_2026-04-08/11_round5_codex_results_r2_strict_repeats3.md" \
  --output dashboard_historical.html

python render_multi_dashboard.py \
  --title "Dashboard (Trusted: openai_exact)" \
  --report "Round 4 Prompt 2 (local, openai_exact)=round_04_linguistic_revision_2026-04-08/10_round4_debate_test_results_prompt2_openai_exact.md" \
  --report "Round 5 Codex strict r2 (repeats=3, openai_exact)=round_05_proto_language_and_dense_code_2026-04-08/11_round5_codex_results_r2_strict_repeats3.md" \
  --output dashboard_trusted.html

python render_combined_dashboard.py \
  round_04_linguistic_revision_2026-04-08/10_round4_debate_test_results_prompt2_openai_exact.md \
  round_05_proto_language_and_dense_code_2026-04-08/11_round5_codex_results_r2_strict_repeats3.md \
  combined_round4_round5_dashboard.html \
  --label-a "Round 4 Prompt 2 (local, openai_exact)" \
  --label-b "Round 5 Codex strict (repeats=3, openai_exact)" \
  --title "Round 4+5 Combined Dashboard"

echo "Wrote: dashboard_historical.html, dashboard_trusted.html, combined_round4_round5_dashboard.html"
