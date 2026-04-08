# Debate Method

## Purpose

Find a compact agent-to-agent coordination protocol that reduces internal communication cost without materially hurting reliability or final-answer quality.

This project is not primarily about shortening the final user-facing answer. It is about shortening what agents say to each other while they collaborate.

---

## The core question for every round

> What communication protocol lets agents coordinate with fewer tokens than plain English while still transferring the state they need?

Every agent must answer this question with actual protocol design implications. Theory without concrete message design is not accepted.

---

## Debate structure

Each round should produce one candidate coordination method. A candidate may be:
- a controlled-English protocol
- a typed message schema
- a fixed-turn interaction rule
- a hybrid approach with fallback to plain English

The result of each round should be concrete enough to benchmark.

---

## What counts as the baseline

The default competitor is:
- plain-English agent coordination

That means agents exchange normal English messages, explain their reasoning in prose, and coordinate without any compression protocol.

The candidate protocol must beat that baseline on internal communication cost while keeping the collaboration functional.

---

## Structure of each debate round

1. **Opening statements**
Each agent argues for a protocol design principle and ends with a concrete one-sentence protocol instruction.

2. **Cross-examination**
Agents challenge whether the proposed protocol is:
- too cryptic
- too lossy
- too hard to follow
- too expensive to repair when it fails

3. **Revised positions**
Each agent updates their protocol proposal after objections.

4. **Draft protocol proposals**
Each agent writes an actual candidate protocol, schema, or message rule set.

5. **Synthesis**
The surviving ideas are combined into one benchmarkable coordination protocol.

---

## Rules

- Protocols must be concrete enough to test.
- Every protocol must specify what information is mandatory.
- Every protocol must specify when plain-English fallback is allowed.
- The benchmark must compare the protocol against plain-English coordination on the same task.
- If the protocol saves tokens but causes frequent repair turns or quality loss, that must be stated honestly.

---

## What success looks like

A successful round produces a protocol that:
- reduces internal communication volume
- still allows claims, objections, evidence, and next actions to be exchanged
- is parseable by both agents and humans inspecting the trace
- survives at least one benchmark task without falling apart
