# Round Three: Full Debate Record

Expanded standalone record of the Round 3 debate. Same content as `11_benchmark_cases.md`, fully elaborated.

**Agents:** Levinson, Bickerton, Lakoff, Montague
**Core question:** What system prompt instruction produces the shortest coherent Claude output?
**Benchmark query:** "What is the difference between RAM and storage?"

**Caveman baseline:**
> "RAM be fast memory. Storage be slow. RAM hold what computer use now. Storage hold everything. RAM small, storage big."
Estimated tokens: ~32

---

## Background: what Rounds 1 and 2 established

Round 1 (Grice, Halliday, Austin/Searle, Goffman) identified linguistic overhead: face-work, meta-commentary, transitions, framing. Their candidate: drop all overhead, assert content directly, stop when done. Estimated 33% reduction vs. caveman on process queries.

Round 2 (Chomsky, Sapir/Whorf, Labov, Pinker) targeted structural overhead: narrative scaffolding (background, significance framing, summary), bad syntactic habits (nominalizations, passive, throat-clearing). Their candidate added syntactic rules to Round 1's structural rules. Estimated 40% reduction on process queries.

Round 3 goes deeper. These agents focus on what can be omitted at the level of grammar and meaning — not just overhead tokens, but grammatical structures and semantic components that consume tokens without proportionate benefit.

---

## Part 1 — Opening Statements (Extended)

### Levinson — Deixis and Contextual Compression

The core insight of pragmatics is that language communicates more than it says. Deixis — words like "this", "it", "the former", "here" — allows a speaker to refer to things established by context without repeating them. Ellipsis — dropping a repeated element because it is recoverable — allows sentences to be shorter when context supplies the missing piece.

Applied to Claude's output: every response is produced in a context set by the user's question. The question names the topic, establishes the frame, and gives Claude information about what the user already knows. Claude can use this context to compress its output in ways that caveman cannot.

**Example — caveman on RAM vs. storage:**
> "RAM be fast memory. Storage be slow. RAM hold what computer use now. Storage hold everything. RAM small, storage big."

The terms "RAM" and "storage" appear five times combined. After the first mention of each, subsequent mentions are deictic — they refer to the already-established topic. They could be replaced:

> "RAM: fast, temporary. Storage: slow, persistent. Former smaller."

"Former" replaces "RAM" in the third sentence — recoverable from the parallel structure. This saves tokens at each substitution point.

But Levinson's deeper point is about content, not just terms. "RAM hold what computer use now" — the user who asked about RAM and storage probably already knows that RAM is used for active processes. This is common knowledge for anyone asking this question. Dropping it saves 7 tokens without losing anything the user needed.

**What caveman drops vs. what Levinson drops:**
- Caveman drops: grammar (articles, auxiliaries, agreement)
- Levinson drops: repeated terms (replaced by deixis), common knowledge content (inferrable from topic)

These are different classes of tokens. Levinson's compression is potentially more powerful because it targets meaning, not just form.

---

### Bickerton — The Creole Grammar Target

Bickerton's creole minimum is the theoretical floor of grammatical stability. It is the grammar that emerges when a community must communicate without a shared language — minimal, regular, learnable without instruction.

**Creole minimum features:**
1. SVO word order (maintained — essential for comprehension)
2. No articles (the, a, an) — omitted
3. No inflectional morphology (past -ed, plural -s, progressive -ing) — omitted
4. No embedded clauses — replaced by coordination
5. Minimal prepositions — kept only when necessary for meaning

**Standard English:** "The plants absorb sunlight, carbon dioxide, and water through their leaves."
**Caveman:** "Plant take sunlight."
**Creole minimum:** "Plants absorb sunlight, CO2, water."

The creole minimum is shorter than standard English and longer than caveman on a per-sentence basis — but produces shorter overall output because it is not broken. Broken grammar (caveman) forces short sentences because longer broken sentences become unreadable. Creole grammar allows longer sentences that carry more information per token, producing fewer total sentences.

**Token analysis:**
- Standard English "The plants absorb sunlight": 5 tokens (The + plants + absorb + sunlight + period)
- Caveman "Plant take sunlight": 3 tokens
- Creole minimum "Plants absorb sunlight": 3 tokens (same as caveman, but grammatically stable)

