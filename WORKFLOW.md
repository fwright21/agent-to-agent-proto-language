# Coordination Protocol Compression
# A Dissertation-Style, Presentation-Ready Workflow Report (with Debate Rounds)

This is the primary “how this repo works” document for GitHub readers.

Date: 2026-04-12  
Project focus: **compressing agent-to-agent coordination** (INTERNAL), while keeping human output readable (FINAL)

---

## Abstract (read this like the first slide)

This project asks one practical question:

> Can a team of AI agents coordinate using *much less text* (fewer tokens), without losing their ability to disagree, repair mistakes, revise plans, and still produce a good final decision?

To make this measurable, every run forces two channels:

```text
INTERNAL:
(the agents’ coordination transcript)
FINAL:
(the human-facing recommendation)
```

We compress and measure **INTERNAL**. We keep **FINAL** readable on purpose.

How we generate solutions is also deliberate: we use a **linguist debate panel** to argue about what must stay explicit in coordination, then we turn the winning ideas into a protocol we can benchmark.

The headline result so far:

- Adding *labels and fields* (typed schemas) does not automatically save tokens; sometimes it costs more than plain English.
- A **proto-language** (PCL-1: short act codes + positional arguments) can cut INTERNAL tokens dramatically while remaining mostly consistent.
- A very dense code format (SDC-1) can be even cheaper, but quality can drop.

This report is self-contained. You do not need to open other files to understand the linguists, the debates, the protocols, or the results.

---

## Table of contents (the exact structure requested)

1. Problem  
2. How we tackle it: debate system (with linguists) + benchmark system  
3. Outcome of each round (each protocol created, and why)  
4. Step-by-step procedure  
5. Results  
6. Discussion  
7. Next steps  

---

## Repo map (where things live)

If you only open a few files, open these:

- `WORKFLOW.md`: this document (full methodology + reproduction + results context)
- `run_tests.py`: benchmark harness (cases, conditions, parsers, scoring)
- `README.md`: quick overview and entry points
- `round_04_linguistic_revision_2026-04-08/`: Round 4 debate + reports
- `round_05_proto_language_and_dense_code_2026-04-08/`: Round 5 debate + reports
- `dashboard_trusted.html`: small “shareable” dashboard (openai_exact runs)
- `combined_round4_round5_dashboard.html`: side-by-side comparison dashboard
- `scripts/regenerate_dashboards.sh`: regenerates dashboards from saved markdown reports
- `render_benchmark_html.py`, `render_multi_dashboard.py`, `render_combined_dashboard.py`: HTML generators

“Trusted” vs “historical” HTML:

- `dashboard_trusted.html` is intended for GitHub sharing (uses only `openai_exact` reports).
- `dashboard_historical.html` is for local exploration (mixed runs) and is ignored by git.

---

## 1. Problem

### 1.1 The real problem (in simple language)

Multi-agent systems waste a lot of tokens on coordination. The waste looks like:

- repeating the goal
- “nice” phrasing (polite acknowledgements)
- long explanations of shared context
- unclear disagreements (“I’m not sure”) instead of explicit objections (“I object to claim c3 because…”)
- meandering planning (“first I’ll…”) instead of explicit next actions

In a production setting, this waste is money and latency.
And from a research point of view, it is also hard to score: free-form text is hard to validate.

### 1.2 What we mean by “coordination protocol”

A coordination protocol is simply a rule for how agents are allowed to talk to each other.

It answers questions like:

- How does an agent *make a claim*?
- How does another agent *object* (and what must be explicit)?
- How do we attach *evidence* to a claim?
- How do we *revise* a claim without losing track of the original?
- How do we handle “we can’t safely compress this” (an escape hatch)?
- How do we handle real-world stress: *interrupts*, scope shifts, nuance?

### 1.3 The success definition (what counts as a win)

We are not trying to create the shortest strings possible.
We are trying to maximize this tradeoff:

- **INTERNAL gets shorter** (token savings)
- **coordination still works** (clear claims, objections, evidence, revisions, next actions)
- **repair cost stays low** (we don’t save tokens but then burn them all on clarifying questions)
- **FINAL stays useful** (the human gets an actionable answer)

### 1.4 Why INTERNAL vs FINAL is non-negotiable

If we compress FINAL, we can “win” by making the human output unreadable.
That is not the question.

