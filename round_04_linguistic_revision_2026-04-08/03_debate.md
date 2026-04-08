# Round 4 Debate Record

Date: 2026-04-08
Status: Draft completed

## Input context

- Baseline protocol: `Relevance-Core Coordination English (RCCE-1)`
- Prior benchmark signal (7 cases):
  - internal tokens reduced: `556 -> 384` (`30.9%`)
  - repair turns increased: `0.1 -> 0.4`
  - final quality slightly lower: `2.4 -> 2.3`
  - weakest behavior under interruption/fallback pressure

## Debate question

How should `RCCE-1` be revised into `ATRCE-2` so compression remains strong while recoverability improves, using linguistic reasoning?

## Procedure

1. Opening proposals from each agent.
2. Cross-critique focused on linguistic tradeoffs.
3. Revision pass based on strongest critiques.
4. Synthesis into one candidate `ATRCE-2`.

## Discussion log

### Opening proposals

- **Chomsky**
  - Problem diagnosis: repair turns rise when structural role is underspecified, especially in interrupt events where `ASK` is overloaded.
  - Proposal: reserve `ASK` for epistemic requests only; introduce a distinct directive-interrupt act to preserve clause force.
  - Compression stance: keep one-line schema and fixed fields.

- **Sperber & Wilson**
  - Problem diagnosis: inferential load is too high in fallback/interrupt turns because listener must infer whether the speaker is asking, revising, or changing priority.
  - Proposal: encode communicative intention explicitly for high-risk turns with minimal added tokens.
  - Compression stance: add explicitness only where repair cost is highest.

- **Bickerton**
  - Problem diagnosis: protocol floor is stable for normal exchanges, but boundary events (interrupt/fallback) lack a minimal dedicated grammar.
  - Proposal: add one minimal message type for external directive shift and require target anchoring on escalation.
  - Compression stance: no new freeform prose; preserve tight slot grammar.

- **Lakoff**
  - Problem diagnosis: some `content=` fields still carry framing language in revisions and next-step assignment.
  - Proposal: enforce action-first content and ban explanatory framing in protocol lines.
  - Compression stance: cut residual metadiscourse, keep factual and directive payload.

### Cross-critique

- Chomsky critiques Lakoff: framing removal alone does not solve illocution ambiguity; type-level distinction is required.
- Sperber & Wilson critiques Chomsky/Bickerton: adding types can bloat inventory unless constrained to empirically costly cases.
- Bickerton critiques Sperber & Wilson: inferential optimization must remain mechanically enforceable in schema, not soft guidance only.
- Lakoff critiques all: new act types should be justified only where current type overloading repeatedly causes repair.

Consensus from critique:
1. The interruption problem is primarily a speech-act typing failure, not a lexical compression failure.
2. `ASK` should not carry interrupt directives.
3. Fallback should preserve reference to the affected target so re-entry to schema is easier.
4. Additional explicitness should be narrowly scoped to boundary events.

### Revision pass

- Agreed changes:
  1. Add `INTERRUPT` message type for external priority/directive changes.
  2. Keep `ASK` strictly for missing-information requests.
  3. Tighten `ESCALATE` to include `target` and `reason`.
  4. Add a short protocol rule: action-first, no framing language in `content`.
  5. Keep existing core types and one-line grammar to preserve familiarity and compliance.

- Rejected changes:
  - No broad symbolic shorthand expansion in this round.
  - No removal of `REV`/`NEXT`; both remain central for recoverable coordination.

### Final synthesis

- Synthesis judgment:
  - `RCCE-1` already achieves substantial token savings.
  - Main failure mode is pragmatic ambiguity at boundary turns.
  - Minimal fix is a constrained grammar extension targeting interruption/fallback recoverability.
  - Proposed candidate: `Act-Typed Relevance Coordination English (ATRCE-2)`.

## Candidate output slot

```text
Protocol: Act-Typed Relevance Coordination English (ATRCE-2)

Line grammar:
TYPE: field=value; field=value; ...

Allowed types and required fields:

CLAIM: id, topic, content
EVID: target, source, content
OBJ: target, reason, content
REV: target, change, content
ASK: target, need
CONF: target, level
NEXT: owner, action
ESCALATE: target, reason
INTERRUPT: source, priority, directive

Rules:
1. One line, one act.
2. One message, one purpose.
3. Use ASK only for missing information.
4. Use INTERRUPT only for external directive/priority shifts.
5. Use ESCALATE only when schema cannot safely encode meaning; always anchor to target.
6. Action-first content: no framing/politeness text in content/action fields.
7. Keep references explicit by id/target when claim state changes.
8. If interrupted, send INTERRUPT then REV/NEXT to re-bind plan state.

Example interrupt sequence:
CLAIM: id=c7; topic=release-plan; content=refactor parser and validator before ship
INTERRUPT: source=human-reviewer; priority=safety-now; directive=skip risky refactors and ship minimal safe fix
REV: target=c7; change=reduce-scope; content=patch validator only and defer parser refactor
NEXT: owner=agentc; action=prepare validator patch and agenta add regression test
```

## Rationale slot

- **Speech-act disambiguation**
  - Interruption is a distinct illocutionary act. Encoding it as `ASK` created force ambiguity and extra repair.
- **Inferential load control**
  - Adding explicit intention only at boundary turns reduces recoverability failures without broad verbosity.
- **Reference continuity**
  - Requiring `target` on `ESCALATE` supports coherent return from fallback and preserves discourse thread identity.
- **Minimal grammar extension**
  - One additional type (`INTERRUPT`) preserves the small grammar principle while addressing the highest-cost failure pattern.
- **Compression preservation**
  - Core compact format and type inventory are retained; changes are localized to high-repair contexts.

## Open risks

- `INTERRUPT` could be overused as a generic planning tool unless constrained by prompts/validation.
- `ESCALATE target=` may add minor token overhead in already dense turns.
- Local benchmark signal may not generalize to live external model behavior.
- Quality gains may require further lexical-level refinement beyond act-typing changes.
