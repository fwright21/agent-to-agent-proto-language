# Shared Questions for All Agents

Every agent must answer all five questions. This keeps debate rounds comparable and forces each framework to address the actual protocol problem.

---

## The five shared questions

### 1. What does plain-English coordination include that agents do not actually need?

Identify the parts of ordinary inter-agent discussion that are wasteful:
- repeated framing
- social padding
- long explanations of already-shared state
- repeated justifications
- redundant summaries

Be specific.

---

### 2. What information must never be lost in a compressed protocol?

Define the non-negotiable state-transfer floor.

Examples:
- claim
- evidence
- target of objection
- confidence
- next action
- fallback request

Which fields are mandatory for collaboration to remain reliable?

---

### 3. What protocol instruction, in one sentence, would reduce coordination cost?

One sentence. Actual instruction text. Not a principle description.

Example shape:
> "Use fixed message types with one claim per line and explicit evidence references."

---

### 4. Where would your protocol fail or become unsafe?

Be honest about failure modes:
- ambiguity
- missing references
- unparseable compression
- repair overhead
- inability to express nuance

These are the cases where plain English may still be necessary.

---

### 5. What fallback rule is necessary when the compressed protocol is not enough?

A serious protocol needs an escape hatch.

Examples:
- `ESCALATE`
- `UNSURE`
- `NEED-PLAIN-ENGLISH`

What should the fallback be, and when should it trigger?