For short simple sentences, caveman and creole minimum are equivalent. For complex content, creole minimum wins because it can construct dense parallel structures that caveman cannot.

---

### Lakoff — Framing Overhead as a Token Class

Rounds 1 and 2 targeted content overhead (unnecessary information) and syntactic overhead (longer constructions). Lakoff targets a third class: framing overhead — tokens that encode the pedagogical structure of the explanation rather than the explanation itself.

**Classes of framing overhead:**

1. **Analogical framing:** "RAM is like a desk where you keep things you're working on." Cost: 14 tokens. Information added: zero (for a user who can understand "fast temporary memory"). This is the most expensive form of framing overhead.

2. **Pedagogical orientation:** "To understand the difference between RAM and storage, it helps to first think about how computers use memory." Cost: 20 tokens before content starts. This is standard Claude output on technical topics.

3. **Conceptual scaffolding:** "At a high level, both RAM and storage serve different purposes in the memory hierarchy." Cost: 16 tokens of setup before any useful content.

4. **Evaluative framing:** "This is why RAM is so important for performance." Cost: 8 tokens of significance framing that adds no factual content.

Caveman drops most framing because it cannot construct the complex phrases needed. But caveman also drops some content along with the framing, producing compressed but sometimes incomplete output. Lakoff's instruction removes framing while keeping content — achieving caveman's savings without caveman's content losses.

**Testable rule:** A sentence is framing overhead if and only if deleting it leaves the factual content of the response unchanged. This rule is testable: read the response without the sentence; if you have lost a fact, the sentence was not framing. If you have not, it was.

---

### Montague — Semantic Redundancy Targeting

Montague's formal semantics treats each semantic component of a response as either contributing new information to the user's model or not. Components that do not contribute new information are semantically redundant and can be dropped without loss.

**Three categories of semantic redundancy in Claude's output:**

1. **Question-structure restatement:** When asked "What is the difference between RAM and storage?", the phrase "RAM and storage differ in the following ways" restates the structure of the question. The user already knows there is a difference — they asked about it. These tokens are entirely redundant.

2. **Contrastive connector redundancy:** When a response uses parallel structure ("RAM: fast. Storage: slow"), the contrastive relation is encoded by the layout. An explicit "in contrast" or "whereas" is then redundant — the format already signals contrast.

3. **Introductory topic restatement:** "RAM, or Random Access Memory, is..." — the definition of the acronym is often redundant when the user has used the term correctly in their question. If they asked about RAM, they know what RAM stands for.

**Applying to caveman:**
Caveman's output "RAM be fast memory. Storage be slow." encodes the contrastive relation implicitly through juxtaposition. No explicit connector. Montague approves. But "RAM hold what computer use now" — this encodes a functional description (active process storage) that is partially derivable from "fast, temporary memory" already stated. The content is redundant with what the response has already said.

The deepest compression identifies not just overhead tokens but redundant content tokens.

---

## Part 2 — Cross-Examination (Extended)

### Clash 1: Levinson vs. Bickerton

**Levinson challenges Bickerton:**

Your creole grammar produces fixed-format output regardless of context. But your system is a uniform grammar constraint — it does not adapt to what the user already knows. My approach is dynamic: compress more when context is rich, compress less when context is thin.

For a user who has never heard of RAM, "RAM: fast, temporary, active data" may be insufficient even in creole grammar — the user needs more content, not less grammar. For an expert user, "RAM faster, volatile; storage slower, persistent" might be the right level. Your grammar constraint is content-neutral, which means it produces the same format for novice and expert users.

**Bickerton responds:**

You are describing a limitation that applies to all fixed instructions, not specifically to creole grammar. Any system prompt that does not have access to user expertise level will produce output that is sometimes over-compressed for novices and under-compressed for experts.

My point is simpler: creole grammar produces output that is reliably shorter than standard English and reliably more parseable than caveman. It is a floor improvement, not a ceiling optimization. Whether it is the right level for every user is a separate question from whether it saves tokens vs. caveman — and it does.

Your contextual deletion requires Claude to model user knowledge, which it may do poorly. My grammar constraint requires Claude to follow a format rule, which it can do reliably. Reliability of application matters for whether the instruction actually produces shorter output in practice.

**Levinson's response:**

