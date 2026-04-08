# Benchmark Suite

## Purpose

This benchmark does not test final-answer compression first. It tests whether a compressed coordination protocol can replace plain-English agent discussion on the same collaboration task.

## Primary comparison

For each task, compare:

1. Plain-English coordination
2. Relevance-Core Coordination English (RCCE-1)

Keep fixed:
- agent roles
- turn count
- task prompt
- required final output

## First benchmark tasks

Use narrow structured coordination tasks before broader open-ended discussions.

Recommended first three tasks:
- protocol rule design
- evidence-based objection and revision
- benchmark-plan decision

## What each run must produce

Each run should include:
- the internal agent exchange
- the final group recommendation
- a count of internal words or tokens
- a count of repair turns
- a note on whether the exchange remained parseable throughout

## Success condition

A protocol run is a real win only if it:
- lowers internal communication cost
- stays mostly compliant with the schema
- does not require large repair overhead
- still reaches a usable final recommendation

## Failure condition

A protocol run is not a win if it becomes shorter by silently dropping necessary information or by forcing repeated clarification.

## First reporting table

| Task | Plain-English cost | Protocol cost | Compliance | Repair turns | Final quality | Winner |
|------|--------------------|---------------|------------|--------------|---------------|--------|
| | | | | | | |

## Interpretation rule

The goal is not shortest possible strings.

The goal is best compression-to-reliability tradeoff.
