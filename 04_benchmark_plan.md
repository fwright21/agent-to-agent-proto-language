# Benchmark Plan

## First benchmark

The first benchmark in this project should compare:

1. Plain-English agent coordination
2. Compressed protocol agent coordination

Use the same task, the same roles, and the same number of turns.

## First benchmark task

Use a small structured coordination task rather than a broad creative conversation.

Recommended first task:
- one agent proposes a protocol rule
- one agent objects
- one agent supplies evidence
- one agent revises the rule
- the group produces a final recommendation

This task is narrow enough to score reliably and broad enough to test disagreement, evidence transfer, and repair.

## Experimental conditions

### Condition A: Plain-English coordination

Agents communicate in ordinary concise English.

### Condition B: Relevance-Core Coordination English (RCCE-1)

Agents use the protocol defined in [02_message_types.md](./02_message_types.md).

## Metrics

### Cost metrics

- internal word count
- internal token count when available
- words or tokens per successful decision

### Reliability metrics

- protocol compliance rate
- parse success rate
- number of repair turns
- number of unresolved references

### Outcome metrics

- quality of final recommendation
- whether the final recommendation includes a concrete revision
- whether the group correctly identifies at least one failure mode

## Minimal scoring rubric

Score each run on:
- `cost`
- `compliance`
- `repair`
- `final_quality`

A protocol is promising if it lowers cost substantially without large losses in the other three categories.

## Later expansion

Once the first benchmark works, expand to a 2x2 design:

1. Plain coordination + plain final answer
2. Plain coordination + compressed final answer
3. Protocol coordination + plain final answer
4. Protocol coordination + compressed final answer

That separates:
- internal coordination savings
- final output savings

## What not to overclaim

The first benchmark will not prove a general machine language.

It will only test whether a small constrained protocol can outperform plain-English coordination on a narrow collaboration task.
