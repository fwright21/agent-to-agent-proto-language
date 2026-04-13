# Agent-to-Agent Compressed Communication (Protocol + Benchmark)

This repo is a small research/engineering project about **making multi-agent coordination cheaper**.
The target is not “shorter answers to humans”. The target is **shorter INTERNAL agent-to-agent conversation** while keeping coordination reliable (claims, objections, evidence, revisions, next actions) and keeping the human-facing output readable.

Every benchmark run forces this shape:

```text
INTERNAL:
(agent coordination transcript — measured + compressed)
FINAL:
(human-facing recommendation — kept readable)
```

## Why this exists (one paragraph)

Multi-agent workflows often spend a large share of tokens on coordination overhead: repeating context, hedging, politeness, and implicit/ambiguous disagreements that trigger repair turns.
This project tests whether a **coordination protocol** (a constrained language for internal moves) can cut INTERNAL tokens without collapsing reliability.

## Methodology (linguistics → spec → benchmark)

Protocol candidates are generated with a “linguist panel” debate loop, then adjudicated by benchmarks:

1) Debate (ideation): personas argue about **recoverability**, **inferential load**, and **speech acts** (e.g., “interrupt” vs “ask”).  
2) Spec (formalization): the winning idea becomes a concrete protocol (syntax + allowed acts).  
3) Benchmark (decision): run the same task suite under each protocol and measure:
   - INTERNAL token cost
   - compliance (format adherence)
   - repair turns (ASK/ESC patterns)
   - final quality (simple proxy)

## Protocols tested (including “unsuccessful” directions)

Baseline:
- `plain_english`: readable internal chat, no protocol.

Typed schemas (readable + easy to validate, but label overhead can be expensive):
- `RCCE-1`: Relevance-Core Coordination English (`TYPE: field=value; ...`)
- `ATRCE-2`: RCCE-1 + explicit `INTERRUPT` act + stricter usage rules

Proto-language (best current savings/tradeoff candidate):
- `PCL-1`: act codes + positional args (`ACT ARG ARG ...`) to remove label overhead while keeping coordination functions

Semantically dense code (token-minimizer, quality risk):
- `SDC-1`: operator-prefixed code (`+c1 ...`, `-c1 ...`), cheapest but can become too cryptic

## What happened in each round (high level)

Round 4 (typed schema track):
- Goal: make coordination moves explicit and validator-friendly.
- Key finding: typed fields can be **more expensive than plain English** for short messages; label overhead is real.
- Key improvement: introducing explicit **speech acts** (especially interrupts) reduces ambiguity-driven repair.

Round 5 (compression frontier):
- Proto-language track (PCL-1): remove repeated field labels while keeping act structure.
- Dense code track (SDC-1): push compression further; observed quality drop in strict runs.

## Results (numbers worth quoting)

From saved strict exact-count runs (tokenizer-native counting for OpenAI models):
- PCL-1 substantially reduces INTERNAL tokens vs plain English, while remaining mostly compliant.
- SDC-1 is cheapest on tokens, but quality can drop.

For the exact runs + tables, open:
- `dashboard_trusted.html` (only openai_exact runs)
- `combined_round4_round5_dashboard.html` (Round 4 vs Round 5 side-by-side)

## Runners / “models tested”

The harness supports:
- `--runner local`: deterministic stored samples (no network; sanity check)
- `--runner codex`: live run via `codex exec`
- `--runner claude`: live run via `claude -p`

Exact token counting:
- `--count-mode openai_exact` uses `tiktoken` when installed (see `requirements.txt`; requires Python >= 3.8).
- If `tiktoken` is unavailable, the harness falls back to an explicit heuristic estimate (still useful for relative comparisons, but not billable tokens).

## How to run

Sanity check (no model calls; uses stored local outputs):

```bash
python run_tests.py --runner local --output test_results.md
```

Live run (Codex):

```bash
python run_tests.py --runner codex --repeats 3 --count-mode auto --output test_results.md
```

Render an HTML report from a markdown report:

```bash
python render_benchmark_html.py test_results.md benchmark_report.html
```

Regenerate the repo’s main dashboards:

```bash
bash scripts/regenerate_dashboards.sh
```

This repo checks in a small set of “shareable” HTML outputs (trusted + combined). Larger/historical dashboards are regenerated locally.

## Full writeup

For the detailed “GitHub-level” walkthrough (debates, linguists, protocol specs, exact reproduction, and discussion), see:
- `WORKFLOW.md`
