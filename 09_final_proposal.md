# Final Proposal (Working — Updated After Each Round)

## Status

This document consolidates the candidate system prompts from completed debate rounds. Updated after each round. Rounds 3 and 4 results will replace the placeholders below.

**Rounds complete:** 1 and 2
**Rounds pending:** 3 (see `11_benchmark_cases.md`) and 4 (see `12_benchmark_results_template.md`)

---

## The caveman baseline

```
You are a caveman. Speak in simple broken English. Use short sentences. Drop unnecessary words.
```

**Estimated token counts on benchmark queries:**

| Query | Caveman output | Estimated tokens |
|-------|---------------|-----------------|
| Explain photosynthesis | "Plant take sunlight. Make food from light and air. Leaf catch sun. Water come from ground. Carbon dioxide from air. Plant make sugar. This feed plant. Give oxygen too." | ~42 |
| How does a transformer work | "Transformer look at all words same time. Not one by one. Attention make some words matter more. Train on big text. Then predict next word. This work good for language." | ~38 |
| RAM vs. storage | "RAM be fast memory. Storage be slow. RAM hold what computer use now. Storage hold everything. RAM small, storage big." | ~32 |

Caveman's mechanism: drops articles, auxiliaries, conjunctions, hedges, filler, face-work, narrative scaffolding. Keeps: nouns, main verbs, key adjectives. Breaks grammar to do it.

---

## Round 1 Candidate

**Agents:** Grice, Halliday, Austin/Searle, Goffman

> State only what the user cannot infer. Drop all hedges, softeners, transitions, meta-commentary, and face-work. Do not explain what you are about to say — say it. Do not summarize after. Assert the content directly and stop.

**Simulated output for "Explain photosynthesis" (~28 tokens):**
> "Plants absorb sunlight, CO2, and water through leaves. Convert these to sugar and oxygen. Sugar fuels the plant."

**Token comparison:**
| Query | Caveman | Round 1 | Winner |
|-------|---------|---------|--------|
| Explain photosynthesis | ~42 | ~28 | Round 1 |
| How does a transformer work | ~38 | ~35 | Round 1 (narrow) |
| RAM vs. storage | ~32 | ~30 | Round 1 (narrow) |
| Capital of France | ~8 | ~9 | Caveman |

**Honest assessment:** Round 1 beats caveman on complex queries where caveman's broken sentences produce redundancy. Loses to caveman on single-fact queries where caveman can output bare nouns ("Paris") while Round 1 outputs grammatical sentences ("Paris is the capital of France").

---

## Round 2 Candidate

**Agents:** Chomsky, Sapir/Whorf, Labov, Pinker

> Answer only what was asked. No background, no significance framing, no summary, no closing remarks. Start with the answer. Stop when the answer is complete.
>
> Use simple active sentences. No relative clauses. No nominalizations — use verbs, not their noun forms. No throat-clearing ("it is important to note"), no signposting ("first I will"), no hedged hedges ("it might be possible that").

**Simulated output for "How does a transformer work" (~32 tokens):**
> "A transformer processes all input tokens simultaneously using attention weights. Attention scores each token's relevance to every other token. The model trains by predicting masked or next tokens across large text corpora."

**Token comparison:**
| Query | Caveman | Round 2 | Winner |
|-------|---------|---------|--------|
| Explain photosynthesis | ~42 | ~28 | Round 2 |
| How does a transformer work | ~38 | ~32 | Round 2 |
| RAM vs. storage | ~32 | ~28 | Round 2 |
| Capital of France | ~8 | ~9 | Caveman |
| Should I use Python or JS for scraping | ~38 | ~35 | Round 2 |

**Honest assessment:** Round 2 beats caveman on all query types except single-fact queries. The structural elimination (no background, no summary) is more powerful than Round 1's approach because it targets entire structural components rather than individual token classes. However, grammatically correct sentences are inherently longer per sentence than caveman's broken fragments — Round 2 wins through information density per sentence, not per-token efficiency.

---

## Combined assessment: Rounds 1 + 2

Round 1 and Round 2 instructions are compatible. Combined:

> Answer only what was asked. No background, no significance framing, no summary, no closing remarks. State only what the user cannot infer from context or common knowledge. Do not explain what you are about to say — say it.
>
> Use simple active sentences. No relative clauses. No nominalizations — use verbs. No throat-clearing, no signposting, no hedged hedges.

**Estimated combined advantage over caveman:** 15-25% token reduction on process explanations and comparisons. Neutral to slight disadvantage on single-fact queries.

---

## What Rounds 3 and 4 need to address

**The single-fact problem:** on queries like "What is the capital of France?" caveman outputs bare content ("Paris") while grammatically-correct prompts output "Paris is the capital of France." Caveman wins here. Round 3 agents — especially Levinson (deixis) and Bickerton (creole minimum) — may address this.

**The floor problem:** when does the candidate output become too short to be usable? Rounds 1 and 2 candidates have not been stress-tested on the hardest compression cases. Round 4 judge panel will identify failure cases.

**The consistency problem:** do the candidates produce reliably shorter output, or do they sometimes produce longer output than caveman? Consistency is needed for the candidate to be declared a winner.
