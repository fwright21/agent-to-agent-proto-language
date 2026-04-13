#!/usr/bin/env bash
set -euo pipefail

# Builds a minimal GitHub Pages site into ./docs
# so HTML dashboards render as webpages on GitHub Pages.

mkdir -p docs

python render_final_report.py \
  --report "Round 4 typed schemas=round_04_linguistic_revision_2026-04-08/10_round4_debate_test_results_prompt2_openai_exact.md" \
  --report "Round 5 compression frontier=round_05_proto_language_and_dense_code_2026-04-08/11_round5_codex_results_r2_strict_repeats3.md" \
  --output docs/final_report.html

echo "Built docs site:"
ls -la docs | sed -n '1,200p'
