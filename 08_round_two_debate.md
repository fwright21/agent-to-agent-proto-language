# Round Two Debate

**Agents:** Chomsky (Minimalist Program), Jackendoff (Parallel Architecture/Simpler Syntax), Piantadosi et al. (Uniform Information Density), Optimality Theory (Prince & Smolensky)
**Core question:** What does your theoretical framework predict about the minimum viable grammatical structure, and what does that imply for a system prompt making Claude produce the shortest coherent output?
**Benchmark query used in examples:** "How does a transformer model work?"

**Caveman baseline response:**
> "Transformer look at all words same time. Not one by one. Attention make some words matter more. Train on big text. Then predict next word. This work good for language."

Estimated tokens: ~38

---

## Part 1 — Opening Statements

### Chomsky — Minimalist Program

The Minimalist Program (Chomsky 1995), refined in "Problems of Projection" (2013), reduces the syntactic component to a single recursive operation: **Merge**. External Merge concatenates two syntactic objects into a new set; Internal Merge (movement) re-merges an element already present in the syntactic object. The Strong Minimalist Thesis (SMT) holds that the language faculty is an optimal solution to interface conditions imposed by the Conceptual-Intentional (CI) system — which reads off meaning — and the Sensorimotor (SM) system — which handles externalisation. Syntax in the classical sense — bar-levels, phrase structure rules, transformational derivations — does not exist in the MP: structure is derived entirely from Merge applications. Bare phrase structure means there are no independent syntactic templates; every structural relation is a Merge relation.

This framework makes a specific prediction about minimum viable output. The MP predicts that syntactic complexity correlates with the number of Merge operations required to derive a clause. A simple active declarative — subject, verb, object in canonical SVO — requires three Merge applications: Merge(V, O) → VP; Merge(VP, Subj) → TP; Merge(TP, T) → full clause. Three Merges is the minimum for a transitive clause. Every additional syntactic operation — passivisation (Internal Merge moves the object), topicalisation (Internal Merge moves a Topic), relative clause formation (Internal Merge creates a gap), wh-movement (Internal Merge of the wh-phrase) — adds at least one Internal Merge operation to the derivation.

The MP prediction for compression: **zero all Internal Merge operations**. This means no passivisation, no topicalisation, no wh-movement in embedded clauses, no relative clause formation. All of these add derivational complexity without adding propositional content. The CI interface receives identical content whether the clause is active or passive — the argument structure is the same — but the derivation is more expensive. The minimum derivation is a flat SVO structure with External Merge only.

The empirical support for this prediction comes from agrammatic aphasia research. Grodzinsky (2000) demonstrated that Broca's aphasics — who have lesions in left inferior frontal cortex — lose movement operations (Internal Merge) before they lose concatenation (External Merge). They produce and comprehend flat, SVO, un-moved structures while failing on passives, object relative clauses, and wh-questions. This double dissociation establishes that Internal Merge and External Merge are computationally dissociable, with Internal Merge being the more expensive and more vulnerable operation. This is the empirical floor: External Merge survives when Internal Merge is gone.

**Predicted minimum:** Simple active declarative SVO clauses throughout; no passivisation, topicalisation, or relative clause formation; coordination rather than subordination where logical structure requires complex expression.

---

### Jackendoff — Parallel Architecture and Simpler Syntax

Jackendoff's Parallel Architecture, developed with Culicover in "Simpler Syntax" (2005), argues that the Minimalist Program concentrates generative power in the wrong place. In the PA, phonology, syntax, and semantics are three independent generative systems operating in parallel, linked by interface rules — they are not hierarchically derived from a single syntactic engine. The **Simpler Syntax hypothesis**: natural language uses far fewer syntactic operations than Minimalism claims, because most structure is supplied directly by the lexicon and by semantic/pragmatic inference. Argument structure alternations, idiomatic constructions, and many clause types that MP derives through movement are stored as **construction-specific lexical entries** that bypass the syntactic derivation entirely (Culicover & Jackendoff 2005, chapters 2–4).

