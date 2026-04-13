# Agent-to-Agent Compressed Communication: Protocol Benchmark

This repo is a small research/engineering project about **making multi-agent coordination cheaper**.
The target is not “shorter answers to humans”. The target is **shorter INTERNAL agent-to-agent conversation** while keeping coordination reliable: claims, objections, evidence, revisions, and next actions. The human-facing output stays readable.

Every benchmark run forces this shape:

```text
INTERNAL:
agent coordination transcript, measured and compressed
FINAL:
human-facing recommendation, kept readable
```

## Why this exists

Multi-agent workflows often spend a large share of tokens on coordination overhead: repeating context, hedging, politeness, and implicit/ambiguous disagreements that trigger repair turns.
This project tests whether a **coordination protocol**, a constrained language for internal moves, can cut INTERNAL tokens without collapsing reliability.

## Methodology: linguistics → spec → benchmark

Protocol candidates are generated with a “linguist panel” debate loop, then adjudicated by benchmarks:

1) Debate: personas argue about recoverability, inferential load, and speech acts, for example “interrupt” vs “ask”.  
2) Spec: the winning idea becomes a concrete protocol with syntax and allowed acts.  
3) Benchmark: run the same task suite under each protocol and measure:
   - INTERNAL token cost
   - compliance, format adherence
   - repair turns, ASK/ESC patterns
   - final quality, simple proxy

## Protocols tested: including “unsuccessful” directions

Baseline:
- `plain_english`: readable internal chat, no protocol.

Typed schemas: readable and easy to validate, but label overhead can be expensive
- `RCCE-1`: Relevance-Core Coordination English. Example: `TYPE: field=value; ...`
- `ATRCE-2`: RCCE-1 + explicit `INTERRUPT` act + stricter usage rules

Proto-language: best current savings/tradeoff candidate
- `PCL-1`: act codes + positional args. Example: `ACT ARG ARG ...`

Semantically dense code: token-minimizer, quality risk
- `SDC-1`: operator-prefixed code. Example: `+c1 ...`, `-c1 ...`

## Linguist panel: personas and what they protect

The “linguists” are used as *personas* that defend different coordination properties. In practice, they push the protocol design toward a stable set of tradeoffs:

- Structural minimalism, Chomsky: preserve explicit structure so targets, dependencies, and revisions stay legible.
- Universals, Greenberg: keep a tiny “irreducible” inventory of coordination functions that cannot disappear.
- Inferential pragmatics, Sperber & Wilson: omit what shared context makes cheaply recoverable, but avoid pushing inference cost so high that repair explodes.
- Information density, Piantadosi: delete low-information overhead first; retain tokens that prevent expensive ambiguity.
- Protolanguage, Bickerton: argue for stable proto-grammar and fragments as long as roles remain clear.
- Framing, Lakoff: strip rhetorical packaging that helps humans but not machine coordination.
- Functional roles, Halliday: zero out interpersonal language; keep minimal cohesion where it supports multi-turn coordination.
- Constraint ranking, Prince & Smolensky: force explicit priority ordering, usually recoverability > compression > stylistic naturalness.
- Parallel architecture, Jackendoff: preserve semantic mapping and reference clarity, not just surface form.

Full persona descriptions live in `01_linguist_agents.md`.

## What happened in each round

Round 4: typed schema track
- Goal: make coordination moves explicit and validator-friendly.
- Key finding: typed fields can be **more expensive than plain English** for short messages; label overhead is real.
- Key improvement: introducing explicit **speech acts**, especially interrupts, reduces ambiguity-driven repair.

Round 5: compression frontier
- Proto-language track, PCL-1: remove repeated field labels while keeping act structure.
- Dense code track, SDC-1: push compression further; observed quality drop in strict runs.

## Results: strict tokenizer-native runs

These are pulled from saved `openai_exact` reports in this repo.

Round 4 Prompt 2, local, `openai_exact`:
- `plain_english`: 530 total INTERNAL tokens
- `RCCE-1`: 600 total INTERNAL tokens, worse than baseline
- `ATRCE-2`: 597 total INTERNAL tokens, worse than baseline

Round 5 strict, Codex, repeats=3, `openai_exact`:
- `plain_english`: 946.3 avg INTERNAL tokens
- `PCL-1`: 524.3 avg INTERNAL tokens, 44.6% lower vs baseline, compliance 98.8%
- `SDC-1`: 406.7 avg INTERNAL tokens, 57.0% lower vs baseline, quality drop risk

For the exact runs + tables, open:
- `dashboard_trusted.html` only openai_exact runs
- `combined_round4_round5_dashboard.html` Round 4 vs Round 5 side-by-side

## Before and after: one benchmark case

Round 5 strict `missing_evidence_repair` INTERNAL samples:

Plain English:

```text
AgentA: I claim this compression scheme reduces message sizes by 80% across all tasks.
AgentB: Please provide evidence or data to support that claim.
AgentC: We ran a small pilot on 30 transcripts and saw an average 35% reduction; no evidence of 80% across all tasks.
AgentD: Confidence: low on the 80% claim, moderate on a 30–40% range given the pilot.
AgentA: Based on the pilot, I revise the claim to 35% average reduction on the sampled transcripts.
AgentB: That revision is supported by the pilot summary.
AgentC: Agree to revise; the original claim is unsupported.
AgentD: Final decision should be revise, not keep.
```

PCL-1:

```text
CLM AgentA comp_all+30%
ASK AgentB evd? scope?
EVD AgentC testset=bench01 n=50 gain=12% not 30
CNF AgentD conf=low
REV AgentA comp_all+12%
NXT AgentB decide keep_rev
CNF AgentC conf=med
NXT AgentD decision=revise
```

## Models and runners tested

The harness supports:
- `--runner local`: deterministic stored samples, no network, sanity check
- `--runner codex`: live run via `codex exec`
- `--runner claude`: live run via `claude -p`

Exact token counting:
- `--count-mode openai_exact` uses `tiktoken` when installed. See `requirements.txt`. Requires Python >= 3.8.
- If `tiktoken` is unavailable, the harness falls back to an explicit heuristic estimate. Useful for relative comparisons, not billable tokens.

Model selection:
- `--codex-model` sets `codex exec -m ...`
- `--claude-model` sets `claude --model ...`

## How to run

Sanity check, no model calls, uses stored local outputs:

```bash
python run_tests.py --runner local --output test_results.md
```

Live run, Codex:

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

This repo checks in a small set of “shareable” HTML outputs: trusted + combined. Larger/historical dashboards are regenerated locally.

## Full writeup

For the detailed “GitHub-level” walkthrough, debates, linguists, protocol specs, exact reproduction, and discussion, see:
- `WORKFLOW.md`
