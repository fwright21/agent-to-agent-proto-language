# Agent-to-Agent Compressed Communication / Proto-Language

## Goal

This project asks:
- how do we make agents communicate with each other more cheaply during collaboration?

The core hypothesis is that agent-to-agent communication does not need full natural-language English. It may be possible to replace ordinary internal discussion with a compact, structured coordination protocol that preserves reliability while reducing token cost.

## Working idea

Human-facing answers need readability.

Agent-facing messages need:
- clear state transfer
- compact disagreement
- evidence references
- explicit next actions
- low ambiguity

That suggests a controlled protocol may outperform freeform English in multi-agent settings.

## What this project will test

The benchmark should compare at least two coordination styles:

1. Plain-English internal discussion
   - agents talk to each other normally
   - no compression protocol

2. Compressed coordination protocol
   - agents use a constrained message format
   - small vocabulary
   - fixed fields
   - controlled English rather than free prose

Optional later comparison:

3. Compressed coordination protocol + compressed final answer prompt
   - use the best output-compression method from the first project
   - likely `Minimal Semantic Compression (Round 3)`

## Recommended benchmark shape

Primary benchmark:
- same task
- same agents
- same number of turns
- compare internal communication cost between:
  - normal English coordination
  - compressed protocol coordination

Measure:
- internal message word count / token count
- final answer quality
- protocol compliance rate
- repair / clarification overhead
- total end-to-end cost

This means the first benchmark here should probably **not** be “normal prompt vs Round 3 prompt” alone.

That comparison is still useful, but it belongs to user-facing output compression.

For this project, the more direct comparison is:
- normal internal agent communication
- compressed internal agent communication

## Initial protocol direction

Start with controlled English, not a fully symbolic language.

Current protocol names:
- `RCCE-1` = `Relevance-Core Coordination English`
- `ATRCE-2` = `Act-Typed Relevance Coordination English`

Methodology:
- Protocol design is grounded in relevance-theoretic compression: preserve information needed for recoverability, remove low-value overhead.
- Protocol revisions are grounded in speech-act clarity: separate communicative acts so agents do not infer intent from ambiguous message forms.

## Debate system

This project uses a linguist-panel debate loop to generate and refine protocol candidates.

Process:
- a panel proposes competing protocol changes using linguistic arguments
- cross-critique identifies ambiguity, inferential load, and recoverability risks
- a synthesis pass produces a candidate protocol revision
- benchmark runs adjudicate the candidate against baselines

The benchmark is the decision layer; debate is the ideation layer.

Example:

```text
CLAIM: drop framing
EVID: q2,q3 shorter
OBJ: q1 factual loss
FIX: one-word rule for atomic facts
CONF: medium
NEXT: rerun benchmark
```

Why this direction:
- cheaper than prose
- still inspectable by humans
- easier to validate
- easier to translate back into plain English

## Risks

- protocol becomes too cryptic and loses reliability
- agents fail to follow it consistently
- repair traffic erases the savings
- debugging becomes harder than the cost win is worth

## Safeguards

- tiny vocabulary
- fixed message types
- required fields
- validator for structure
- plain-English fallback such as `ESCALATE` or `UNSURE`
- benchmark both compression and adherence

## Suggested next files to create

- `00_project_scope.md`
- `01_agent_protocol_hypothesis.md`
- `02_message_types.md`
- `03_protocol_examples.md`
- `04_benchmark_plan.md`
- `05_failure_modes.md`
- `run_tests.py` adapted for protocol benchmarking
