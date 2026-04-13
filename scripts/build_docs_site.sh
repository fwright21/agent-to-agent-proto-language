#!/usr/bin/env bash
set -euo pipefail

# Builds a minimal GitHub Pages site into ./docs
# so HTML dashboards render as webpages on GitHub Pages.

bash scripts/regenerate_dashboards.sh

mkdir -p docs

cp -f dashboard_trusted.html docs/dashboard_trusted.html
cp -f combined_round4_round5_dashboard.html docs/combined_round4_round5_dashboard.html

# Canonical Round 5 strict report (used by README/LinkedIn sharing)
cp -f \
  round_05_proto_language_and_dense_code_2026-04-08/12_round5_codex_benchmark_report_r2_strict_repeats3.html \
  docs/round5_strict_r2.html

echo "Built docs site:"
ls -la docs | sed -n '1,200p'
