# Session Handoff — 2026-04-12

## 0) What this project is (one paragraph)

This repo is a small research/engineering project about **making multi-agent coordination cheaper**. The target is not “shorter answers to humans”. The target is **shorter INTERNAL agent-to-agent conversation** while keeping coordination reliable (claims, objections, evidence, revisions, next actions) and keeping the human-facing output readable.

Every benchmark run forces this shape:

```text
INTERNAL:
(agent coordination transcript — measured + compressed)
FINAL:
(human-facing recommendation — kept readable)
```

---

## 1) Who could be interested (and why, given the results)

### 1.1 Product / platform teams (cost + latency owners)

If you run multi-agent workflows in production, INTERNAL coordination can become a large share of your token bill. The results here show that **you can reduce INTERNAL tokens substantially** with a protocol (PCL-1) while keeping high format compliance, which suggests a real cost/latency lever.

### 1.2 Agent framework engineers (protocol + orchestration)

This repo provides:

- concrete protocol specs (RCCE-1, ATRCE-2, PCL-1, SDC-1)
- a repeatable benchmark harness
- a clear story of *why* each protocol change happened (debates + failure modes)

The results show that “structured English” with field labels is not always cheaper, and that act-typing for interrupts is a real coordination stability improvement.

### 1.3 Evaluation / reliability people

The benchmark focuses on measurable failure modes:

- compliance drift
- repair turns (asking/escaping)
- missing references and unclear targets
- quality drops when compression becomes too cryptic

This gives a practical evaluation surface for coordination protocols.

### 1.4 Researchers (protocol design for LLMs)

This repo treats protocol design as: **debate → formal spec → benchmark evidence**. It also explores a compression frontier:

- typed schemas (readable + parseable, but label overhead)
- proto-language (positional arguments)
- dense code (even cheaper, higher quality risk)

---

## 2) What happened in the debates (high level, plain language)

We use a “linguist panel” debate method to generate protocol candidates. The linguists are used as *personas* that protect different coordination properties.

Key debate conclusions that shaped the protocols:

- **Speech acts matter**: an “interrupt” is not a question; if the protocol doesn’t label it explicitly, other agents guess, and guessing causes repair.
- **Label overhead is real**: `field=value` schemas can cost more tokens than they save when messages are short.
- **Proto-language can be stable**: using short act codes + positional arguments can keep structure while cutting repeated label text.
- **There is a compression cliff**: dense symbolic code can reduce tokens further, but quality can drop because meaning becomes too private/cryptic.

---

## 3) Current protocol candidates (embedded specs)

### 3.1 RCCE-1 (typed coordination English)

Line grammar:

```text
TYPE: field=value; field=value; ...
```

Types + required fields:

```text
CLAIM: id, topic, content
EVID: target, source, content
OBJ: target, reason, content
REV: target, change, content
ASK: target, need
CONF: target, level
NEXT: owner, action
ESCALATE: reason   (early versions sometimes allowed target to be optional)
```

### 3.2 ATRCE-2 (RCCE-1 + explicit interrupt + stricter rules)

Adds:

```text
INTERRUPT: source, priority, directive
```

Also tightens:

- `ASK` is only for missing information (not directives)
- `ESCALATE` must anchor to a `target`
- action-first content (ban framing/politeness inside content/action)

### 3.3 PCL-1 (proto-language: act codes + positional arguments)

Line grammar:

```text
ACT ARG ARG ...
```

Acts:

```text
CLM <id> <topic> <state>
OBJ <target> <reason> <state>
EVD <target> <source> <state>
REV <target> <change> <state>
ASK <target> <need>
CNF <target> <low|med|hi>
NXT <owner> <action>
ESC <target> <reason>
INT <source> <priority> <directive>
```

Core idea: remove label overhead (`target=`, `content=`) but keep coordination functions.

### 3.4 SDC-1 (semantically dense code)

Line grammar:

```text
OPREF PAYLOAD
```

Operators:

```text
+ claim
- objection
= evidence
~ revision
? ask
^ confidence
! next action
/ escape
@ interrupt
```

Core idea: explore the maximum compression boundary; risk is readability/quality collapse.

---

## 4) Benchmark suite (what we test)

The benchmark uses narrow structured tasks so scoring is stable:

1) protocol rule proposal  
2) missing-evidence repair  
3) fallback trigger (escape hatch decision)  
4) benchmark-scope decision (comparability vs realism tradeoff)  
5) human interrupt during execution (priority shift mid-run)  

Metrics tracked:

- INTERNAL token count (main cost)
- format compliance
- repair turns (ASK/ESC/ESCALATE patterns)
- final quality (simple proxy)

---

## 5) Key results worth remembering (numbers you can quote)

### 5.1 Typed schemas can lose to plain English on tokens

One Round 4 exact-count run reported total INTERNAL tokens:

- plain English: **530**
- RCCE-1: **600**
- ATRCE-2: **597**

Interpretation: field labels can cost more than they save when messages are short.

### 5.2 Proto-language (PCL-1) is the best current “savings + still works” candidate

One Round 5 Codex strict exact-count run (averages across repeats):

- plain English: **946.3** INTERNAL; quality **2.5**
- PCL-1: **524.3** INTERNAL; compliance **98.8%**; quality **2.7**
- SDC-1: **406.7** INTERNAL; quality **1.5**

Interpretation: SDC-1 is cheapest but quality drops; PCL-1 keeps most savings while staying usable.

### 5.3 Known weakness: brittleness under strict formatting

In that same Round 5 strict report:

- `missing_evidence_repair` under PCL-1: **91.7%** compliance

Interpretation: compact formats amplify small mistakes (missing an argument) into non-compliance and repair.

---

## 6) How to reproduce (copy/paste)

Sanity check (no model calls; uses local stored outputs):

```bash
python run_tests.py --runner local --output test_results.md
```

Live run with Codex:

```bash
python run_tests.py --runner codex --repeats 3 --count-mode auto --output test_results.md
```

Optional: render the Markdown report into HTML:

```bash
python render_benchmark_html.py test_results.md benchmark_report.html
```

---

## 7) What changed in this session (so the next person doesn’t miss it)

### 7.1 The main dissertation/workflow report was rewritten to include the debates + linguists

The “workflow” is now written as a self-contained dissertation-style report with:

- a plain-language explanation of the linguist panel and what each one contributes
- a round-by-round narrative of what changed and why
- embedded protocol specs (no “go read another file” dependency)
- the step-by-step reproduction procedure
- the results + discussion + next steps

### 7.2 A stability fix was made to avoid a `/tmp` absolute-path crash

Some environments reject absolute `/tmp/...` paths for certain tool calls. The harness now writes Codex “last message” outputs to a repo-local temp directory (`.codex_tmp/`) to avoid that failure mode.

---

## 8) Open questions / next steps (practical priorities)

1) Strengthen “final quality” evaluation (current metric is intentionally simple).  
2) Add realistic coordination cases (PR review, incident triage) to stress interrupts and reference clarity.  
3) Make PCL-1 less brittle (stronger self-check + tighter id/topic conventions).  
4) Run portability checks across different model backends to confirm compliance and repair patterns hold.  

