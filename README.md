# 🧠 Agent-to-Agent Protocol Compression
## A benchmark for cheaper, more reliable multi-agent coordination

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

That structure is a **structured coordination format**.

This is a promising direction, backed by benchmark runs, not a one-size-fits-all standard.

## 👩‍💻 Linguistic methodology (how protocols are designed)

Protocols are designed via a “linguist panel” debate loop:

1) Debate: personas argue about what must stay explicit for coordination (reference clarity, recoverability, information density).  
2) Spec: the winning idea becomes a concrete set of actions + formatting rules.  
3) Benchmark: we run the same tasks and measure tokens, compliance, repair turns, and final output quality.  

The point is to make tradeoffs measurable, not ideological.

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
- `plain_english` readable internal chat, no format constraints

Typed schemas:
- `RCCE-1` `TYPE: field=value; ...`
- `ATRCE-2` RCCE-1 + explicit `INTERRUPT` act + stricter rules

Compact coordination format:
- `PCL-1` act codes + positional args, `ACT ARG ARG ...`

Semantically dense code:
- `SDC-1` operator-prefixed code, `+c1 ...`, `-c1 ...`

## 📊 Results (evidence)

From the saved benchmark reports in this repo, the results from each protocol are:

- `plain_english`: 946.3 avg INTERNAL tokens
- `RCCE-1`: 889.3 avg INTERNAL tokens
- `ATRCE-2`: 895.3 avg INTERNAL tokens
- `PCL-1`: 524.3 avg INTERNAL tokens, 98.8% compliance
- `SDC-1`: 406.7 avg INTERNAL tokens (but quality dropped in the suite)

Final results page (GitHub Pages): `docs/final_results.html`

## 👉 Takeaway

- If you care about cost + still-working coordination: `PCL-1` is the current winner in this repo’s strict run.
- If you only care about the smallest token count: `SDC-1` wins tokens, but it is not the best single “default” protocol here (quality dropped in the suite).

## Before / after (example)

Normal coordination:

```text
AgentA: I claim this reduces internal tokens by ~30% across tasks.
AgentB: Please provide evidence and clarify scope.
AgentC: In our test set we saw closer to ~12%, not 30%.
AgentA: OK — revising the claim to ~12%.
```

Compressed coordination (PCL-1):

```text
CLM AgentA comp_all+30%
ASK AgentB evd? scope?
EVD AgentC testset=bench01 gain=12% not 30
REV AgentA comp_all+12%
```

Expanded (debug view):

```text
CLM AgentA comp_all+30% -> Claim: “~30% across tasks”
REV AgentA comp_all+12% -> Revise: “~12% on test set”
```

## Reports and dashboards

GitHub shows `.html` files as source in the repo view. For publishable visuals, use GitHub Pages via `docs/`:

```bash
bash scripts/build_docs_site.sh
```

Then GitHub: Settings → Pages → deploy from `main` → `/docs`.

- Landing page: `docs/index.html`
- Final results: `docs/final_results.html`

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

If you want the deeper dive:
- Protocol specs + personas: `01_linguist_agents.md`, `02_message_types.md`, `03_protocol_examples.md`
- Benchmark suite + cases: `10_benchmark_suite.md`, `11_benchmark_cases.md`
- Round artifacts: `round_04_linguistic_revision_2026-04-08/`, `round_05_proto_language_and_dense_code_2026-04-08/`