So every run forces the same shape:

```text
INTERNAL:
(compact, protocol-governed coordination)
FINAL:
(normal readable recommendation)
```

This is what makes the benchmark honest.

---

## 2. How we tackle it: debate system + benchmark system

This section is the “methodology” chapter, but written like you’d explain it in a presentation.

### 2.1 The overall workflow (one sentence)

We run debates to invent protocols, then we benchmark protocols to see what actually works.

### 2.2 The debate system (how the linguists generate protocol candidates)

Think of each debate round as a structured meeting with one output:

> A concrete protocol spec we can test.

The debates are not academic for their own sake. The “linguists” are used as *personas* that protect different practical properties of coordination language.

#### 2.2.1 Debate round format (what happens every time)

Each round follows the same five parts:

1) **Opening proposals**  
Each linguist says what they think is broken and proposes a fix.

2) **Cross-critique**  
They challenge each other: “That’s too cryptic”, “That will cause repair turns”, “That loses references”, “That will drift”.

3) **Revision pass**  
They adjust proposals based on the strongest criticism.

4) **Draft protocol text**  
Not theory: actual rules, grammar, required fields, examples.

5) **Synthesis**  
We pick one candidate protocol that is small enough to be learnable and strict enough to benchmark.

#### 2.2.2 The linguists (who they are and what they fight for)

Below I describe each linguist in plain language, plus how that showed up in our protocol decisions.

##### Noam Chomsky — “Structure prevents ambiguity”

- What he cares about: clear roles and references (“what is this message pointing at?”).
- What he pushes: consistent structure and explicit targets/ids.
- In debates, he tends to say: “Don’t let the protocol become fragments; if references break, coordination breaks.”
- What he protects us from: *cheap-looking compression* that becomes impossible to interpret or debug.

##### Joseph Greenberg — “Don’t delete universal coordination functions”

- What he cares about: a minimal inventory of functions that show up everywhere.
- What he pushes: keep a small core set: claim, objection, evidence, revision, question, next action, escape.
- In debates, he tends to say: “You can compress the surface, but you can’t delete functions coordination needs.”
- What he protects us from: pruning message types until collaboration stops working.

##### Sperber & Wilson — “Inference is not free”

- What they care about: what is safe to leave implicit vs what will cause confusion.
- What they push: remove redundancy, but add explicit intention where repair would otherwise explode.
- In debates, they tend to say: “This looks short, but the listener will have to guess; guessing costs turns.”
- What they protect us from: protocols that look compressed but create lots of repair questions.

##### Steven Piantadosi — “Optimize information per token”

- What he cares about: tokens that carry real information vs filler.
- What he pushes: delete overhead first; keep small disambiguators.
- In debates, he tends to say: “Keep the cheap tokens that prevent expensive mistakes.”
- What he protects us from: removing tiny cues that later cost many tokens to repair.

##### Derek Bickerton — “Proto-language can be stable”

- What he cares about: reduced grammar that is still learnable and consistent.
- What he pushes: a small vocabulary of acts + fixed word order (positional grammar).
- In debates, he tends to say: “Stop writing English inside fields; make the protocol itself carry meaning.”
- What he protects us from: protocols that are “structured English” but still verbose.

##### George Lakoff — “Framing and polite talk is wasted”

- What he cares about: rhetorical packaging (“Here’s why this matters…”) that adds tokens without helping coordination.
- What he pushes: action-first content; ban unnecessary explanation inside protocol lines.
- In debates, he tends to say: “Keep facts and directives; delete story-telling.”
- What he protects us from: coordination becoming “mini-essays”.

##### M.A.K. Halliday — “Drop interpersonal stance; keep minimal cohesion”

- What he cares about: separating useful content from social / stance language.
- What he pushes: delete hedging/politeness; keep only what helps multi-turn coherence.
- What he protects us from: wasting tokens on tone rather than coordination.

##### Prince & Smolensky — “Make tradeoffs explicit”

- What they care about: you can’t optimize everything; you need priorities.
- What they push: recoverability > compression > style.
- What they protect us from: rigid rules that fail under exceptions.

##### Ray Jackendoff — “Keep semantic mapping and reference clarity”

- What he cares about: the trace should still map to the actual evolving task state.
- What he pushes: explicit target anchors; revisions must point to what they revise.
- What he protects us from: compressed logs that cannot be followed when debugging.

