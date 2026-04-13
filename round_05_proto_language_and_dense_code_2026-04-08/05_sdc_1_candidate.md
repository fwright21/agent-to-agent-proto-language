# SDC-1 Candidate

Date: 2026-04-08
Status: first-pass candidate for benchmark evaluation
Name: `Semantically Dense Code 1`

## Design idea

`SDC-1` is a compact codebook, not a language-like grammar.

It pushes compression harder by using:

- operator-led lines
- short payload chunks
- symbolic composition
- dense state transforms such as `x>y`, `x->y`, and `a|b`

## Line grammar

```text
OPREF PAYLOAD
```

## Operators

- `+` claim
- `-` objection
- `=` evidence
- `~` revision
- `?` ask
- `^` confidence
- `!` next action
- `/` escape
- `@` interrupt

## Rules

1. One line, one act.
2. Keep payloads compact and compositional.
3. Reuse the same atoms across cases.
4. Use `/ref reason` when compression would hide critical nuance.
5. Keep final output in plain English.

## Example

```text
+c1 conf.tag=req
-c1 ovh>all-line
=c1 notes>tag-if-needed
~c1 tag@uncertain|disputed
```

## Expected advantage

`SDC-1` should save tokens vs `ATRCE-2` if the codebook remains stable enough that the model does not need to reconstruct English internally every turn.

## Main risks

- tokenizer risk: compact symbol strings may not tokenize as cheaply as they look
- repair risk: dense payloads may become harder to interpret under interruption or fallback pressure
- debugging risk: humans may lose readability faster than with `PCL-1`