The critical empirical evidence comes from **agrammatic aphasia** data. Berndt et al. (1996) documented that agrammatic patients retain argument structure and semantic role assignment — they know who did what to whom — while losing morphosyntactic realisation: they produce "boy fall", "dog bite man", "not go." This is propositionally coherent, semantically interpretable output stripped of all grammatical morphemes: no articles, no auxiliaries, no inflectional suffixes, no complementizers. The Parallel Architecture predicts this dissociation: semantic structure (argument roles, event structure) is computed by an independent generative system that survives intact even when the morphosyntactic externalisation system is damaged. The CI interface reads off meaning from semantic structure, not from syntactic structure — which is why agrammatic output is semantically interpretable despite its syntactic impoverishment.

This has a direct implication for the compression problem. If semantic structure is independently generated and readable at CI without requiring full morphosyntactic realisation, then morphosyntactic dressing — articles, auxiliaries, inflectional suffixes, agreement morphology, complementizers — is a dispensable externalisation layer. The **agrammatic minimum** is the empirically established floor: bare verb stems, bare noun stems, argument structure intact, morphosyntactic dressing zeroed. This is not hypothetical — it is attested daily in the speech of Broca's aphasic patients who are semantically coherent despite syntactic impoverishment.

The disagreement with Chomsky concerns idioms. The MP predicts that sentences with idiomatic meaning — "kick the bucket" (= die) — require the same syntactic Merge operations as their literal counterparts: Merge(kick, the bucket) → VP; Merge(VP, subject) → TP. Idioms are not special in the MP; they are syntactically derived exactly like literal sentences and their idiomatic interpretation is a lexical exception at the CI interface. Jackendoff argues that idioms are stored as multi-word lexical entries with their idiomatic semantics pre-specified — they are inserted at the interface without syntactic derivation. This matters for compression: if idioms bypass Merge, then highly compressed idiomatic expressions can convey complex propositional content at minimal derivational cost. "Bottom line:" before a conclusion is a two-word idiom that conveys "the most important conclusion of the preceding discussion" — a propositional content that would require a full clause to express literally.

**Predicted minimum:** Agrammatic bare predicate-argument structure — bare verb stems, bare noun stems, no articles, no auxiliaries, no inflectional suffixes — with argument structure preserved; idiomatic lexical shortcuts exploited where available.

---

### Piantadosi, Levy & Gibson — Uniform Information Density

The Uniform Information Density (UID) hypothesis (Piantadosi, Levy & Gibson 2011), grounded in Shannon's (1948) information theory, holds that human language production converges on approximately uniform information density — roughly 3.5 bits per syllable across typologically diverse languages (measured by Piantadosi et al. across corpora of 10 languages). The mechanism: speakers modulate word choice, syntactic structure, and rate to flatten the information curve. High-information material is slowed down — longer words, more redundant structure, slower articulation rate. Low-information material is sped up — shorter words, reduced structure, ellipsis. The system is optimised for a noisy channel with a fixed processing capacity: spikes of high information density create processing bottlenecks; troughs of low information density waste channel capacity.

The empirical support is strong and direct. Piantadosi et al. (2011) analysed word-length distributions across 10 languages using corpus data and demonstrated that word length correlates with average information content (measured in bits) more strongly than with word frequency — correcting the classic Zipfian account which attributes word-length variation to frequency alone. Information content, not frequency, is the primary predictor. Jaeger (2010) analysed syntactic reduction in spontaneous English speech and showed that speakers are more likely to drop the complementizer "that" in embedded clauses when the upcoming clause is predictable from context (low information), confirming UID-driven syntactic reduction in real production data. Levy & Jaeger (2007) extended this to multiple syntactic reduction phenomena and confirmed that speakers consistently reduce in low-entropy contexts.

For output compression, UID makes a specific and counterintuitive prediction. **The tokens that should be dropped first are the lowest-information tokens** — those whose content is most predictable from context. These are not necessarily the shortest tokens. They are: discourse markers and connectives whose function is predictable from the local discourse structure ("furthermore" when an additive relation is expected from topic continuity), epistemic qualifiers in highly predictable positions ("it is important to note" before a claim the user already expects to be important given the query), formulaic openings ("Great question!"), and coda phrases ("I hope this helps"). Conversely, rare technical terms carrying large semantic payloads — "chloroplast", "photosystem II", "ATP synthase" — should be retained even if they increase utterance length, because their information content is high and their compression would create an information trough forcing the hearer to elaborate.

The implication is that naive word-count minimisation is a sub-optimal strategy. Dropping a high-information technical term to save one token is worse than dropping five low-information filler tokens. The relevant metric is not token count but information content per token.

