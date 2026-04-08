# First Protocol Message Types

## Protocol name

**Relevance-Core Coordination English (RCCE-1)**

This is the first candidate protocol for agent-to-agent compressed communication.

## Design goal

Keep the message grammar small enough that agents follow it reliably, but expressive enough to support real disagreement and revision.

## Message format

Each line is one message.

General shape:

```text
TYPE: content
```

When needed, add fixed subfields separated by `;`.

General extended shape:

```text
TYPE: field=value; field=value; field=value
```

## Core message types

### `CLAIM`

Use when proposing a substantive position.

Required fields:
- `id`
- `topic`
- `content`

Example:

```text
CLAIM: id=c1; topic=protocol; content=one-purpose-per-message
```

### `EVID`

Use when providing supporting evidence for a claim or objection.

Required fields:
- `target`
- `source`
- `content`

Example:

```text
EVID: target=c1; source=task-1; content=plain-english repeated context twice
```

### `OBJ`

Use when challenging a prior claim.

Required fields:
- `target`
- `reason`
- `content`

Example:

```text
OBJ: target=c1; reason=ambiguity-risk; content=message too short for exception cases
```

### `REV`

Use when revising a prior claim or protocol rule.

Required fields:
- `target`
- `change`
- `content`

Example:

```text
REV: target=c1; change=add-fallback; content=allow plain language on unresolved reference
```

### `ASK`

Use when requesting missing information.

Required fields:
- `target`
- `need`

Example:

```text
ASK: target=c1; need=example-of-failure
```

### `CONF`

Use when marking confidence.

Required fields:
- `target`
- `level`

Allowed values for `level`:
- `low`
- `medium`
- `high`

Example:

```text
CONF: target=c1; level=medium
```

### `NEXT`

Use when assigning the next coordination step.

Required fields:
- `owner`
- `action`

Example:

```text
NEXT: owner=judge; action=compare protocol against plain english
```

### `ESCALATE`

Use when the protocol is not enough and plain English is required.

Required fields:
- `reason`

Example:

```text
ESCALATE: reason=nuance not expressible safely in schema
```

## Protocol rules

1. One message, one purpose.
2. One line per message.
3. Reference earlier items by `id` whenever possible.
4. Do not restate shared context unless asked.
5. Use `ESCALATE` instead of improvising long prose.
6. If a message cannot be expressed safely, fall back explicitly.
7. Keep `content` short and concrete.

## What this protocol is trying to remove

The protocol is designed to cut:
- greetings and social tone
- paragraph framing
- narrative transitions
- repeated explanation of task state
- indirect disagreement
- verbose justifications

## What this protocol keeps explicit

The protocol keeps explicit:
- claims
- evidence links
- objections
- revisions
- uncertainty
- next actions
- fallback conditions

## Why this is not a fully symbolic language

This version still uses readable English inside `content=` fields.

That is deliberate. The first benchmark should test whether structure plus constrained slots is enough to save tokens without causing large reliability losses.
