# Session Handoff — 2026-04-08

## Project
Agent-to-agent compressed communication / proto-language work in `/Users/francescawright/Documents/Agent_to_agent_compressed_communication_proto_language`.

## Goal of this phase
1. Fork the original linguistics-driven prompt compression project into a new project focused on internal agent coordination.
2. Keep the debate structure, but change the design target from final-answer compression to compressed agent-to-agent protocols.
3. Define the first protocol candidate, benchmark tasks, and harness.
4. Record the benchmark and reporting work in token terms, not word terms.

## Status: BENCHMARK AND REPORTING UPDATED

## What is now done
- Created the new sibling project folder:
  - `/Users/francescawright/Documents/Agent_to_agent_compressed_communication_proto_language`
- Reframed the project around a new core question:
  - can a constrained coordination protocol reduce multi-agent communication cost without materially hurting reliability or final recommendation quality?
- Updated the top-level project framing in:
  - `README.md`
  - `00_project_scope.md`
  - `00_debate_method.md`
  - `02_shared_questions.md`
  - `04_benchmark_plan.md`
  - `04_better_than_caveman_criteria.md`
  - `06_live_debate_template.md`

## New protocol-design files added
- `01_agent_protocol_hypothesis.md`
- `02_message_types.md`
- `03_protocol_examples.md`
- `05_failure_modes.md`
- updated benchmark scaffolding in:
  - `10_benchmark_suite.md`
  - `11_benchmark_cases.md`

## Current protocol candidate
Protocol name:
- `Relevance-Core Coordination English (RCCE-1)`

Current message types:
- `CLAIM`
- `EVID`
- `OBJ`
- `REV`
- `ASK`
- `CONF`
- `NEXT`
- `ESCALATE`

Current design principles:
- one message, one purpose
- one line per message
- fixed required fields by message type
- explicit references via `id` / `target`
- use `ESCALATE` instead of unsafe freeform compression
- controlled English, not a fully symbolic language

## Debate structure decision
Yes, the linguists still debate.

But the debate target is now:
- what must remain explicit in agent coordination
- what can be compressed safely
- where inferential omission is acceptable
- when fallback to plain language is necessary

Current conceptual role mapping in `01_linguist_agents.md`:
- Chomsky: protects structural relations
- Greenberg: identifies irreducible coordination categories
- Sperber & Wilson: justify omission of cheaply recoverable context
- Piantadosi: removes low-information overhead
- Bickerton: pushes proto-grammar reduction
- Lakoff: strips framing language
- Halliday: removes interpersonal function, preserves necessary cohesion
- Prince & Smolensky: frames tradeoffs as ranked constraints
- Jackendoff: preserves semantic mapping and reference clarity

Recommended first live debate panel:
- Chomsky
- Sperber & Wilson
- Bickerton
- Lakoff

## Benchmark design now in place
The first benchmark is no longer about user-facing answer brevity.

It now compares:
1. `plain_english`
2. `RCCE-1`

The benchmark focuses on internal coordination cost and reliability, not caveman-style final output compression.

### Benchmark cases
Defined in `11_benchmark_cases.md`:
- `protocol_rule_proposal`
- `missing_evidence_repair`
- `fallback_trigger`
- `benchmark_scope_decision`
- `reference_clarity`
- `scope_expansion`

### Intended metrics
- estimated internal token count
- protocol compliance rate
- repair turns
- final recommendation quality

## Harness status
`run_tests.py` in the new project has been replaced with a coordination benchmark harness.

It now:
- compares `plain_english` vs `RCCE-1`
- runs the six benchmark cases above
- asks the selected runner to simulate a 4-agent exchange
- parses output into:
  - `INTERNAL:` section
  - `FINAL:` section
- computes:
  - average internal token count
  - protocol compliance percentage
  - repair-turn count
  - simple final-quality score
- estimates Claude Sonnet 4 output-cost savings using `$15 / MTok` as the guideline
- writes results to `test_results.md`

### Validation completed
- `python3 -m py_compile run_tests.py`
- `python3 run_tests.py --help`
- `python3 run_tests.py --runner local --repeats 3`

### Current results
The latest local six-case benchmark completed successfully.

Summary:
- `plain_english`: `486` estimated tokens total, `100%` compliance, `0.2` average repair turns, `2.5` average final quality
- `RCCE-1`: `322` estimated tokens total, `100%` compliance, `0.3` average repair turns, `2.3` average final quality
- token savings: `164` estimated tokens per six-case suite
- relative reduction: `33.7%`

Scale-up estimate:
- 10 suites: `1,640` tokens saved
- 100 suites: `16,400` tokens saved
- 1,000 suites: `164,000` tokens saved

Claude Sonnet 4 cost guideline:
- using `$15 / MTok` output pricing, the savings are about `$0.00246` per six-case suite if internal token savings map roughly to output tokens
- that scales to about `$2.46` per `1,000` suites

### Remaining caveat
This is still a local fallback benchmark, not a live external Codex/Claude backend run. The token-saving signal is useful, but it is not final proof of production behavior.

## Important framing decisions
- keep the debate architecture as the ideation engine
- treat the benchmark as the evidence layer
- do not oversell this as a general machine language
- first benchmark should stay narrow and structured
- optimize for token savings-to-reliability ratio, not shortest possible strings
- report metrics in estimated tokens and Claude pricing terms, not word counts

## Main risks identified
- protocol becomes too cryptic and loses reliability
- agents drift out of schema into prose
- repair traffic erases the savings
- schema too rigid for nuance
- missing references break coordination
- token savings may not hold under a real external model run
- quality may dip as coordination gets more compressed

## Current safeguards
- tiny message vocabulary
- fixed fields
- controlled English inside `content=` values
- explicit fallback via `ESCALATE`
- benchmark compliance directly rather than assuming it
- local fallback path for benchmarking when external runner access is unavailable
- token-based cost estimates tied to Claude Sonnet 4 pricing for scale intuition

## Best next steps
1. If desired, rerun the benchmark with a real Codex backend once the CLI connectivity issue is resolved.
2. Add a second protocol variant and compare:
   - perhaps a looser controlled-English variant
   - or a more compressed symbolic variant
3. Expand the report with a token-cost table that shows the savings under other Anthropic models if needed.
4. After that, run the first actual linguist debate to generate protocol alternatives against the benchmark rather than in the abstract.
5. Only later add the 2x2 expansion:
   - plain coordination + plain final answer
   - plain coordination + compressed final answer
   - protocol coordination + plain final answer
   - protocol coordination + compressed final answer

## How to resume quickly
- Open `README.md` for the project framing.
- Open `02_message_types.md` for the current protocol schema.
- Open `11_benchmark_cases.md` for the benchmark tasks.
- Open `run_tests.py` for the benchmark harness.
- Open `test_results.md` for the current token-based results.
- Open `benchmark_report.html` for the rendered report with methodology, debate history, token savings, and scale-up estimates.
