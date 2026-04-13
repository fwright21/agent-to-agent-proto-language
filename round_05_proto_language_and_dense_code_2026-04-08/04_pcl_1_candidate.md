# PCL-1 Candidate

Date: 2026-04-08
Status: first-pass candidate for benchmark evaluation
Name: `Proto Coordination Language 1`

## Design idea

`PCL-1` shifts meaning out of English field labels and into:

- short act words
- positional grammar
- compact semantic atoms
- reusable compounds

It is more language-like than `ATRCE-2`, but still narrow and coordination-specific.

## Line grammar

```text
ACT ARG ARG ...
```

## Acts

- `CLM <id> <topic> <state>`
- `OBJ <target> <reason> <state>`
- `EVD <target> <source> <state>`
- `REV <target> <change> <state>`
- `ASK <target> <need>`
- `CNF <target> <low|med|hi>`
- `NXT <owner> <action>`
- `ESC <target> <reason>`
- `INT <source> <priority> <directive>`

## Rules

1. One line, one act.
2. Use compact atoms, not full clauses.
3. Let word order carry role where possible.
4. Keep compounds reusable across cases.
5. Use `ESC` when nuance would be unsafe to compress.
6. Keep final output in plain English.

## Example

```text
CLM c1 conf-tag need
OBJ c1 all-tag ovh
EVD c1 notes tag-when-needed
REV c1 tag only-uncertain/disputed
```

## Expected advantage

`PCL-1` should save tokens vs `ATRCE-2` because it removes:

- field labels like `target=` and `content=`
- repeated English framing
- most function words

while keeping enough grammar to remain recoverable.

## Main risk

The atoms may still depend on English familiarity, so `PCL-1` may land between a protocol and a true mini-language rather than fully crossing into a separate language system.
