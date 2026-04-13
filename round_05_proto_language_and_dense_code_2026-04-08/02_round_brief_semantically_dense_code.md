# Round 5B Brief: Semantically Dense Code Track

Date: 2026-04-08
Mode: Minimal guidance, evidence-informed
Candidate name target: `SDC-1`

## Input

- Current best protocol: `ATRCE-2`
- Current benchmark signal on the 7-case suite:
  - `plain_english`: `556` internal tokens, `0.1` repair, `2.4` final quality
  - `RCCE-1`: `384` internal tokens, `0.4` repair, `2.3` final quality
  - `ATRCE-2`: `362` internal tokens, `0` repair, `2.3` final quality
- Key hypothesis:
  - additional savings may come from a denser coordination code rather than from more English-like protocol structure

## Core question

Can a semantically dense coordination code beat `ATRCE-2` by using a compact shared codebook that carries more task meaning per token?

## What counts as semantically dense code here

The candidate should behave more like a compact codebook than like normal prose.

That means:
- short reusable atoms for recurring coordination meanings
- composition rules that let multiple meanings be packed into one short line
- minimal glue words
- strong reuse across benchmark cases
- explicit fallback when code density would make a message unsafe

This track does not need to look like a natural language.
It can be more code-like than the proto-language track.

## Important caution

Dense-looking strings are not automatically cheap for a model.

The candidate should therefore avoid:
- arbitrary one-off abbreviations
- symbols with unclear semantics
- forms that require too much decoding work
- compression that depends on the reader already knowing unstated hidden mappings

Prefer:
- stable ASCII atoms
- compositional chunks
- repeated short forms for repeated functions
- predictable separators and ordering

## Constraints

- Do not assume that a human notion of "dense" equals token efficiency.
- Optimize for benchmarkable coordination compression, not aesthetic cleverness.
- Preserve explicit claim, objection, evidence, revision, interrupt handling, next action, and fallback.
- Keep the codebook small enough to generalize across the existing 7 benchmark cases.
- Include a safety rule for nuance-heavy exceptions.

## Required output

1. A candidate dense code spec named `SDC-1`.
2. A compact codebook of atoms and operators.
3. Composition rules showing how meanings combine.
4. Example encodings for at least these cases:
   - protocol rule proposal
   - fallback trigger
   - human interrupt during execution
5. A brief rationale explaining why `SDC-1` could save tokens vs `ATRCE-2`.
6. Risks introduced by the design, especially tokenizer risk and repair risk.

## Direct prompt

```text
You are a linguist panel designing a semantically dense coordination code for agent-to-agent communication.

Input context:
- Current best protocol: ATRCE-2
- Current benchmark signal on a 7-case suite:
  - plain_english: 556 internal tokens, 0.1 repair, 2.4 final quality
  - RCCE-1: 384 internal tokens, 0.4 repair, 2.3 final quality
  - ATRCE-2: 362 internal tokens, 0 repair, 2.3 final quality
- Hypothesis:
  - additional savings may come from a denser shared codebook rather than from English-like slot content

Task:
Design a candidate semantically dense coordination code named SDC-1.

Definition of success:
- SDC-1 should use a compact shared codebook that carries more coordination meaning per token than ATRCE-2.
- It does not need to look like a natural language.
- It does need to remain usable and recoverable across the benchmark cases.

Constraints:
- Do not assume that human-perceived density equals tokenizer efficiency.
- Avoid arbitrary one-off abbreviations.
- Prefer stable ASCII atoms, compositional chunks, and predictable separators.
- Preserve explicit claim, objection, evidence, revision, interrupt handling, next action, and fallback.
- Keep the codebook small enough to generalize across the 7 existing benchmark cases.

Required output:
1. SDC-1 spec.
2. Compact codebook of atoms and operators.
3. Composition rules.
4. Example encodings for:
   - protocol rule proposal
   - fallback trigger
   - human interrupt during execution
5. Brief rationale for why it could beat ATRCE-2 on token cost.
6. Risks, especially tokenizer risk and repair risk.
```