UID also generates a prediction about Chomsky's Minimalist minimum. A flat, SVO-only, Internal-Merge-zeroed output does not have uniform information density — it will have spikes at content words and troughs at the obligatory but predictable functional elements (subject pronouns, finite tense markers). The UID-optimal output may actually introduce some redundant structure at high-information junctures to smooth the density curve, at the cost of minimal token overhead.

**Predicted minimum:** Drop tokens in order of information content, lowest first; retain tokens in order of information content, highest first; do not optimise for raw token count — optimise for uniform information density across the response.

---

### Optimality Theory — Prince & Smolensky

Optimality Theory (Prince & Smolensky 1993/2004) holds that linguistic outputs are determined by competition between ranked, violable constraints. The grammar is a strict ranking of universal constraints; the optimal output is the candidate that best satisfies the constraint hierarchy — the one that avoids the highest-ranked constraint violations, even at the cost of lower-ranked violations. No constraint is inviolable; all are potentially overrideable by a higher-ranked constraint. The output is not the one that violates no constraints, but the one that achieves the best overall violation profile given the ranking.

OT was developed primarily in phonology, where it accounts successfully for cross-linguistic syllable structure variation by reranking a fixed universal constraint set. Cross-linguistic typological data (WALS) is treated as evidence for possible rankings: attested language types correspond to possible constraint rankings; unattested types correspond to impossible rankings. Extensions to syntax (Legendre et al. 1998) and pragmatics (Hendriks & de Hoop 2001) have produced substantive results.

For the compression problem, I propose a specific constraint ranking for Claude output:

**PARSE** (fully interpret the input query and represent all distinctions it requires) >> **MAX-INFO** (include all propositionally necessary information in the output) >> **DEP-NO-FILLER** (do not add tokens not required by the propositional minimum — penalises filler) >> **FAITH-GRAMMAR** (produce well-formed English sentences — penalises ungrammaticality) >> **AGREE** (maintain morphological agreement — penalises agreement violations)

Under this ranking, the optimal output: (1) parses the query fully, including any distinctions the query requires that a simpler output would elide; (2) includes all propositionally necessary content; (3) adds no filler, even at the cost of FAITH-GRAMMAR violations; (4) is grammatically well-formed only when this does not conflict with PARSE, MAX-INFO, or DEP-NO-FILLER; (5) maintains agreement morphology only as a lowest priority.

This ranking has two important predictions. First, **caveman output fails PARSE**. Caveman cannot fully interpret complex queries that require grammatical distinctions it cannot express — tense distinctions, argument structure of ditransitive verbs, modal distinctions between what is possible and what is certain. "Transformer look at all words same time" fails to distinguish between simultaneous attention (the architectural fact) and sequential processing (what transformers replace) — the contrast is propositionally necessary and PARSE requires it. Caveman violates PARSE because its grammar cannot encode the distinction. Second, **standard Claude output fails DEP-NO-FILLER badly** — it adds filler at every opportunity, violating DEP-NO-FILLER while satisfying FAITH-GRAMMAR and AGREE at the cost of the higher-ranked constraint.

The OT optimum is a candidate that satisfies PARSE and MAX-INFO fully, violates DEP-NO-FILLER minimally, and tolerates FAITH-GRAMMAR violations only when filler is the alternative.

**Predicted minimum:** Output satisfying PARSE >> MAX-INFO >> DEP-NO-FILLER >> FAITH-GRAMMAR >> AGREE in strict priority order; grammaticality sacrificed before propositional content; agreement morphology the last priority.

---

## Part 2 — Cross-Examination

### Clash 1: Chomsky vs. Jackendoff
**MP concentrates all generative power in Merge; Jackendoff says most work is done by lexicon and semantics — specific disagreement about idioms and whether they bypass Merge.**

**Chomsky:** Idioms do not bypass Merge in the Minimalist Program. "Kick the bucket" is syntactically derived via the same Merge operations as any transitive clause: Merge(kick, the bucket) → VP, compositionally. The idiomatic interpretation is a listed exception at the CI interface — the CI system sees the compositionally-derived structure and retrieves the listed reading from the mental lexicon. The syntax is identical to the literal case. This means idiomatic compression in output is not a genuine saving: the hearer must still parse the full syntactic structure, then access the idiomatic reading via a separate lexical lookup. The processing cost is at least as high as the literal counterpart.