I accept that reliability is important. I narrow my instruction to the cases where contextual deletion is reliable: repeated terms from the question (replace with pronouns), and content that is common knowledge for the explicitly stated topic. I do not claim to model user expertise — I claim to use the question structure itself as the model.

---

### Clash 2: Lakoff vs. Montague

**Lakoff challenges Montague:**

Your semantic redundancy analysis is more powerful than mine in theory. Dropping content that is already present in the user's knowledge model is deeper compression than dropping framing. But your instruction requires Claude to model the user's knowledge state — which is exactly the brittleness problem Levinson just encountered.

My framing removal is conservative: I only drop tokens that contain no factual content. This is testable and reliable. Your redundancy analysis requires Claude to determine which facts are "new" to the user — a judgment that is context-dependent and often unreliable.

**Montague responds:**

I am not claiming Claude should model general user knowledge. I am claiming Claude can use the question structure as a proxy. When the user asks "what is the difference between X and Y", the question structure reveals what the user knows (that X and Y exist and are different) and what they want to know (the content of the difference). This is not a model of user expertise — it is a structural inference from the question.

The specific case of question-structure restatement ("RAM and storage differ in the following ways") is always safe to cut because it is always redundant with the question. No knowledge modeling required.

**Lakoff:**

I accept the narrow version of your claim. Question-structure restatement is always redundant and always safe to cut. Your broader semantic redundancy analysis is not. I will add question-structure restatement to my list of framing overhead — it is a special case of my rule: a sentence that contains no new factual content relative to the question.

