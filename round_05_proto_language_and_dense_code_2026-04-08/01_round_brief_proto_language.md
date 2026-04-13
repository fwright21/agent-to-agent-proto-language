# Round 5A Brief: Proto-Language Track

Date: 2026-04-08
Mode: Minimal guidance, evidence-informed
Candidate name target: `PCL-1`

## Input

- Current best protocol: `ATRCE-2`
- Current benchmark signal on the 7-case suite:
  - `plain_english`: `556` internal tokens, `0.1` repair, `2.4` final quality
  - `RCCE-1`: `384` internal tokens, `0.4` repair, `2.3` final quality
  - `ATRCE-2`: `362` internal tokens, `0` repair, `2.3` final quality
- Interpretation:
  - structured protocol clearly saves tokens
  - repair has been controlled by stronger act typing
  - most meaning still lives in English inside slot values

## Core question

Can a true proto-language for agent coordination beat `ATRCE-2` by carrying more meaning in its own grammar and vocabulary, rather than in free English phrases?

## What counts as proto-language here

The candidate should move meaning into the system itself.

That means:
- less English inside `content=...`
- more meaning carried by message type, word order, compact atoms, and reusable forms
- a small stable vocabulary that can be recombined across cases
- explicit fallback when the code cannot safely express a nuance

This does not need to be a full general language.
It does need to be more than a fielded template with English in the boxes.

## Constraints

- Do not optimize for shortest strings alone.
- Optimize for compression with recoverability.
- Preserve explicit disagreement, evidence linkage, revision, next-action assignment, and fallback safety.
- Keep the system learnable enough that a model can apply it consistently across the benchmark cases.
- Minimize free English, but do not ban it completely if a narrow fallback is necessary.
- Prefer compositional structure over arbitrary abbreviations.

## Required output

1. A candidate proto-language spec named `PCL-1`.
2. The core vocabulary and grammar rules.
3. The fallback rule and when it triggers.
4. Example encodings for at least these cases:
   - missing-evidence repair
   - fallback trigger
   - human interrupt during execution
5. A brief rationale explaining why `PCL-1` should save tokens vs `ATRCE-2`.
6. Risks introduced by the design.

## Direct prompt

```text
You are a linguist panel designing an agent coordination proto-language.

Input context:
- Current best protocol: ATRCE-2
- Current benchmark signal on a 7-case suite:
  - plain_english: 556 internal tokens, 0.1 repair, 2.4 final quality
  - RCCE-1: 384 internal tokens, 0.4 repair, 2.3 final quality
  - ATRCE-2: 362 internal tokens, 0 repair, 2.3 final quality
- Interpretation:
  - structured protocol clearly saves tokens
  - repair has been controlled by stronger act typing
  - most meaning still lives in English inside slot values

Task:
Design a candidate proto-language named PCL-1 for multi-agent coordination.

Definition of success:
- PCL-1 should move meaning into the system itself rather than relying mainly on English phrases inside fields.
- It should be more language-like than ATRCE-2, but still stable and recoverable under the benchmark cases.

Constraints:
- Do not optimize for shortest strings alone.
- Optimize for compression with recoverability.
- Preserve explicit disagreement, evidence linkage, revision, next-action assignment, and fallback safety.
- Minimize free English.
- Prefer compositional structure over arbitrary opaque abbreviations.

Required output:
1. PCL-1 spec.
2. Core vocabulary and grammar rules.
3. Fallback rule.
4. Example encodings for:
   - missing-evidence repair
   - fallback trigger
   - human interrupt during execution
5. Brief rationale for why it should beat ATRCE-2 on token cost without causing repair collapse.
6. Risks.
```