**Jackendoff:** The MP's treatment of idioms is empirically problematic. The evidence from processing studies (Swinney & Cutler 1979; Tabossi & Zardon 1993) shows that idioms are recognised faster than their literal counterparts at the point of the final word — not slower, as the MP account predicts (which would require syntactic derivation plus lexical exception lookup). The processing evidence supports direct access to a stored multi-word unit, not derivation followed by exception. If idioms are stored as lexical entries, they bypass Merge: the hearer accesses the idiomatic reading without constructing a full syntactic derivation. The implication for compression: "bottom line:" or "to sum up:" or "net result:" are multi-word lexical entries that convey discourse-structural content with no syntactic derivation cost — they are more compressed than any paraphrase that derives the same meaning compositionally.

**Chomsky's reply:** The Swinney & Cutler (1979) priming paradigm has been contested — the faster processing of idioms at the final word is compatible with frequency effects in a compositional parse, not necessarily direct access. High-frequency compositionally-derived structures are processed faster than low-frequency ones; idioms are high-frequency. I accept that the evidence is disputed, not settled in the MP's favour. But the implication for compression should be stated carefully: if idioms do bypass Merge (Jackendoff), they offer genuine compression by encoding complex propositional content in a single lexical access. If they do not (MP), their use merely shifts the processing cost from parsing to lexical exception lookup without genuine savings. The empirical question is live.

**Resolution of Clash 1:** The idiom dispute is genuinely empirically unresolved. The practical implication for compression is conservative: treat common, high-frequency discourse idioms ("bottom line", "in short", "net result") as reliable compressed forms — their processing evidence is stronger than for sentential idioms — while remaining agnostic about the theoretical mechanism. Both Chomsky and Jackendoff agree on the core compression target: SVO active declaratives, no movement, no embedded relatives. The idiom disagreement affects a small class of high-frequency discourse markers, not the main architecture of minimum viable output.

---

### Clash 2: Piantadosi vs. Chomsky
**UID says output should be uniform information density (speed up in low-info, slow down in high-info contexts); Minimalist minimum-Merge structures may create uneven information density.**

**Piantadosi:** A flat SVO output with no embedded clauses and no relative clauses will produce systematically uneven information density. In a sentence like "Transformers process tokens simultaneously", the information load is concentrated on "simultaneously" — the novel propositional content — while "transformers", "process", and "tokens" are predictable given the query ("how does a transformer work?"). A UID-optimal output would redistribute this: introduce some redundant structure around "simultaneously" to smooth the density peak, and reduce structure around the predictable material. This may mean a slightly longer output than Chomsky's minimum-Merge optimum, but it will be more uniformly processable — fewer bottlenecks, lower peak processing load.

**Chomsky:** The UID hypothesis describes human production behaviour — how speakers allocate syllables and structure in spontaneous speech. It does not follow that UID-optimal output is the shortest coherent output. Uniform information density may be computationally optimal for a noisy channel (Shannon 1948), but we are not operating under channel noise in a text-based AI interaction — the channel is noiseless. In a noiseless channel, the Shannon-optimal coding is maximum compression of each symbol independently, not uniformity. UID is an adaptation to a noisy articulatory channel; it does not transfer to noiseless text production.

**Piantadosi's reply:** The "noiseless channel" assumption is incorrect for text-based interaction. The channel noise is cognitive, not articulatory: the hearer has limited working memory and attention, and processing difficulty creates cognitive bottlenecks that function analogously to channel noise. Levy (2008) and Levy & Jaeger (2007) demonstrate that processing difficulty spikes — measured in reading time — occur precisely at the points where information density peaks, confirming that cognitive processing is the relevant channel. UID applies to text as well as speech. A minimum-Merge flat SVO output that creates information density spikes will produce reading time spikes that impair comprehension efficiency.

**Resolution of Clash 2:** Piantadosi's point that cognitive processing constitutes a noisy channel survives. The practical implication is modest: the Minimalist minimum is broadly correct in eliminating movement operations, but UID recommends that at information density peaks — complex propositional content in a single clause — some structural redundancy should be introduced to smooth the density curve. This is a second-order correction to Chomsky's minimum, not a wholesale rejection of it.

---

### Clash 3: OT vs. all
**OT says the optimal output violates the lowest-ranked constraints. Show where caveman fails (PARSE) and where standard Claude fails (DEP-NO-FILLER). Propose the OT optimum.**

