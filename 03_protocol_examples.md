# Protocol Examples

## Example 1: Protocol design disagreement

### Plain-English version

> I think we should keep messages very short and avoid adding confidence labels because they may not be necessary if the objection itself is clear.
>
> I disagree. Confidence labels help downstream agents decide whether to request clarification or proceed. Without them, compressed messages may be harder to triage.
>
> Fair point. We could keep confidence labels but restrict them to low, medium, and high.

### Protocol version

```text
CLAIM: id=c1; topic=confidence; content=remove confidence labels
OBJ: target=c1; reason=triage-risk; content=receivers need uncertainty signal
REV: target=c1; change=restrict-values; content=use low-medium-high only
```

### What changed

- framing and politeness disappeared
- each turn has one job
- the disagreement target is explicit
- revision is easy to parse

## Example 2: Missing evidence request

### Plain-English version

> Your claim that the protocol saves tokens is too abstract. Can you show a specific task where plain English repeated state unnecessarily?
>
> Yes. In the planning task, the plain-English agents restated the same objective in each turn.

### Protocol version

```text
ASK: target=c2; need=specific example of token waste
EVID: target=c2; source=planning-task; content=agents repeated same objective each turn
```

## Example 3: Fallback to plain language

### Situation

An agent finds that a legal-risk exception is too nuanced for the schema.

### Protocol version

```text
ESCALATE: reason=exception chain requires plain language explanation
```

### Intended behavior

After `ESCALATE`, the system temporarily allows plain English for that message rather than forcing lossy compression.

## Example 4: Small coordination sequence

### Task

Decide whether to test a protocol on a review workflow before broader debate tasks.

### Protocol sequence

```text
CLAIM: id=c3; topic=benchmark; content=start with review workflow
EVID: target=c3; source=design-rule; content=structured tasks easier to compare
OBJ: target=c3; reason=coverage-risk; content=review workflow may underrepresent open debate
REV: target=c3; change=narrow-scope; content=use review workflow first then expand
NEXT: owner=judge; action=define first benchmark task and metrics
```

## Interpretation guide

This protocol is meant to be:
- shorter than normal prose
- easier to validate than improvised shorthand
- readable enough for debugging

If later benchmarks show high compliance and low repair cost, the project can test a more compressed variant.
