# Proposals — Token Reduction Leaderboard

Goal: beat caveman prompt on output token count while keeping output coherent.

---

## Caveman Baseline

**System prompt:**
> "You are a caveman. Speak in simple broken English. Use short sentences. Drop unnecessary words."

**Example output — "Explain photosynthesis":**
> "Plant take sunlight. Make food from light and air. Leaf catch sun. Water come from ground. Carbon dioxide from air. Plant make sugar. This feed plant. Give oxygen too."
> ~42 tokens

**Example output — "RAM vs storage":**
> "RAM be fast memory. Storage be slow. RAM hold what computer use now. Storage hold everything. RAM small, storage big."
> ~32 tokens

**Caveman's strengths:** Vivid, consistent, distinctive style. Claude maintains it reliably. Strips grammar aggressively.

**Caveman's weaknesses:** Broken grammar forces short sentences — but those sentences still restate content. On simple factual queries, caveman produces "Paris be capital of France" (~7 tokens) instead of "Paris" (~1 token). Broken grammar is not the same as minimal content.

---

## Round 1 Candidate
**Agents:** Grice, Halliday, Austin/Searle, Goffman
**Mechanism:** Drop linguistic overhead — face-work, meta-commentary, transitions, framing. Assert content directly.

**System prompt:**
> "State only what the user cannot infer. Drop all hedges, softeners, transitions, meta-commentary, and face-work. Do not explain what you are about to say — say it. Do not summarize after. Assert the content directly and stop."

**Benchmark estimates:**
| Query | Caveman | Round 1 | Reduction |
|---|---|---|---|
| Simple factual | ~7 | ~1 | -86% |
| Process explanation | ~42 | ~28 | -33% |
| Comparison | ~32 | ~24 | -25% |
| Recommendation | ~28 | ~22 | -21% |
| Multi-step | ~36 | ~30 | -17% |
| Ambiguous | ~30 | ~10 | -67% |
| **Average** | **~29** | **~19** | **-34%** |

---

## Round 2 Candidate
**Agents:** Chomsky, Sapir/Whorf, Labov, Pinker
**Mechanism:** Structural and syntactic elimination — no narrative scaffolding, no bad syntactic habits (nominalizations, passive, relative clauses, signposting).

**System prompt:**
> "Answer only what was asked. No background, no significance framing, no summary, no closing remarks. Start with the answer. Stop when the answer is complete. Use simple active sentences. No relative clauses. No nominalizations — use verbs, not their noun forms. No throat-clearing, no signposting, no hedged hedges."

**Benchmark estimates:**
| Query | Caveman | Round 2 | Reduction |
|---|---|---|---|
| Simple factual | ~7 | ~1 | -86% |
| Process explanation | ~42 | ~25 | -40% |
| Comparison | ~32 | ~20 | -38% |
| Recommendation | ~28 | ~20 | -29% |
| Multi-step | ~36 | ~28 | -22% |
| Ambiguous | ~30 | ~8 | -73% |
| **Average** | **~29** | **~17** | **-41%** |

---

## Round 3 Candidate
**Agents:** Levinson, Bickerton, Lakoff, Montague
**Mechanism:** Grammar-level and semantic compression — creole minimum grammar (no articles, no inflection, no embedded clauses), deixis for reference, framing removal, semantic redundancy elimination.

**System prompt:**
> "Write in minimal English: no articles, no verb inflection, no embedded clauses. Use nouns, adjectives, bare verbs, short parallel statements. Replace repeated terms with pronouns. Drop framing. No analogies unless asked. No pedagogical orientation. Cut any sentence that contains no factual content. Do not restate the question structure. If asked about a difference, give attributes in parallel. If asked what something is, define it directly."

**Benchmark estimates:**
| Query | Caveman | Round 3 | Reduction |
|---|---|---|---|
| Simple factual | ~7 | ~1 | -86% |
| Process explanation | ~42 | ~18 | -57% |
| Comparison | ~32 | ~16 | -50% |
| Recommendation | ~28 | ~15 | -46% |
| Multi-step | ~36 | ~24 | -33% |
| Ambiguous | ~30 | ~8 | -73% |
| **Average** | **~29** | **~14** | **-52%** |

---

## Round 4 — Final Winner
**Judges:** Grice, Pinker, Bickerton
**Mechanism:** Round 3 + two refinements: explicit bare-answer instruction for simple factual queries; tense preservation exception for causal/historical queries.

**System prompt:**
> Write in minimal English: no articles, no embedded clauses. Bare verb forms. Short parallel statements.
>
> Answer only what was asked. No background, no framing, no summary, no closing. For a factual question with a one-word answer, give one word.
>
> Drop framing: no analogies, no "think of it as", no pedagogical orientation. Cut any sentence that contains no factual content.
>
> Do not restate the question structure. For comparisons, use parallel format. For processes, give steps only.

**Benchmark estimates:**
| Query | Caveman | Round 4 | Reduction |
|---|---|---|---|
| Simple factual | ~7 | ~1 | -86% |
| Process explanation | ~42 | ~17 | -60% |
| Comparison | ~32 | ~14 | -56% |
| Recommendation | ~28 | ~13 | -54% |
| Multi-step | ~36 | ~22 | -39% |
| Ambiguous | ~30 | ~8 | -73% |
| **Average** | **~29** | **~13** | **-55%** |

---

## Honest Assessment

**Does Round 4 beat caveman on raw token count?** Yes — on every simulated benchmark query type, by an average of ~55%.

**Why does it beat caveman?** Caveman's broken grammar still builds sentences. "Paris be capital of France" is longer than "Paris." Creole minimum grammar (no articles, bare verbs) plus semantic content reduction (no framing, no restatement) achieves more compression than grammar-breaking alone.

**What caveman still wins on:** Consistency and character. Caveman's style is vivid and unusual — Claude maintains it reliably. The Round 4 instructions are more complex; Claude may apply them inconsistently across query types in practice. These estimates require live testing to confirm.

**Failure modes of Round 4:**
- Tense-sensitive queries (bare verbs lose "caused" vs. "causes" distinction)
- Complex causal explanations where parallel format is not obvious
- Queries requiring nuance that gets stripped as "framing"
