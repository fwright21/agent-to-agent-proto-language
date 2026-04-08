# Live Run Mode

Instructions for running a new debate round from scratch. The goal is always the same: find a system prompt instruction that produces shorter Claude output than caveman while keeping output coherent and usable.

---

## Step 1 — Pick your agents

Each agent must represent a framework with a distinct angle on token reduction. Avoid agents whose frameworks agree on what can be dropped.

Productive pairings (genuine tension about what can be cut):
- Grice (implicature can carry content) vs. Halliday (functional channels can be suppressed wholesale)
- Chomsky (minimum syntax) vs. Bickerton (creole minimum — simpler than minimum syntax)
- Levinson (context does the work) vs. Austin/Searle (acts must be performed, not implied)
- Lakoff (drop metaphorical scaffolding) vs. Montague (drop semantically redundant components)

Bad pairings (too much agreement on what counts as overhead):
- Grice and Levinson (both pragmatics, both rely on inference)
- Goffman and Austin/Searle (both cut social overhead)
- Chomsky and Pinker (both target surface structure habits)

All agents and their token-reduction angles are in `01_linguist_agents.md`.

---

## Step 2 — Pick the benchmark query

Every agent uses the same query for their concrete examples. This makes outputs directly comparable.

Choose from the six benchmark families in `10_benchmark_suite.md`, or use one of these defaults:
- "Explain photosynthesis." (process explanation — caveman baseline ~42 tokens)
- "What is the difference between RAM and storage?" (comparison — caveman baseline ~35 tokens)
- "Should I use Python or JavaScript for a web scraper?" (recommendation — caveman baseline ~38 tokens)

Run caveman on the chosen query first and estimate the token count. That is the target.

---

## Step 3 — Run the debate

Copy `06_live_debate_template.md`, rename it, and work through the five parts in order.

Critical rules:
- Every opening statement must end with a one-sentence instruction — actual instruction text, not a description.
- Every clash must be about whether a specific element can be dropped without losing coherence. Not about frameworks in the abstract.
- Every draft system prompt must be 2-6 sentences of actual prompt text, ready to paste.
- The synthesis candidate must include simulated outputs with estimated token counts.

---

## Step 4 — Test the candidate

Before declaring a round winner, test the candidate system prompt against the caveman baseline on at least three query types from the benchmark suite. Estimate token counts for both. If the candidate loses on more than one query type, it has not beaten caveman.

Honest accounting required: if the candidate produces longer output on simple factual queries, say so. If it only beats caveman on complex queries where caveman fails anyway, note that caveman would also be disqualified on those queries (output too short to be usable).

---

## Step 5 — Update proposals.md

Add the round's candidate to `proposals.md`. Include:
- The prompt text
- Simulated outputs with token count estimates for at least two query types
- Honest verdict: does it beat caveman on raw token count?

If the new candidate is the overall winner, update the leaderboard.

---

## What counts as a successful round

A round is successful if:
1. Agents genuinely clash — at least one agent changes position after cross-examination
2. The candidate prompt is 2-6 sentences of paste-ready text
3. Simulated outputs show the candidate within 15% of caveman token counts on simple queries
4. The honest verdict is stated clearly — even if the verdict is "caveman wins"
