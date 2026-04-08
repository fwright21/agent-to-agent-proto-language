# Project Scope

## Short version

This project is about compressing **agent-to-agent coordination**, not just compressing the final answer to the user.

## Core research question

Can a constrained coordination protocol reduce multi-agent communication cost without materially hurting reliability or final-answer quality?

## Primary comparison

Use the same collaborative task and compare:

1. Plain-English coordination
2. Compressed coordination protocol

The primary benchmark should measure:
- internal communication volume
- final-answer quality
- coordination failures
- total end-to-end cost

## Secondary comparison

After the protocol benchmark exists, optionally test:

1. Plain-English coordination + plain final answer
2. Plain-English coordination + compressed final answer
3. Protocol coordination + plain final answer
4. Protocol coordination + compressed final answer

This separates two different savings effects:
- savings from internal coordination compression
- savings from final-output compression

## Why this matters

The first project found that semantic compression can beat caveman-style output compression on user-facing responses.

This project asks whether a similar idea can be applied internally:
- agents should not waste tokens talking to each other in full prose when a compact protocol is enough

## Initial protocol design constraints

- controlled English, not a pure symbolic language
- small fixed vocabulary
- one message = one purpose
- required fields
- easy translation back into plain English
- explicit fallback when the protocol cannot safely express the message

## Minimal first benchmark task

A good first task is a small debate or review workflow where agents must:
- make claims
- object
- cite evidence
- propose revisions
- decide a next step

That is a better starting point than a broad creative task.

## First implementation recommendation

Do not rewrite the whole copied project at once.

Instead:
1. keep the copied structure as scaffolding
2. define the first protocol
3. swap the benchmark so it measures agent coordination cost
4. only then rewrite the debate prompts around the new question