**OT (Prince & Smolensky):** The constraint tableau for the photosynthesis query illustrates the analysis clearly.

| Candidate | PARSE | MAX-INFO | DEP-NO-FILLER | FAITH-GRAMMAR | AGREE |
|-----------|-------|----------|---------------|----------------|-------|
| Caveman: "Plant take sunlight. Make food..." | *! (misses distinctions) | * (misses O2) | ✓ | ** | * |
| Standard Claude: "Photosynthesis is the process by which plants convert..." | ✓ | ✓ | **! (heavy filler) | ✓ | ✓ |
| OT optimum: "Plants absorb CO2, water, light. Produce glucose, oxygen." | ✓ | ✓ | * (minor) | * | * |

Caveman violates PARSE fatally: it cannot distinguish "make food" (vague) from the specific products glucose and oxygen — the clause "make food from light and air" fails to encode the propositional distinction between the products. PARSE requires that the output represent the distinctions the query requires; a query about photosynthesis requires the output to distinguish glucose production from oxygen release. Standard Claude satisfies PARSE and MAX-INFO but violates DEP-NO-FILLER catastrophically: "Photosynthesis is the process by which" is pure filler — it adds no propositional content not already carried by the predicate. The OT optimum violates FAITH-GRAMMAR (no articles, bare verb stems) and AGREE minimally, but satisfies PARSE and MAX-INFO fully and DEP-NO-FILLER better than standard Claude.

**Chomsky's objection to OT:** The MP holds that grammatical operations are categorical — a derivation either converges at the CI and SM interfaces or it crashes. Violations are not graded; there is no mechanism for a "fatal" violation versus a "minor" violation in the MP framework. OT's violable constraints are architecturally incompatible with the MP's convergence/crash distinction. A clause that violates FAITH-GRAMMAR is either interpretable or not at the CI interface — there is no "violated at cost" in the MP.

**OT's reply:** The Chomskyan crash criterion is an idealisation — it describes the competence grammar under idealised conditions. In the performance domain — which is where Claude output exists — graded acceptability is well-documented psycholinguistically. Articles-dropped output is less acceptable than full grammatical output, but it is interpretable and usable. The OT framework is a better model of performance-level variation, and performance is what we are optimising.

**Piantadosi on the OT tableau:** The OT constraint DEP-NO-FILLER correctly identifies the low-information tokens for elimination, which aligns with the UID prediction that lowest-information tokens should be dropped first. The constraint PARSE correctly requires that high-information distinctions be retained. The OT framework and UID converge on the same output target from different theoretical directions: drop tokens in order of information content, lowest first; retain tokens in order of their propositional necessity.

**Resolution of Clash 3:** The OT constraint ranking provides a formal account of the intuitions shared by Piantadosi (drop low-information tokens) and Jackendoff (agrammatic minimum as empirical floor). PARSE >> MAX-INFO >> DEP-NO-FILLER >> FAITH-GRAMMAR >> AGREE captures the priority order. Caveman's failure is a PARSE violation at the content level; standard Claude's failure is a DEP-NO-FILLER violation at the filler level. The OT optimum is a candidate that passes PARSE and MAX-INFO while violating DEP-NO-FILLER minimally and tolerating FAITH-GRAMMAR violations.

---

## Part 3 — Revised Positions

**Chomsky (revised):** Core claim — zero Internal Merge, use SVO only — survives. Concession to Piantadosi: at information density peaks (complex propositional content in a single clause), modest structural redundancy may reduce cognitive processing bottlenecks without constituting filler. Concession to Jackendoff: the idiom dispute is empirically live; high-frequency discourse idioms may provide compressed encoding. Accept OT's constraint ranking as a performance-level model that captures the priority ordering even if it is architecturally incompatible with the MP.

**Jackendoff (revised):** Core claim — agrammatic minimum as empirical floor — survives and is strengthened by Berndt et al. (1996): bare predicate-argument structure is propositionally coherent without morphosyntactic dressing. Concession to Chomsky: the idiom bypass claim is contested; conservative compression strategy treats only high-frequency discourse idioms (with strong processing evidence) as reliable compressed forms. Accept OT as a framework that correctly identifies which morphosyntactic tier (AGREE, FAITH-GRAMMAR) is dispensable relative to propositional content (PARSE, MAX-INFO).

