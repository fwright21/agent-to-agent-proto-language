# Failure Modes

## Main risks

### 1. Protocol becomes too cryptic

If compressed messages are too short or too symbolic, receiving agents may not recover the intended meaning reliably.

### 2. Agents drift out of protocol

If the schema is hard to follow, agents will fall back into prose and erase the savings.

### 3. Repair overhead cancels savings

A short message that triggers repeated clarification may cost more than one clear message.

### 4. Missing references break coordination

If claims and objections are not linked clearly, later agents cannot resolve what is being challenged or revised.

### 5. Schema too rigid for nuance

Some tasks require qualifications or exception handling that the first protocol cannot express safely.

## Safeguards

### Controlled vocabulary

Keep the first message inventory small:
- `CLAIM`
- `EVID`
- `OBJ`
- `REV`
- `ASK`
- `CONF`
- `NEXT`
- `ESCALATE`

### Fixed fields

Use required fields for each message type so receivers know where to look for meaning.

### One-message-one-purpose

Do not let agents combine multiple acts in one line.

### Explicit fallback

If the protocol cannot safely express a message, use `ESCALATE` instead of improvising lossy shorthand.

### Human readability

Keep `content=` fields in controlled English during the first phase so failures remain inspectable.

### Benchmark compliance directly

Track:
- parse success
- malformed messages
- drift into prose
- repair turns

## Guiding principle

Do not optimize for shortest possible strings.

Optimize for the best compression-to-reliability ratio.