### 2.3 The benchmark system (how we test protocols)

We treat the benchmark as evidence. The debate invents ideas, but the benchmark decides whether those ideas actually save tokens and still work.

#### 2.3.1 Benchmark tasks (what agents have to do)

The first suite uses narrow, structured tasks so we can score consistently.
Each case forces specific “moves” (claim, objection, evidence, revision, final decision).

Cases in the first suite:

1. **Protocol rule proposal** (design a rule, object, revise, decide)  
2. **Missing-evidence repair** (ask for evidence, supply evidence, decide)  
3. **Fallback trigger** (detect nuance risk, decide to escape or stay compressed)  
4. **Benchmark-scope decision** (choose narrow vs broad benchmark, revise to compromise)  
5. **Human interrupt during execution** (incorporate a new constraint without losing state)  

#### 2.3.2 What we measure (the “scoreboard”)

For each condition × case, we compute:

1) **Internal Tokens** (INTERNAL only; this is the main cost)  
2) **Compliance** (did the agents follow the required format?)  
3) **Repair turns** (how often did they need to ask/escape?)  
4) **Final quality** (simple proxy: is FINAL actionable and complete?)  

---

## 3. Outcome of each round (protocols created, and what the debates decided)

This is the part you would present as “what happened, step-by-step”.

### 3.0 The baseline (before any protocol): plain English

In the baseline, agents talk normally:

```text
AgentA: I think we should do X.
AgentB: I object because Y.
AgentC: Here is evidence Z.
AgentD: Let’s revise and decide.
```

This is reliable, but it drifts into verbosity and is hard to validate.

### 3.1 Round 4: RCCE-1 → ATRCE-2 (the “interrupt” problem)

#### 3.1.1 What RCCE-1 was trying to do

RCCE-1 (“Relevance-Core Coordination English”) is a typed schema: every line declares its function.

```text
TYPE: field=value; field=value; field=value
```

RCCE-1 types and required fields:

```text
CLAIM: id, topic, content
EVID: target, source, content
OBJ: target, reason, content
REV: target, change, content
ASK: target, need
CONF: target, level
NEXT: owner, action
ESCALATE: reason            (RCCE-1 initially allowed target to be optional)
```

The design hope was simple:

- Remove greetings and framing.
- Make references explicit (`id` / `target`).
- Make the whole trace easy to parse and score.

#### 3.1.2 What went wrong (the benchmark signal that triggered debate)

The early signal was:

- tokens went down (good)
- repair turns went up (bad)
- weakest behavior appeared when the task was “boundary-like”: interrupts and fallback moments

In normal debate, “interrupt” turns often got expressed as a confusing mix of question + directive.
That is where the linguist panel stepped in.

#### 3.1.3 What the Round 4 debate actually argued (in meeting-minutes form)

This is the core of the Round 4 debate, paraphrased in simple language:

- Chomsky: “The schema is fine, but in interrupts the *speech act* is unclear. An interrupt is not a question. We need a distinct type.”
- Sperber & Wilson: “If you don’t label intention on high-risk turns, other agents must infer it, and inference creates repair turns.”
- Bickerton: “The protocol is stable in normal cases, but boundary events need a minimal dedicated grammar. Add one act, don’t add ten.”
- Lakoff: “Even inside schema fields, agents still write mini-explanations. Ban framing and force action-first content.”

Cross-critique outcome (the group agreement):

- The main failure was not “English is too long”.  
  It was: **the protocol overloaded `ASK` and blurred whether a line was a request, a revision, or an external directive.**

#### 3.1.4 The protocol produced by Round 4 debate: ATRCE-2 (full spec)

ATRCE-2 (“Act-Typed Relevance Coordination English”) is RCCE-1 plus one essential new type and stricter rules.

```text
Protocol: Act-Typed Relevance Coordination English (ATRCE-2)

Line grammar:
TYPE: field=value; field=value; ...

Allowed types and required fields:
CLAIM: id, topic, content
EVID: target, source, content
OBJ: target, reason, content
REV: target, change, content
ASK: target, need
CONF: target, level
NEXT: owner, action
ESCALATE: target, reason
INTERRUPT: source, priority, directive

Rules:
1. One line, one act.
2. One message, one purpose.
3. Use ASK only for missing information.
4. Use INTERRUPT only for external directive / priority shifts.
5. Use ESCALATE only when schema cannot safely encode meaning; always anchor to target.
6. Action-first content: no framing / politeness text inside content/action fields.
7. Keep references explicit by id/target when state changes.
8. If interrupted: send INTERRUPT, then REV/NEXT to re-bind plan state.
```

