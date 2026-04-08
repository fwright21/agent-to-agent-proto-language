# Agent Coordination Evaluation Criteria

## Baseline

The baseline is plain-English coordination between agents on the same task.

That means:
- no compressed protocol
- normal sentence-level explanations
- ordinary objections, evidence statements, and next-step proposals in prose

The goal is to beat this baseline on internal communication cost without collapsing coordination quality.

---

## Evaluation axes

### 1. Internal communication reduction (primary)

Does the candidate protocol reduce the amount of agent-to-agent communication versus plain-English coordination?

Measure:
- words or tokens used in internal messages
- averaged across benchmark tasks

This is the primary axis.

---

### 2. Reliability

Can agents still exchange the required state correctly?

Questions:
- are claims still understandable?
- are objections still targetable?
- are evidence references still recoverable?
- is next action clear?

---

### 3. Compliance

Do agents actually follow the protocol consistently?

A protocol that saves tokens only when perfectly obeyed but is usually ignored is weak.

Measure:
- percent of messages that parse
- percent of turns that match schema
- percent of turns needing repair

---

### 4. Repair overhead

How much extra communication is needed when the protocol fails?

A compressed protocol can look good on raw message length but still lose overall if it causes:
- clarification turns
- retries
- restatements
- fallback expansions

---

### 5. Final-answer quality

Did the protocol preserve the quality of the final output?

Even if the internal coordination is cheaper, the protocol fails if it materially damages:
- correctness
- completeness
- usefulness

---

## Winning condition

A winning protocol should:
- reduce internal communication cost
- maintain acceptable reliability
- maintain acceptable final-answer quality
- avoid large repair overhead

If a protocol is cheaper but causes frequent failure or confusion, it has not actually won.