**Resolution:** Both agents converge. Framing overhead (Lakoff) and question-structure restatement (Montague's reliable case) are combined into one rule: cut any sentence that adds no factual content that was not already present in the question or a prior sentence.

---

## Part 3 — Revised Positions (Extended)

### Levinson (revised)

Original position: use pronouns and ellipsis; drop common knowledge content.

Revision: narrow to reliable cases only. Two instructions that are always safe:
1. Replace repeated terms with pronouns or ellipsis when the referent is unambiguous from sentence sequence.
2. Drop content that is explicitly stated or entailed by the question.

Drop: the broader claim about dropping "common knowledge for the topic" — this requires knowledge modeling and is unreliable.

Revised instruction: "Replace repeated noun phrases with pronouns when the referent is clear. Do not state content that is entailed by the question."

---

### Bickerton (revised)

Position held on creole grammar. It is the most reliable compression mechanism because it is a rule about form, not content.

Addition: integrate Levinson's reliable pronoun-replacement rule into the creole minimum. The creole minimum can use pronouns — creoles do use anaphoric reference. Adding this makes the creole minimum slightly more aggressive without losing reliability.

Revised instruction: "Write in minimal English: no articles, no inflection, no embedded clauses. Use pronouns for repeated referents. Short parallel statements."

---

### Lakoff (revised)

Original position: no analogies, no framing, cut any sentence with no factual content.

Addition: the combined rule with Montague — cut any sentence that adds no factual content not already present in the question or a prior sentence. This is the most precise version of the framing removal rule.

Revised instruction: "Cut any sentence that contains no factual content beyond what is already in the question or a previous sentence. No analogies, no framing, no pedagogical orientation."

---

### Montague (revised)

Original position: drop semantically redundant components.

Narrowed to: drop question-structure restatements (always safe); avoid parallel connector words when format already encodes the parallel relation (safe when structure is clear); drop summary sentences (the summary is never new information).

Revised instruction: "Do not restate the question structure. Let parallel format signal contrast — do not add 'in contrast' or 'whereas' when the layout already shows it. No summary sentences."

---

## Part 4 — Draft System Prompts (Extended)

### Levinson's draft

> Replace repeated noun phrases with pronouns when the referent is clear from sequence. Do not state content that is entailed by the question — if the user asked about a difference, do not state that there is a difference. Start with the content. Stop when the content is complete.

**Estimated token reduction:** 10-15% vs. caveman on comparison queries (mostly from pronoun replacement and entailment-dropping).

---

### Bickerton's draft

> Write in minimal English: no articles (a, the), no verb inflection (drop -s, -ed, -ing where possible), no embedded clauses (use coordination: "and", "but", "or" instead). Use pronouns for repeated referents. Short parallel statements. This is stripped English, not broken English — word order remains correct.

**Estimated token reduction:** 20-30% vs. caveman on most query types. Article removal alone saves 1-2 tokens per sentence.

---

### Lakoff's draft

> No analogies unless explicitly requested. No framing sentences ("to understand X, think of Y"). No pedagogical orientation before content. Cut any sentence that adds no factual content beyond what is already in the question or a prior sentence in this response.

**Estimated token reduction:** 15-25% vs. caveman on technical explanations where framing overhead is highest.

---

### Montague's draft

> Do not restate the question structure — if asked about a difference, give the attributes directly without announcing there is a difference. Use parallel format for comparisons: the format encodes the relation, no connector needed. No summary sentences at the end of a response.

**Estimated token reduction:** 5-10% vs. caveman (smaller than other agents because it targets a specific class of tokens rather than a broad class).

---

## Part 5 — Synthesis: Round 3 Candidate

The combination that produces the most token reduction without coherence loss:

1. Bickerton's creole grammar (article removal, inflection removal, no embedding) — highest-yield reliable compression
2. Levinson's pronoun replacement — integrates naturally with creole grammar
3. Lakoff's framing removal — removes token class not addressed by grammar rules
4. Montague's question-structure rule — removes the specific redundancy of restating the question

Combined candidate:

> Write in minimal English: no articles, no verb inflection, no embedded clauses. Use pronouns for repeated referents. Short parallel statements.
>
> Drop framing. No analogies unless asked. No pedagogical orientation. Cut any sentence that adds no factual content beyond what is in the question or a prior sentence.
>
> Do not restate the question structure. For comparisons, use parallel format — the format encodes the contrast.

---

## Benchmark Results (Extended)

### Query: "What is the difference between RAM and storage?"

**Caveman:** ~32 tokens
**Round 3 candidate:** ~16 tokens (estimated)

Simulation:
> "RAM: fast, temporary, holds active data. Storage: slow, persistent, holds all data. RAM smaller."

Token count: RAM(1) + :(1) + fast(1) + temporary(1) + holds(1) + active(1) + data(1) + Storage(1) + :(1) + slow(1) + persistent(1) + holds(1) + all(1) + data(1) + RAM(1) + smaller(1) = ~16 tokens

Caveman achieves 32 tokens using broken grammar for 5 sentences. Round 3 achieves 16 tokens using creole grammar for 3 sentences with denser content per sentence.

### Query: "Explain photosynthesis."

**Caveman:** ~42 tokens
**Round 3 candidate:** ~18 tokens (estimated)

Simulation:
> "Plants absorb sunlight, CO2, water. Produce sugar, oxygen. Sugar fuels plant."

This is 3 sentences vs. caveman's 8. Each sentence carries more content. The ellipsis in sentence 2 ("Produce" with subject dropped — recoverable from sentence 1) saves 1 token. No articles, no framing, no redundancy.

### Query: "Should I use Python or JavaScript for a web scraper?"

**Caveman:** ~28 tokens
**Round 3 candidate:** ~15 tokens (estimated)

Simulation:
> "Python. Better libraries (requests, BeautifulSoup). Less setup than JS."

Bare recommendation, one-phrase justification, one comparative note. Complete. Nothing added beyond what was asked.

---

## Honest assessment of Round 3

**Where Round 3 beats caveman decisively:** process explanations, comparisons, recommendations. The creole grammar plus framing removal produces approximately 50% token reduction on these query types.

**Where Round 3 matches caveman:** simple factual queries. Both tend toward bare answers. Caveman sometimes adds unnecessary broken sentences; Round 3 sometimes adds a minimal grammatical sentence where bare output would suffice.

**Where Round 3 may fail:** tense-sensitive queries. "The company was founded in 1998" — bare verb "founded" loses the past tense. This may matter for historical queries. Bickerton's concession: add tense back when temporal distinction matters.

**Consistency concern:** Caveman's broken grammar is vivid and unusual — Claude applies it reliably because the style is distinctive. Round 3's instructions are more subtle and Claude may drift toward longer output on extended conversations. This is the main practical risk.

**Overall verdict:** Round 3 is the strongest candidate on raw token count. The judge panel in Round 4 will determine whether it holds up across the full benchmark suite and whether the consistency concern is significant.