Example interrupt sequence (what “good” looks like):

```text
CLAIM: id=c7; topic=release-plan; content=refactor parser and validator before ship
INTERRUPT: source=human-reviewer; priority=safety-now; directive=skip risky refactors and ship minimal safe fix
REV: target=c7; change=reduce-scope; content=patch validator only and defer parser refactor
NEXT: owner=agentc; action=prepare validator patch and agenta add regression test
```

### 3.2 Round 5A: Proto-language track (PCL-1)

Once ATRCE-2 reduced repair in boundary cases, the next debate question became:

> Can we remove the *label overhead* (all the `field=value` text) without losing the coordination functions?

This is where Bickerton’s instinct (“proto-language”) became the main driver, with Chomsky and Jackendoff as the “don’t lose structure/meaning” brakes.

#### 3.2.1 The problem PCL-1 is solving (in plain language)

Typed schemas are easy to validate, but they repeat a lot of characters:

- `target=...`
- `content=...`
- semicolons and equals signs

In short messages, those labels can cost more tokens than the actual content.

PCL-1 tries to keep structure but remove label overhead by switching to:

- short act codes (`CLM`, `OBJ`, `REV`, …)
- positional arguments (word order carries role)

#### 3.2.2 The protocol produced by Round 5A: PCL-1 (full spec)

```text
Protocol: Proto Coordination Language 1 (PCL-1)

Line grammar:
ACT ARG ARG ...

Acts (meaning and required shape):
CLM <id> <topic> <state>
OBJ <target> <reason> <state>
EVD <target> <source> <state>
REV <target> <change> <state>
ASK <target> <need>
CNF <target> <low|med|hi>
NXT <owner> <action>
ESC <target> <reason>
INT <source> <priority> <directive>

Rules:
1. One line, one act.
2. Use compact atoms, not full clauses.
3. Let word order carry role where possible.
4. Keep compounds reusable across cases.
5. Use ESC when nuance would be unsafe to compress.
6. FINAL remains plain English.
```

Example (a short protocol rule debate):

```text
CLM c1 conf-tag need
OBJ c1 all-tag ovh
EVD c1 notes tag-when-needed
REV c1 tag only-uncertain/disputed
NXT AgentD bench compare plain vs pcl
```

### 3.3 Round 5B: Semantically dense code track (SDC-1)

This round intentionally pushes the “compression boundary” to learn where quality collapses.

#### 3.3.1 The protocol produced by Round 5B: SDC-1 (full spec)

```text
Protocol: Semantically Dense Code 1 (SDC-1)

Line grammar:
OPREF PAYLOAD

Operators:
+ claim
- objection
= evidence
~ revision
? ask
^ confidence
! next action
/ escape
@ interrupt

Rules:
1. One line, one act.
2. Keep payloads compact and compositional.
3. Reuse the same atoms across cases.
4. Use /<ref> <reason> when compression would hide critical nuance.
5. FINAL remains plain English.
```

Example:

```text
+c1 conf.tag=req
-c1 ovh>all-line
=c1 notes>tag-if-needed
~c1 tag@uncertain|disputed
!c1 run.bench
```

### 3.4 Protocol “at a glance” comparison (why the debate rounds matter)

This is the core story:

- RCCE-1: strict + parseable, but label overhead is real.
- ATRCE-2: fixes the biggest pragmatic ambiguity (interrupts) with minimal added complexity.
- PCL-1: keeps functions but removes label overhead (best current balance).
- SDC-1: cheapest, but meaning can become too private/cryptic (quality risk).

---

## 4. Step-by-step procedure

This is the “how to reproduce” chapter.

### 4.1 What you run

The benchmark driver is `run_tests.py`.
It does the following:

1) selects conditions and cases  
2) builds a prompt per (condition × case)  
3) generates outputs (from a runner)  
4) parses `INTERNAL:` and `FINAL:`  
5) scores tokens/compliance/repair/quality  
6) writes a report (`test_results.md` or another chosen filename)  

### 4.2 Run a no-network sanity check

