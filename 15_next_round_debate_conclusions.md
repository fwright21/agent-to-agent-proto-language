# Next Round Debate Conclusions (Pre-Brief)

Date: 2026-04-08
Scope: conclusions from the current 7-case benchmark to guide the next linguist debate round.

## Empirical conclusions to carry forward

1. `RCCE-1` is a real compression win on internal coordination:
   - plain English: `556` internal tokens
   - protocol RCCE-1: `384` internal tokens
   - reduction: `30.9%`
2. Protocol adherence is currently strong (`100%` compliance in local runs).
3. The main weakness is repair overhead:
   - plain English: `0.1` average repair turns
   - protocol RCCE-1: `0.4` average repair turns
4. Final recommendation quality shows a small dip:
   - plain English: `2.4`
   - protocol RCCE-1: `2.3`
5. Compression is weakest under interruption pressure (`human_interrupt_during_execution`), where token gains shrink and repair pressure rises.

## Design objective for the next protocol candidate

`ATRCE-2` should preserve compression while improving robustness under interruption and fallback pressure.

Target envelope for the next candidate:
- keep token reduction at or above `25%` vs plain English
- reduce repair turns below `0.4`
- recover final quality to at least baseline-adjacent behavior
- preserve high schema adherence

## Linguistics-centered research questions for the panel

1. **Information structure under interruption**
   - Which discourse functions are being under-encoded when a human interrupt occurs (topic shift marking, scope revision marking, or commitment update marking), and which minimal markers restore recoverability?

2. **Speech-act typing and illocution clarity**
   - Does interruption constitute a distinct illocutionary act that requires its own message type, or can current acts (`ASK`/`REV`) encode it without pragmatic ambiguity?

3. **Reference economy vs. anaphora failure**
   - How far can reference forms be reduced (ellipsis, pronouns, compressed IDs) before anaphora resolution breaks in multi-turn, multi-agent exchanges?

4. **Escalation grammar and boundary conditions**
   - What linguistic boundary should trigger `ESCALATE`: semantic underspecification, unresolved deixis, or high inferential load, and how can that trigger be encoded compactly?

5. **Compression hierarchy by linguistic layer**
   - Which layer now offers safest additional savings: discourse framing, syntax, lexical redundancy, or message-type inventory, given current repair behavior?

6. **Repair minimization as a pragmatic constraint**
   - Can the protocol include a minimal set of obligatory coherence cues that lower clarification turns while preserving most token savings?

## Debate instruction framing

The next debate should not optimize for shortest strings alone. It should optimize for:
1. compressibility,
2. recoverability,
3. low repair traffic,
4. stable final recommendation quality.

Use the benchmark as the adjudication layer for claims.
