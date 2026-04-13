# Handoff + Git Prep (2026-04-08)

## Current status

Round 4 debate and benchmark flow are complete.

Protocol naming is now linguist-based:
- `RCCE-1` = Relevance-Core Coordination English
- `ATRCE-2` = Act-Typed Relevance Coordination English

## Round 4 outputs (new folder, no overwrite strategy)

Folder:
- `round_04_linguistic_revision_2026-04-08/`

Key files:
- `01_round_brief_minimal.md`
- `02_agents.md`
- `03_debate.md` (includes synthesized ATRCE-2 candidate)
- `04_round4_debate_test_results_prompt1_baseline.md`
- `05_round4_benchmark_report_prompt1_baseline.html`
- `06_round4_output_naming.md`
- `07_round4_debate_test_results_prompt2.md`
- `08_round4_benchmark_report_prompt2.html`

## Benchmark result snapshot (Prompt 2 run)

Source: `round_04_linguistic_revision_2026-04-08/07_round4_debate_test_results_prompt2.md`

Totals / averages:
- `plain_english`: 556 internal tokens, 100% compliance, 0.1 repair turns, 2.4 final quality
- `RCCE-1`: 384 internal tokens, 100% compliance, 0.4 repair turns, 2.3 final quality
- `ATRCE-2`: 362 internal tokens, 100% compliance, 0.0 repair turns, 2.3 final quality

Interpretation:
- ATRCE-2 beats RCCE-1 on token cost and repair turns in the local benchmark.
- Final quality is unchanged vs RCCE-1 in this local run.

## Non-round files updated

- `README.md`
  - removed low-priority historical/origin text
  - added protocol-name rationale (`Relevance-Core`, `Act-Typed`)
- `run_tests.py`
  - added third condition (ATRCE-2)
  - generalized reporting for multi-condition comparisons
  - fixed 7-case suite wording
  - display labels now show `RCCE-1` / `ATRCE-2` in output
- `11_benchmark_cases.md`
  - added `human_interrupt_during_execution`

## Git repo state

Update (2026-04-13): this directory **is** a git repository now (there is a `.git/` folder and an `origin` remote is configured).

Check used:
- At the time this handoff was written, `git rev-parse --is-inside-work-tree` returned `not-git-repo`.
- Today you can confirm with: `git rev-parse --is-inside-work-tree` and `git remote -v`.

## Prepare to save to git

### 1) Initialize repo

```bash
git init
```

### 2) Optional: set default branch

```bash
git branch -M main
```

### 3) Add all files

```bash
git add .
```

### 4) First commit (single commit path)

```bash
git commit -m "Round 4 debate, ATRCE-2 benchmark, and protocol naming update"
```

## Suggested commit split (clean history)

If you prefer multiple commits:

1. Round artifact scaffolding + debate docs
- `round_04_linguistic_revision_2026-04-08/01_*.md`
- `round_04_linguistic_revision_2026-04-08/02_*.md`
- `round_04_linguistic_revision_2026-04-08/03_*.md`

2. Benchmark harness and case updates
- `run_tests.py`
- `11_benchmark_cases.md`

3. Generated round results
- `round_04_linguistic_revision_2026-04-08/04_*`
- `round_04_linguistic_revision_2026-04-08/05_*`
- `round_04_linguistic_revision_2026-04-08/07_*`
- `round_04_linguistic_revision_2026-04-08/08_*`

4. Naming + README cleanup
- `README.md`
- `02_message_types.md`
- `benchmark_report.html`
- `2026-04-08_round4_handoff_and_git_prep.md`

## Optional next step after init

If you want, next action is:
1. run `git init`
2. I will stage by commit group and give you exact commit commands/messages.
