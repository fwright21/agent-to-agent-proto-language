# Agent-to-Agent Protocol Compression

why use many token when few token do trick — but for agent-to-agent coordination, not human prose

This repo explores whether multi-agent systems can coordinate with **much less INTERNAL text** while keeping FINAL output readable.

Every benchmark run forces this shape:

```text
INTERNAL:
agent coordination transcript, measured and compressed
FINAL:
human-facing recommendation, kept readable
```

## The story

Multi-agent workflows waste tokens on coordination overhead:

- repeating context
- hedging and politeness
- implicit disagreement that triggers repair turns

We want the same coordination functions — claim, objection, evidence, revision, next action — with fewer tokens.

So we treat coordination like an API: small vocabulary, explicit moves, benchmarked behavior.

## Before / after

Round 5 strict `missing_evidence_repair` INTERNAL sample.

Normal coordination:

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

Proto-language coordination, PCL-1:

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

Same moves. Less overhead.

## What we built

We built a protocol design + evaluation loop:

1) Debate: a “linguist panel” proposes and critiques protocol rules  
2) Spec: the winning idea becomes a concrete syntax and act inventory  
3) Benchmark: run the same case suite under each protocol and measure tokens, compliance, repairs, and a simple quality proxy  

## Linguist panel

The “linguists” are personas that protect different coordination properties:

- Chomsky: explicit structure, don’t hide dependencies
- Greenberg: irreducible coordination categories
- Sperber & Wilson: omit what is cheaply recoverable, avoid expensive inference
- Piantadosi: information per token, delete low-info overhead
- Bickerton: proto-grammar, stable roles, fragments ok
- Lakoff: strip framing and rhetoric
- Halliday: drop interpersonal stance, keep minimal cohesion
- Prince & Smolensky: explicit constraint ranking, recoverability > compression
- Jackendoff: preserve semantic mapping and reference clarity

Full persona descriptions: `01_linguist_agents.md`.

## Protocols tested

Baseline:
- `plain_english` readable internal chat, no protocol

Typed schemas:
- `RCCE-1` `TYPE: field=value; ...`
- `ATRCE-2` RCCE-1 + explicit `INTERRUPT` act + stricter rules

Proto-language:
- `PCL-1` act codes + positional args, `ACT ARG ARG ...`

Semantically dense code:
- `SDC-1` operator-prefixed code, `+c1 ...`, `-c1 ...`

## What happened in each round

High-level, no theory required:

- Round 1: define the goal (compress INTERNAL, keep FINAL readable) and sketch basic coordination moves.
  - Artifacts: `05_round_one_debate.md`, `02_message_types.md`
- Round 2: tighten message types and shared evaluation questions so protocols can be benchmarked instead of argued about.
  - Artifacts: `08_round_two_debate.md`, `02_shared_questions.md`
- Round 3: explore agent-role structure and synthesis patterns for protocol proposals.
  - Artifacts: `13_round_three_agents.md`, `14_round_three_debate.md`, `03_synthesis_template.md`
- Round 4: test “typed schema” coordination (RCCE-1 → ATRCE-2), learn that labels can cost more than they save, and that explicit `INTERRUPT` is a practical win.
  - Artifacts: `round_04_linguistic_revision_2026-04-08/`, `combined_round4_round5_dashboard.html`
- Round 5: test a proto-language (PCL-1) and a token-minimizing dense code (SDC-1), then measure the tradeoff frontier.
  - Artifacts: `round_05_proto_language_and_dense_code_2026-04-08/`, `round_05_proto_language_and_dense_code_2026-04-08/12_round5_codex_benchmark_report_r2_strict_repeats3.html`

## Results snapshot

Pulled from saved `openai_exact` reports in this repo.

Round 5 strict, Codex, repeats=3, `openai_exact`:
- `plain_english`: 946.3 avg INTERNAL tokens
- `PCL-1`: 524.3 avg INTERNAL tokens, 44.6% lower vs baseline, compliance 98.8%
- `SDC-1`: 406.7 avg INTERNAL tokens, 57.0% lower vs baseline, but quality dropped in strict runs

Round 4 Prompt 2, local, `openai_exact`:
- `plain_english`: 530 total INTERNAL tokens
- `RCCE-1`: 600 total INTERNAL tokens, worse than baseline
- `ATRCE-2`: 597 total INTERNAL tokens, worse than baseline

## Conclusions

- If you care about cost + still-working coordination: `PCL-1` is the current winner in this repo’s strict run.
- If you only care about the smallest token count: `SDC-1` wins tokens, but it is not the best single “default” protocol here (quality dropped in the suite).

## Reports and dashboards

GitHub shows `.html` files as source in the repo view. For publishable visuals, use GitHub Pages via `docs/`:

```bash
bash scripts/build_docs_site.sh
```

Then GitHub: Settings → Pages → deploy from `main` → `/docs`.

- Landing page: `docs/index.html`
- Trusted dashboard: `docs/dashboard_trusted.html`
- Round 5 strict report: `docs/round5_strict_r2.html`

## Run it yourself

Sanity check, no model calls:

```bash
python run_tests.py --runner local --output test_results.md
```

Live run, Codex:

```bash
python run_tests.py --runner codex --repeats 3 --count-mode auto --output test_results.md
```

Exact token counting:
- `--count-mode openai_exact` uses `tiktoken` via `requirements.txt`, Python >= 3.8

## Full writeup

For the detailed walkthrough, debates, protocol specs, reproduction, and discussion:
- `WORKFLOW.md`
