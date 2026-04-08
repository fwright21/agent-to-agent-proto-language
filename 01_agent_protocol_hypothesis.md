# Agent Protocol Hypothesis

## Working hypothesis

A multi-agent system wastes tokens when agents communicate in full natural-language prose even though their real needs are narrower:
- state transfer
- disagreement targeting
- evidence reference
- confidence marking
- next-step coordination

The project hypothesis is that a constrained coordination protocol can reduce internal communication cost without materially hurting task performance.

## Design claim

The first useful protocol should be **controlled English**, not a fully symbolic language.

Why:
- models can follow it more consistently than opaque shorthand
- humans can still inspect failures
- validation is simpler
- fallback to plain language is easier

## What the protocol must preserve

A compressed message must still let the receiving agent recover:
- what claim is being made
- what earlier message it refers to
- what evidence supports or attacks it
- how certain the sender is
- what action should happen next

If those fields are missing, compression is probably false economy.

## What the protocol should strip away

The protocol should aggressively remove:
- politeness
- conversational openings and closings
- repeated restatement of shared context
- long-form rhetorical justification
- redundant summaries
- freeform narrative transitions

## Initial protocol principle

One message should serve one coordination purpose.

That means a message should usually do exactly one of these things:
- make a claim
- object to a claim
- cite evidence
- propose a revision
- request clarification
- mark uncertainty
- assign a next step

## Key prediction

Compared against plain-English agent discussion on the same task, the protocol should:
- reduce internal token count
- reduce repeated context restatement
- preserve enough structure for reliable handoff
- sometimes increase repair turns if it is too compressed

## Main failure conditions

The protocol fails if:
- references become unclear
- agents drift back into prose
- the schema is too rigid for nuance
- repair traffic cancels out the savings
- humans cannot audit why the agents reached a decision

## Evaluation stance

A successful protocol is not the shortest possible one.

A successful protocol is the one that produces the best tradeoff between:
- lower internal cost
- high parse/compliance rate
- low repair overhead
- acceptable final-answer quality