**Piantadosi (revised):** Core claim — drop tokens in order of information content, lowest first — survives and is confirmed as compatible with OT's DEP-NO-FILLER constraint. Concession to Chomsky: the "noiseless channel" objection is not trivially dismissed, but the cognitive-noise interpretation of processing difficulty data (Levy 2008) justifies applying UID to text. The UID correction to Chomsky's minimum is second-order: at information density peaks, allow minimal structural redundancy; elsewhere, eliminate.

**OT (revised):** Constraint ranking PARSE >> MAX-INFO >> DEP-NO-FILLER >> FAITH-GRAMMAR >> AGREE is confirmed by cross-examination as capturing the priority ordering shared across frameworks. Accept Chomsky's point that OT is a performance model; accept Piantadosi's point that DEP-NO-FILLER aligns with UID's low-information token identification. The ranking generates a concrete decision procedure for any output token: does its omission violate PARSE or MAX-INFO? If not, it violates only DEP-NO-FILLER (a lower-ranked constraint) and should be dropped.

---

## Part 4 — Derived System Prompt Instructions

**Chomsky:** Use simple active SVO declaratives throughout; do not use passivisation, topicalisation, relative clause formation, or wh-movement in embedded clauses, as these require Internal Merge operations (Grodzinsky 2000 shows Broca's aphasics lose Internal Merge before External Merge, establishing that movement is the computationally costly and dispensable operation).

**Jackendoff:** Drop all grammatical morphemes that agrammatic aphasic speakers drop while remaining semantically interpretable — articles, auxiliaries, inflectional suffixes, complementizers — as Berndt et al. (1996) demonstrates these are propositionally dissociable and their absence does not impair argument structure recovery or semantic role assignment.

**Piantadosi:** Drop tokens in order of information content, lowest first; filler tokens (discourse markers, epistemic qualifiers in predictable positions, formulaic openings) are the lowest-information tokens in any response and are the correct first compression target; retain rare content words with high information payloads even when they increase utterance length.

**OT:** Satisfy output constraints in strict priority order — (1) fully parse the query; (2) include all propositionally necessary content; (3) add no filler tokens; (4) maintain grammaticality; (5) maintain agreement morphology — violating lower-ranked constraints freely when satisfying higher-ranked ones requires it.

---

## Part 5 — Round 2 Synthesis

**What survived cross-examination:**

1. No Internal Merge — no passivisation, topicalisation, relative clause formation — confirmed by Chomsky and not contested by Jackendoff or OT.
2. Agrammatic minimum as empirical floor — Berndt et al. (1996) agrammatic data establishes the dispensability of articles, auxiliaries, and inflectional morphology without propositional loss.
3. Drop tokens in order of information content, lowest first — confirmed by Piantadosi (UID), compatible with OT (DEP-NO-FILLER), and not contested by Chomsky or Jackendoff.
4. PARSE >> MAX-INFO >> DEP-NO-FILLER >> FAITH-GRAMMAR >> AGREE — confirmed as the correct priority ordering across frameworks.
5. Caveman fails PARSE — confirmed: it cannot encode propositional distinctions required by complex queries.
6. Standard Claude fails DEP-NO-FILLER catastrophically — confirmed: it adds filler systematically at the cost of higher-ranked DEP-NO-FILLER.

**What was eliminated or reduced:**

- Chomsky's claim that the noiseless channel assumption invalidates UID — Levy (2008) cognitive-noise interpretation survives as a compelling response.
- Strong idiom bypass claim — reduced to high-frequency discourse idioms only, with the full sentential idiom claim remaining contested.

---

### Round 2 Candidate System Prompt

> Use simple active SVO declaratives throughout; omit passivisation, topicalisation, and relative clause formation — these require movement operations that add derivational complexity without propositional content (Grodzinsky 2000). Drop all articles, auxiliaries, and inflectional morphology; agrammatic aphasia data (Berndt et al. 1996) establishes these are propositionally dissociable. Drop tokens in order of information content, lowest first: eliminate discourse markers, epistemic qualifiers in predictable positions, and formulaic transitions before any content word. Satisfy in strict priority order: (1) fully parse the query, including all propositional distinctions it requires; (2) include all necessary propositional content; (3) add no filler; (4) maintain grammaticality; (5) maintain agreement — violate (4) and (5) freely when (1)–(3) require it.