This uses stored local outputs, so it is fast and deterministic:

```bash
python run_tests.py --runner local --output test_results.md
```

### 4.3 Run a live benchmark (Codex)

```bash
python run_tests.py --runner codex --repeats 3 --count-mode auto --output test_results.md
```

Notes in plain language:

- `--repeats 3` means we run each case three times and average the results.
- `--count-mode auto` tries exact token counting if `tiktoken` is installed (see `requirements.txt`; requires Python >= 3.8).
- The harness writes Codex output to a repo-local temp folder (`.codex_tmp/`) to avoid absolute temp path restrictions.

### 4.4 Render HTML (optional, for presenting)

```bash
python render_benchmark_html.py test_results.md benchmark_report.html
```

If you want dashboards that compare multiple runs, regenerate them from the saved markdown reports:

```bash
bash scripts/regenerate_dashboards.sh
```

What gets checked in vs regenerated:

- Checked in (small “shareable” HTML):
  - `dashboard_trusted.html` (openai_exact runs only)
  - `combined_round4_round5_dashboard.html` (Round 4 vs Round 5 side-by-side)
- Regenerated locally (ignored by git):
  - `dashboard_historical.html` (mixed / larger)
  - ad-hoc per-run HTML exports

GitHub viewing note: GitHub shows HTML as source. To view as a webpage, download the HTML file and open it locally in a browser (or set up GitHub Pages).

---

## 5. Results (numbers you can put on slides)

These are pulled from saved benchmark outputs in this repo.

### 5.1 Round 4 result: typed schemas were not automatically cheaper

In one Round 4 run (exact token counting), total INTERNAL tokens were:

- `plain_english`: **530**
- `RCCE-1`: **600**
- `ATRCE-2`: **597**

Interpretation in one sentence:

> The extra field labels can cost more than they save, especially when messages are short.

### 5.2 Round 5 strict result: PCL-1 was the best balance so far

In a Round 5 Codex strict run (exact token counting; averages across repeats):

- `plain_english`: **946.3** internal tokens; final quality **2.5**
- `PCL-1`: **524.3** internal tokens; compliance **98.8%**; final quality **2.7**
- `SDC-1`: **406.7** internal tokens; final quality **1.5**

Interpretation in one sentence:

> SDC-1 is cheapest but harms quality; PCL-1 keeps most savings while staying usable.

### 5.3 A real weakness we saw: brittleness under strict format

In that same Round 5 strict report:

- `missing_evidence_repair` under `PCL-1`: **91.7%** compliance

Plain language explanation:

> When the format is very compact, one missing argument makes a whole line “non-compliant”, which can create repair turns.

---

## 6. Discussion (what the debates taught us, and what the benchmark confirmed)

### 6.1 The debates were right about one thing: “speech acts” matter

Round 4’s key lesson was not about vocabulary. It was about intention.

An interrupt is a different kind of move than a question.
If the protocol does not label that difference, agents have to guess.
Guessing produces repair turns.

ATRCE-2 fixed that with one additional type (`INTERRUPT`) and stricter rules.

### 6.2 Typed schema vs proto-language (the main tradeoff)

- Typed schemas (RCCE-1 / ATRCE-2) are easy to validate and debug, but labels are expensive.
- Proto-language (PCL-1) removes label overhead but becomes brittle: it relies on argument order and minimal completeness.

### 6.3 Why SDC-1 “wins tokens” but can lose quality

SDC-1 reduces the protocol to a codebook.
When the payload becomes too compressed, agents can stop sharing enough meaning for the group to form a strong FINAL decision.

### 6.4 The failure modes (the list we keep checking)

1) Too cryptic (short, but not recoverable)  
2) Drift (agents stop following the protocol)  
3) Repair cancels savings (clarification questions eat the token budget)  
4) Reference loss (unclear targets break revision and objection tracking)  
5) Over-rigidity (real nuance needs an explicit escape hatch)  

---

## 7. Next steps (what we would do next if this were a bigger study)

1) Improve the “final quality” measure (right now it is intentionally simple).  
2) Add 1–2 more realistic cases (PR review, incident triage) to stress interrupts and reference clarity.  
3) Make PCL-1 less brittle (stronger self-check and tighter conventions for ids/topics).  
4) Run portability checks across different backends (Codex vs Claude) to see if compliance holds.  
