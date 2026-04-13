# Contributing

## Quickstart

1) Run a no-network sanity check (uses stored local samples):

```bash
python run_tests.py --runner local --output test_results.md
```

2) Render HTML for sharing:

```bash
python render_benchmark_html.py test_results.md benchmark_report.html
```

3) Regenerate the repo dashboards from saved markdown reports:

```bash
bash scripts/regenerate_dashboards.sh
```

## Token counting

- `--count-mode estimate` is a heuristic comparison metric.
- `--count-mode openai_exact` uses `tiktoken` when installed (see `requirements.txt`) and is the preferred mode for quoting “tokens” in writeups.

## Adding a new protocol condition

1) Add a new entry in `CONDITIONS` in `run_tests.py`.
2) Add a display label in `CONDITION_DISPLAY`.
3) If the condition has a strict line format, add:
   - a line validator, and
   - a compliance function in `compliance_for_condition`.
4) Update `LOCAL_SAMPLES` so `--runner local` stays deterministic.

## Adding a new benchmark case

1) Add a new case entry to `CASES` in `run_tests.py` with a stable `label`.
2) Add samples for each condition in `LOCAL_SAMPLES`.
3) Regenerate `benchmark_report.html` and the dashboards, and keep the markdown report(s) that back any published claims.

