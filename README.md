# 🧠 Agent-to-Agent Protocol Compression
## A protocol benchmark for cheaper multi-agent coordination

I explored how to reduce token cost and improve reliability in multi-agent systems by structuring internal communication.

Core question:
Can we make AI agents coordinate more efficiently — without breaking coordination?

The goal is **not** to shorten answers for humans.
We focus on reducing **INTERNAL** agent-to-agent communication while keeping the final output readable.

Every benchmark run forces this shape:

```text
INTERNAL:
(agent coordination transcript — measured + compressed)
FINAL:
(human-facing recommendation — kept readable)
```

## 💡 The problem (in plain English)

When multiple AI agents work together, they often spend tokens on overhead:

- repeating context
- hedging and politeness (“maybe”, “I think”, etc.)
- back-and-forth repairs to resolve ambiguity

So the question is:
Can we give agents a structured way to communicate that is shorter, but still reliable?

That structure is what we call a **protocol**.

This is a promising direction, backed by benchmark runs, not a one-size-fits-all standard.

## 🧩 What’s a “protocol”?

A protocol is just a set of rules for how agents talk to each other.
Instead of full sentences, agents use predefined actions + compact formats.

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

## 👩‍💻 What do linguists do here?

The “linguists” are not just reviewers — they’re a design panel for communication itself.
They argue about what can be safely removed and what must stay explicit for coordination to work.

They operate as different personas, each protecting something important:
clarity, structure, efficiency, meaning, recoverability.

Full persona descriptions: `01_linguist_agents.md`.

## 🔁 How protocols are created

Each protocol goes through the same cycle:

1) Debate (linguist panel) → proposals + critique  
2) Specification → concrete syntax + rules  
3) Benchmarking → same tasks, measured outcomes  

We track:
token usage, formatting correctness (compliance), repair turns, and a simple final-quality proxy.

## 🧪 What we built

We built a protocol design + evaluation loop:

1) Debate: a “linguist panel” proposes and critiques protocol rules  
2) Spec: the winning idea becomes a concrete syntax and act inventory  
3) Benchmark: run the same case suite under each protocol and measure tokens, compliance, repairs, and a simple quality proxy  

## 🧪 What we tested

Baseline:
- `plain_english` readable internal chat, no protocol

Typed schemas:
- `RCCE-1` `TYPE: field=value; ...`
- `ATRCE-2` RCCE-1 + explicit `INTERRUPT` act + stricter rules

Proto-language:
- `PCL-1` act codes + positional args, `ACT ARG ARG ...`

Semantically dense code:
- `SDC-1` operator-prefixed code, `+c1 ...`, `-c1 ...`

## 🔁 Timeline (very short)

- R1–R3: define the benchmark scaffolding (moves, templates, failure modes).
- R4: test typed schemas (`RCCE-1`, `ATRCE-2`).
- R5: test compression frontier (`PCL-1`, `SDC-1`).

Details + artifacts live in `WORKFLOW.md`.

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

## 📊 Measurable impact (one strict run)

From Round 5 strict (Codex, repeats=3, `openai_exact`):
- `PCL-1`: ~45% fewer INTERNAL tokens vs `plain_english` (524.3 vs 946.3), with 98.8% compliance

## 👉 Takeaway

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
