# Round 5 Shared Evaluation Plan

Date: 2026-04-08
Scope: compare two new compression tracks against the existing benchmark line.

## Candidates to compare

1. `plain_english`
2. `RCCE-1`
3. `ATRCE-2`
4. `PCL-1` proto-language candidate
5. `SDC-1` semantically dense code candidate

## Shared benchmark suite

Use the same 7 benchmark cases already in `run_tests.py`:

1. `protocol_rule_proposal`
2. `missing_evidence_repair`
3. `fallback_trigger`
4. `benchmark_scope_decision`
5. `reference_clarity`
6. `scope_expansion`
7. `human_interrupt_during_execution`

The comparison only means anything if the task set stays fixed.

## Primary metrics

- internal token count
- protocol/code compliance
- repair turns
- final recommendation quality

## Additional diagnostic metrics for the new tracks

- free-English dependency
  - how much meaning still appears as normal English instead of code-native structure
- fallback frequency
  - whether the system wins only by escaping to English
- ambiguity pressure
  - whether dense forms trigger more clarification or weaker finals

## Decision criteria

`PCL-1` or `SDC-1` counts as a meaningful win only if it:

- beats `ATRCE-2` on internal token cost
- does not introduce obvious repair collapse
- preserves usable final recommendations
- remains coherent across all 7 cases, not just the easy ones

Practical target:

- internal tokens lower than `362`
- average repair at or near `ATRCE-2`
- final quality not materially below `2.3`

## Suggested run order

1. Generate `PCL-1` from the proto-language brief.
2. Generate `SDC-1` from the dense-code brief.
3. Encode both in `run_tests.py` as new benchmark conditions.
4. Add local sample outputs for both candidates.
5. Run local benchmark first for shape checking.
6. Run external model benchmarks after the local version is stable.

## Counting plan

- `claude` runner:
  - use estimated token counting unless true Anthropic usage data is available
- `codex` runner:
  - use exact OpenAI-style token counting when tokenizer support is available
- `local` runner:
  - use the same configured counting mode as a proxy benchmark

## Main comparison question

Which of the two new directions actually produces the better compression-to-reliability tradeoff:

- a more language-like compact system (`PCL-1`)
- a more codebook-like dense system (`SDC-1`)

This round should answer that empirically rather than by intuition.
