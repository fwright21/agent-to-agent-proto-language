# Round Three Agent Profiles

Standalone reference for Round 3 agents. Full research questions focused on token reduction.

---

## Levinson — Pragmatics and Deixis

**Framework:** Deixis and implicature do communicative work without consuming tokens. Context resolves ambiguity that explicit language cannot. The question is how much Claude can leave unsaid because the user already has it from context.

**Token-reduction research question:** How much can Claude rely on implicature and deictic reference to say less? When the user asks about RAM and storage, every subsequent use of "RAM" and "storage" is a repeated term — replaceable with pronouns or ellipsis. When the topic is explicitly stated in the question, common knowledge about that topic need not be restated. How aggressively can Claude exploit this?

**What caveman drops:** Most discourse-level overhead. Face-work, transitions, meta-commentary.

**What caveman keeps that Levinson would drop:** Repeated noun phrases ("RAM hold what computer use now. Storage hold everything. RAM small, storage big." — three uses of RAM, two of storage). Deixis would replace most of these.

**One-sentence instruction:** "Replace repeated terms with pronouns. Drop content that is common knowledge for the topic named in the question."

**Failure mode:** If Claude misjudges what the user already knows and drops content they needed, the output is insufficient. This instruction requires conservative application — drop only what is provably recoverable from the question structure or common knowledge, not from assumed user expertise.

---

## Bickerton — Creolistics and Bioprogram Hypothesis

**Framework:** Creoles are the simplest grammatically stable languages. They consistently exhibit minimal grammar: SVO order, no inflection, no articles, no embedded clauses, coordination only. This is the floor of grammatical stability — below this, language becomes harder to parse, not easier.

**Token-reduction research question:** What is the creole minimum for English output — the shortest grammatically stable form that a reader can parse without effort? Caveman goes below this minimum and pays a comprehension cost. The creole minimum is shorter than standard English but above the caveman floor. Is it short enough to beat caveman on token count?

**Creole minimum features:**
- No articles (the, a, an)
- No verb inflection (plural -s, past -ed, progressive -ing)
- No embedded clauses (relative clauses, that-clauses)
- Coordination only (and, or, but)
- SVO order maintained

**What caveman drops that creole keeps:** SVO order. Subject-verb agreement (partially — caveman breaks it; creole minimum allows bare verbs that work in SVO context).

**What creole minimum drops that caveman keeps:** Caveman still uses some articles and some inflections inconsistently. Creole minimum drops them systematically.

**One-sentence instruction:** "Write in minimal English: no articles, no verb inflection, no embedded clauses. Short parallel statements. Nouns, adjectives, bare verbs."

**Estimated token savings vs. standard English:** 15-25% from article and inflection removal alone.

**Failure mode:** Works well for factual and comparative content. May fail for nuanced content where inflection (tense, aspect) carries necessary meaning — e.g. "X caused Y" vs. "X causes Y" is a meaningful distinction that bare verb forms lose.

---

## Lakoff — Cognitive Linguistics and Conceptual Metaphor

**Framework:** Abstract thought is structured through conceptual metaphors. Claude's explanations often encode the pedagogical metaphor ("think of it as", "imagine", "it's like") before giving content. These framing tokens consume budget without adding information.

**Token-reduction research question:** Which conceptual metaphors and framing structures in Claude's responses bloat token count? Analogies are the primary target — "RAM is like a desk" costs 6 tokens and adds no information to the definition. Pedagogical orientation ("to understand X, it helps to first consider Y") costs 10+ tokens before any content starts. Framing sentences ("what this means in practice is") cost 5+ tokens. All are removable without losing content.

**Testable rule for framing overhead:** A sentence is framing overhead if removing it leaves the factual content of the response unchanged. Any such sentence should be cut.

**What caveman drops:** Most analogy and framing language — caveman cannot construct the complex phrases needed for analogies.

**What caveman keeps that Lakoff would drop:** Caveman sometimes produces evaluative framing: "This work good for language." This sentence frames the significance of transformers rather than adding content. Lakoff would drop it.

**One-sentence instruction:** "No analogies unless asked. No framing sentences. Cut any sentence that contains no factual content."

**Failure mode:** Some analogies are the most efficient way to convey a concept — "RAM is like working memory" communicates the temporal/active dimension efficiently. A blanket analogy ban may make some explanations longer by forcing Claude to construct the same concept without the analogy.

---

## Montague — Formal Semantics and Compositionality

**Framework:** The meaning of a complex expression is a function of its parts. Which parts of a Claude response are semantically redundant — encoding meaning already present in the question or in prior sentences?

**Token-reduction research question:** Which semantic components of Claude's output are recoverable from the question structure and can be dropped? When asked "What is the difference between X and Y?", any token that encodes "there is a difference between X and Y" is redundant — the user already knows this from their question. When the response uses parallel structure (RAM: A. Storage: B), the contrastive relation is encoded by the format — an explicit "in contrast" is redundant.

**Specific redundancy cases:**
- "X and Y differ in the following ways" — restates the question structure
- "This means that" — announces an inference the reader can draw
- "In other words" — announces a restatement
- "To summarize" — announces that what follows is a summary (the summary itself is sufficient)
- "As I mentioned above" — cataphoric reference that assumes a longer text than necessary

**One-sentence instruction:** "Do not restate the question structure. Use parallel format for comparisons — the format encodes the contrast. Do not announce inferences, restatements, or summaries — make them."

**Failure mode:** Parallel format without explicit connectors can be ambiguous when the items being contrasted are not clearly parallel in the user's mental model. "RAM: fast. Storage: persistent." — the user must infer that these are the key distinguishing attributes, not just random facts about each. If the contrast is non-obvious, removing the contrastive connector loses necessary information.
