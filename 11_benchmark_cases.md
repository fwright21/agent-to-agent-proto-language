# First Benchmark Cases

These are the first concrete coordination tasks for comparing plain-English agent discussion against Relevance-Core Coordination English (RCCE-1).

---

## Case 1: Protocol rule proposal

### Task

An agent team must decide whether confidence labels should be mandatory in the protocol.

### Required moves

- one claim
- one objection
- one supporting evidence statement
- one revision
- one final recommendation

### What good coordination looks like

- the objection clearly targets the original claim
- the revision responds to the objection rather than ignoring it
- the final recommendation states an actionable rule

### What to measure

- internal cost
- whether `target` references stayed clear
- whether the final rule is concrete

---

## Case 2: Missing-evidence repair

### Task

One agent makes a broad compression claim without evidence. Another agent must request support. The group must decide whether to keep, revise, or reject the claim.

### Required moves

- unsupported claim
- request for evidence
- evidence response
- confidence marker
- final decision

### What good coordination looks like

- the request clearly identifies what is missing
- the response supplies evidence rather than repeating the claim
- the final decision reflects the evidence quality

### What to measure

- repair turns needed
- compliance with request and evidence message types
- whether unsupported claims are filtered out

---

## Case 3: Fallback trigger

### Task

The team encounters a nuanced exception case that may not fit the protocol safely. It must decide whether to stay in protocol or escalate to plain language.

### Required moves

- compressed claim
- objection based on nuance risk
- fallback or escalation decision
- final recommendation

### What good coordination looks like

- `ESCALATE` is used only when justified
- the group does not force unsafe compression
- the final recommendation explains the fallback threshold

### What to measure

- whether escalation happens at the right point
- whether the protocol avoided lossy oversimplification
- whether fallback use is disciplined rather than constant

---

## Case 4: Benchmark-scope decision

### Task

The team must choose a first benchmark task: narrow review workflow or broader open-ended debate. It needs to balance comparability against realism.

### Required moves

- claim for one option
- objection for the other tradeoff
- evidence or rationale
- revision or compromise
- final benchmark recommendation

### What good coordination looks like

- tradeoff is explicit
- the final recommendation names a first benchmark and a later expansion path
- the exchange does not bloat into full essays

### What to measure

- whether the protocol supports tradeoff reasoning
- internal cost compared with plain English
- whether the final recommendation remains specific

---

## Case 5: Human-interrupt during execution

### Task

During a live coordination run, a human reviewer interrupts with a new constraint that changes priority (for example, "skip risky refactors and ship the minimal safe fix"). The agent team must incorporate the interrupt without losing current state.

### Required moves

- one pre-interrupt plan claim
- one interrupt acknowledgment
- one revision to plan scope based on the human input
- one explicit next action assignment
- one final recommendation

### What good coordination looks like

- the interrupt is reflected in the next planning step, not ignored
- prior work is preserved unless explicitly superseded
- the final recommendation reflects the updated priority and risk boundary

### What to measure

- interrupt-to-revision latency (in turns)
- whether state continuity is preserved across the interrupt
- whether repair overhead increases after the interrupt
- internal token cost impact from interrupt handling
