# Round 4 Output Naming

Use separate files per prompt variant in this round folder.

## Prompt 1 (baseline in this round)
- `04_round4_debate_test_results_prompt1_baseline.md`
- `05_round4_benchmark_report_prompt1_baseline.html`

## Prompt 2 (next candidate)
- `07_round4_debate_test_results_prompt2.md`
- `08_round4_benchmark_report_prompt2.html`

## Commands

Run benchmark for prompt 2 (example):

```bash
python3 run_tests.py --runner local --repeats 3 --output round_04_linguistic_revision_2026-04-08/07_round4_debate_test_results_prompt2.md
```

Then produce prompt-2 HTML by copying and editing from prompt-1 HTML:

```bash
cp round_04_linguistic_revision_2026-04-08/05_round4_benchmark_report_prompt1_baseline.html \
   round_04_linguistic_revision_2026-04-08/08_round4_benchmark_report_prompt2.html
```
