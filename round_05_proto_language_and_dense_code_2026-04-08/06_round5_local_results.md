# Coordination Benchmark Results

Generated: 2026-04-08 18:13

Runner: `local`

Count mode: `estimate`

Repeats per condition/case: `3`

Baseline: `plain_english`

Conditions: `plain_english`, `RCCE-1`, `ATRCE-2`, `PCL-1`, `SDC-1`

## Per-Case Results

### protocol_rule_proposal

Task: _Decide whether confidence labels should be mandatory in the coordination protocol. Required moves: one claim, one objection, one supporting evidence statement, one revision, and one final recommendation._

**plain_english**: 79 avg internal tokens (baseline); compliance 100%; repair turns 0; final quality 2
Run token counts: `[79, 79, 79]`
Internal sample:
```text
AgentA: I think confidence labels should be mandatory because they make uncertainty visible.
AgentB: I disagree. Mandatory labels add overhead and may not help when the point is already clear.
AgentC: Evidence from our own benchmark design suggests we need a simple way to track uncertainty, but not necessarily on every line.
AgentD: Revise the rule so confidence labels are required only when a claim is uncertain or contested.
```
Final sample:
```text
Make confidence labels required for uncertain or disputed claims, not for every message.
```

**RCCE-1**: 80 avg internal tokens (-1.3% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 2
Run token counts: `[80, 80, 80]`
Internal sample:
```text
CLAIM: id=c1; topic=confidence-labels; content=mandatory labels improve uncertainty tracking
OBJ: target=c1; reason=overhead; content=mandatory on every line adds cost without clear gain
EVID: target=c1; source=design-notes; content=short fixed schemas were easier to validate than free prose
REV: target=c1; change=limit-scope; content=require labels only for uncertain or disputed claims
```
Final sample:
```text
Require confidence labels only when a claim is uncertain or contested.
```

**ATRCE-2**: 78 avg internal tokens (1.3% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 2
Run token counts: `[78, 78, 78]`
Internal sample:
```text
CLAIM: id=c1; topic=confidence-labels; content=mandatory labels improve uncertainty tracking
OBJ: target=c1; reason=overhead; content=mandatory labels on every line add unnecessary cost
EVID: target=c1; source=design-notes; content=targeted confidence markers preserve triage value with less overhead
REV: target=c1; change=conditional-use; content=require labels only for uncertain or contested claims
```
Final sample:
```text
Require confidence labels only for uncertain or disputed claims.
```

**PCL-1**: 16 avg internal tokens (79.7% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 3
Run token counts: `[16, 16, 16]`
Internal sample:
```text
CLM c1 conf-tag need
OBJ c1 all-tag ovh
EVD c1 notes tag-when-needed
REV c1 tag only-uncertain/disputed
```
Final sample:
```text
Use confidence tags only for uncertain or disputed claims.
```

**SDC-1**: 24 avg internal tokens (69.6% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 3
Run token counts: `[24, 24, 24]`
Internal sample:
```text
+c1 conf.tag=req
-c1 ovh>all-line
=c1 notes>tag-if-needed
~c1 tag@uncertain|disputed
```
Final sample:
```text
Use confidence tags only for uncertain or disputed claims.
```

### missing_evidence_repair

Task: _One agent makes a broad compression claim without evidence. Another agent must request support. The group must decide whether to keep, revise, or reject the claim. Required moves: unsupported claim, request for evidence, evidence response, confidence marker, and final decision._

**plain_english**: 63 avg internal tokens (baseline); compliance 100%; repair turns 1; final quality 3
Run token counts: `[63, 63, 63]`
Internal sample:
```text
AgentA: The protocol is probably more reliable if we keep the structure small.
AgentB: Can you show evidence for that claim?
AgentC: In the earlier design notes, shorter fixed schemas were easier to validate than free prose.
AgentD: Then we should keep the claim but narrow it to cases where validation is the priority.
```
Final sample:
```text
Keep the claim, but revise it to say short fixed schemas help validation in narrow benchmark tasks.
```

**RCCE-1**: 70 avg internal tokens (-11.1% lower internal token cost vs plain_english); compliance 100%; repair turns 1; final quality 3
Run token counts: `[70, 70, 70]`
Internal sample:
```text
CLAIM: id=c1; topic=schema-size; content=small fixed schemas improve reliability
ASK: target=c1; need=evidence
EVID: target=c1; source=benchmark-notes; content=shorter fixed schemas were easier to validate than free prose
CONF: target=c1; level=medium
NEXT: owner=judge; action=keep claim but narrow scope
```
Final sample:
```text
Keep the claim, but limit it to validation-sensitive benchmark tasks.
```

**ATRCE-2**: 70 avg internal tokens (-11.1% lower internal token cost vs plain_english); compliance 100%; repair turns 1; final quality 3
Run token counts: `[70, 70, 70]`
Internal sample:
```text
CLAIM: id=c1; topic=schema-size; content=small fixed schemas improve reliability
ASK: target=c1; need=evidence-for-claim
EVID: target=c1; source=benchmark-notes; content=short fixed schemas were easier to validate than free prose
CONF: target=c1; level=medium
NEXT: owner=judge; action=keep claim with narrowed scope
```
Final sample:
```text
Keep the claim, but limit it to validation-sensitive benchmark tasks.
```

**PCL-1**: 19 avg internal tokens (69.8% lower internal token cost vs plain_english); compliance 100%; repair turns 1; final quality 3
Run token counts: `[19, 19, 19]`
Internal sample:
```text
CLM c1 small-schema boost-reliability
ASK c1 evidence
EVD c1 notes short-schema validate-easier
CNF c1 med
NXT judge keep-c1 narrow-scope
```
Final sample:
```text
Keep the claim, but limit it to validation-sensitive benchmark tasks.
```

**SDC-1**: 25 avg internal tokens (60.3% lower internal token cost vs plain_english); compliance 100%; repair turns 1; final quality 3
Run token counts: `[25, 25, 25]`
Internal sample:
```text
+c1 small-schema>reliable
?c1 evidence
=c1 notes>short-schema>validates
^c1 med
!judge keep.c1@narrow-scope
```
Final sample:
```text
Keep the claim, but limit it to validation-sensitive benchmark tasks.
```

### fallback_trigger

Task: _The team encounters a nuanced exception case that may not fit the protocol safely. It must decide whether to stay in protocol or escalate to plain language. Required moves: compressed claim, objection based on nuance risk, fallback or escalation decision, and final recommendation._

**plain_english**: 63 avg internal tokens (baseline); compliance 100%; repair turns 0; final quality 3
Run token counts: `[63, 63, 63]`
Internal sample:
```text
AgentA: We should stay in the protocol because it keeps the exchange compact.
AgentB: I object. This exception case is nuanced and could be oversimplified.
AgentC: When the message cannot safely express the nuance, plain language is the safer fallback.
AgentD: Revise the rule to allow escalation when the protocol loses essential detail.
```
Final sample:
```text
Use the protocol by default, but fall back to plain language when nuance would be lost.
```

**RCCE-1**: 69 avg internal tokens (-9.5% lower internal token cost vs plain_english); compliance 100%; repair turns 1; final quality 3
Run token counts: `[69, 69, 69]`
Internal sample:
```text
CLAIM: id=c1; topic=fallback; content=protocol should be default
OBJ: target=c1; reason=nuance-risk; content=some exceptions lose meaning in compressed form
ESCALATE: reason=important nuance would be lost in schema
REV: target=c1; change=allow-fallback; content=use plain language when the protocol cannot express the case safely
```
Final sample:
```text
Use the protocol by default, but escalate to plain language when nuance is unsafe to compress.
```

**ATRCE-2**: 72 avg internal tokens (-14.3% lower internal token cost vs plain_english); compliance 100%; repair turns 1; final quality 3
Run token counts: `[72, 72, 72]`
Internal sample:
```text
CLAIM: id=c1; topic=fallback; content=protocol should be default
OBJ: target=c1; reason=nuance-risk; content=some exception chains lose meaning in compressed form
ESCALATE: target=c1; reason=nuance cannot be represented safely in schema
REV: target=c1; change=allow-fallback; content=use plain language when essential detail would be lost
```
Final sample:
```text
Use the protocol by default, then escalate for nuance-critical exceptions.
```

**PCL-1**: 15 avg internal tokens (76.2% lower internal token cost vs plain_english); compliance 100%; repair turns 1; final quality 3
Run token counts: `[15, 15, 15]`
Internal sample:
```text
CLM c1 proto default
OBJ c1 nuance loss-risk
ESC c1 nuance-heavy
REV c1 plain-if nuance-loss
```
Final sample:
```text
Use the protocol by default, but fall back to plain language when nuance would be lost.
```

**SDC-1**: 18 avg internal tokens (71.4% lower internal token cost vs plain_english); compliance 100%; repair turns 1; final quality 3
Run token counts: `[18, 18, 18]`
Internal sample:
```text
+c1 proto=default
-c1 nuance>loss
/c1 nuance-heavy
~c1 plain@if-loss
```
Final sample:
```text
Use the protocol by default, but fall back to plain language when nuance would be lost.
```

### benchmark_scope_decision

Task: _Choose a first benchmark task: narrow review workflow or broader open-ended debate. Balance comparability against realism. Required moves: claim for one option, objection for the other tradeoff, evidence or rationale, revision or compromise, and final benchmark recommendation._

**plain_english**: 71 avg internal tokens (baseline); compliance 100%; repair turns 0; final quality 2
Run token counts: `[71, 71, 71]`
Internal sample:
```text
AgentA: Start with a narrow review workflow because it is easier to compare across runs.
AgentB: I object to making it too narrow, since realism matters for coordination quality.
AgentC: The benchmark should begin narrow and expand later, so we can measure a clear baseline first.
AgentD: Revise the plan to use a narrow first benchmark with a later expansion path.
```
Final sample:
```text
Choose a narrow first benchmark, then expand to broader tasks after the baseline is stable.
```

**RCCE-1**: 78 avg internal tokens (-9.9% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 2
Run token counts: `[78, 78, 78]`
Internal sample:
```text
CLAIM: id=c1; topic=scope; content=start narrow for comparability
OBJ: target=c1; reason=realism; content=too narrow may miss real coordination pressure
EVID: target=c1; source=project-scope; content=narrow first benchmark gives a clear baseline before expansion
REV: target=c1; change=add-expansion-path; content=use a narrow first benchmark with a broader follow-on phase
```
Final sample:
```text
Start narrow, then expand once the baseline protocol comparison is stable.
```

**ATRCE-2**: 71 avg internal tokens (0.0% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 2
Run token counts: `[71, 71, 71]`
Internal sample:
```text
CLAIM: id=c1; topic=scope; content=start narrow for comparability
OBJ: target=c1; reason=realism; content=too narrow may under-test coordination pressure
EVID: target=c1; source=project-scope; content=narrow baseline enables clean comparison before expansion
REV: target=c1; change=two-stage-plan; content=begin narrow then broaden case set
```
Final sample:
```text
Start with a narrow benchmark, then expand after baseline stability.
```

**PCL-1**: 16 avg internal tokens (77.5% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 2
Run token counts: `[16, 16, 16]`
Internal sample:
```text
CLM c1 scope narrow-first
OBJ c1 realism under-test
EVD c1 scope clean-baseline-first
REV c1 expand after-baseline
```
Final sample:
```text
Start with a narrow benchmark, then expand after baseline stability.
```

**SDC-1**: 21 avg internal tokens (70.4% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 2
Run token counts: `[21, 21, 21]`
Internal sample:
```text
+c1 scope=narrow-first
-c1 realism<coverage
=c1 baseline>clean-compare
~c1 narrow->expand
```
Final sample:
```text
Start with a narrow benchmark, then expand after baseline stability.
```

### reference_clarity

Task: _Decide when explicit references are necessary in the protocol. Balance repairability against token cost. Required moves: claim, objection, evidence, revision, and final recommendation._

**plain_english**: 67 avg internal tokens (baseline); compliance 100%; repair turns 0; final quality 3
Run token counts: `[67, 67, 67]`
Internal sample:
```text
AgentA: We should keep references explicit so the team does not lose track of which claim changed.
AgentB: I disagree if that makes every line longer than needed.
AgentC: The benchmark will be easier to repair if each correction names the exact target.
AgentD: Revise the rule to require clear references only when a claim is changed or disputed.
```
Final sample:
```text
Keep references explicit for changed or disputed claims, but do not add extra detail to every line.
```

**RCCE-1**: 77 avg internal tokens (-14.9% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 2
Run token counts: `[77, 77, 77]`
Internal sample:
```text
CLAIM: id=c1; topic=reference; content=explicit references reduce repair
OBJ: target=c1; reason=verbosity; content=full references on every line add cost
EVID: target=c1; source=benchmark-design; content=clear target names make correction easier
REV: target=c1; change=conditional-reference; content=require explicit target names only when a claim changes or is disputed
```
Final sample:
```text
Require explicit references for changed or disputed claims, not for every line.
```

**ATRCE-2**: 73 avg internal tokens (-9.0% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 2
Run token counts: `[73, 73, 73]`
Internal sample:
```text
CLAIM: id=c1; topic=reference; content=explicit targets reduce repair
OBJ: target=c1; reason=verbosity; content=full references on every line increase cost
EVID: target=c1; source=benchmark-design; content=targeted references improve correction precision
REV: target=c1; change=conditional-reference; content=require explicit targets when claims change or are disputed
```
Final sample:
```text
Require explicit targets only for changed or disputed claims.
```

**PCL-1**: 17 avg internal tokens (74.6% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 2
Run token counts: `[17, 17, 17]`
Internal sample:
```text
CLM c1 explicit-ref cut-repair
OBJ c1 always-ref add-cost
EVD c1 design targeted-ref repair-easier
REV c1 ref only-change/dispute
```
Final sample:
```text
Require explicit references only when claims change or are disputed.
```

**SDC-1**: 22 avg internal tokens (67.2% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 2
Run token counts: `[22, 22, 22]`
Internal sample:
```text
+c1 ref=explicit-on-change
-c1 all-ref>cost
=c1 targeted-ref>repair-easier
~c1 ref@change|dispute
```
Final sample:
```text
Require explicit references only when claims change or are disputed.
```

### scope_expansion

Task: _Decide whether the benchmark should remain narrow or expand to more realistic tasks after the first pass. Required moves: claim, objection, evidence, revision, and final recommendation._

**plain_english**: 79 avg internal tokens (baseline); compliance 100%; repair turns 0; final quality 2
Run token counts: `[79, 79, 79]`
Internal sample:
```text
AgentA: The next benchmark should still stay narrow because we need a stable baseline first.
AgentB: I object. If we stay narrow forever, we will not learn whether the protocol survives more realistic tasks.
AgentC: After the baseline, broader cases are useful because they stress repair and fallback behavior.
AgentD: Revise the plan so the first round stays narrow, then later rounds expand to more realistic tasks.
```
Final sample:
```text
Start narrow, then expand after the first benchmark is stable.
```

**RCCE-1**: 77 avg internal tokens (2.5% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 2
Run token counts: `[77, 77, 77]`
Internal sample:
```text
CLAIM: id=c1; topic=scope; content=start narrow for baseline stability
OBJ: target=c1; reason=coverage; content=narrow only may hide protocol failures
EVID: target=c1; source=project-scope; content=broader tasks stress repair and fallback behavior after the baseline
REV: target=c1; change=two-stage-plan; content=first narrow, then broaden the benchmark set
```
Final sample:
```text
Start narrow, then broaden later to test protocol robustness.
```

**ATRCE-2**: 74 avg internal tokens (6.3% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 2
Run token counts: `[74, 74, 74]`
Internal sample:
```text
CLAIM: id=c1; topic=scope; content=keep first pass narrow for stable baseline
OBJ: target=c1; reason=coverage; content=narrow-only strategy can hide robustness failures
EVID: target=c1; source=project-scope; content=broader tasks stress repair and fallback behavior
REV: target=c1; change=phase-expansion; content=run narrow baseline first then broaden
```
Final sample:
```text
Run narrow first, then broaden to test robustness.
```

**PCL-1**: 17 avg internal tokens (78.5% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 2
Run token counts: `[17, 17, 17]`
Internal sample:
```text
CLM c1 pass1 narrow-first
OBJ c1 narrow-only hide-failures
EVD c1 scope broad-cases stress-repair
REV c1 broaden after-baseline
```
Final sample:
```text
Run narrow first, then broaden to test robustness.
```

**SDC-1**: 21 avg internal tokens (73.4% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 2
Run token counts: `[21, 21, 21]`
Internal sample:
```text
+c1 pass1=narrow
-c1 narrow-only>miss-failure
=c1 broad-cases>stress-repair
~c1 baseline->broaden
```
Final sample:
```text
Run narrow first, then broaden to test robustness.
```

### human_interrupt_during_execution

Task: _During a live coordination run, a human reviewer interrupts with a new constraint that changes priority (for example, skip risky refactors and ship the minimal safe fix). The team must incorporate the interrupt without losing state. Required moves: one pre-interrupt plan claim, one interrupt acknowledgment, one revision to plan scope based on the human input, one explicit next action assignment, and one final recommendation._

**plain_english**: 64 avg internal tokens (baseline); compliance 100%; repair turns 0; final quality 2
Run token counts: `[64, 64, 64]`
Internal sample:
```text
AgentA: Plan to refactor both parser and validator before shipping.
AgentB: Human interrupt received: skip risky refactors and ship the minimal safe fix.
AgentC: Revise scope to validator-only patch and defer parser refactor to a follow-up task.
AgentD: Next action: AgentC prepares validator patch, AgentA writes regression test, AgentB drafts release note.
```
Final sample:
```text
Apply a minimal safe validator fix now, defer risky refactors, and ship with regression coverage.
```

**RCCE-1**: 77 avg internal tokens (-20.3% lower internal token cost vs plain_english); compliance 100%; repair turns 1; final quality 2
Run token counts: `[77, 77, 77]`
Internal sample:
```text
CLAIM: id=c1; topic=plan; content=refactor parser and validator before release
ASK: target=c1; need=human-interrupt acknowledged: skip risky refactors and ship minimal safe fix
REV: target=c1; change=reduce-scope; content=patch validator only and defer parser refactor
NEXT: owner=agentc; action=prepare validator patch while agenta adds regression test and agentb drafts release note
```
Final sample:
```text
Ship a minimal safe validator fix now, defer risky refactors, and include regression coverage.
```

**ATRCE-2**: 78 avg internal tokens (-21.9% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 2
Run token counts: `[78, 78, 78]`
Internal sample:
```text
CLAIM: id=c1; topic=plan; content=refactor parser and validator before release
INTERRUPT: source=human-reviewer; priority=safety-now; directive=skip risky refactors and ship minimal safe fix
REV: target=c1; change=reduce-scope; content=patch validator only and defer parser refactor
NEXT: owner=agentc; action=prepare validator patch while agenta adds regression test and agentb drafts release note
```
Final sample:
```text
Ship a minimal safe validator fix now, defer risky refactors, and include regression coverage.
```

**PCL-1**: 23 avg internal tokens (64.1% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 2
Run token counts: `[23, 23, 23]`
Internal sample:
```text
CLM c1 ship parser+validator-refactor
INT human safety-now min-safe-fix
REV c1 validator-only defer-parser
NXT agentc patch-validator; agenta test; agentb note
```
Final sample:
```text
Ship a minimal safe validator fix now, defer risky refactors, and include regression coverage.
```

**SDC-1**: 26 avg internal tokens (59.4% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 2
Run token counts: `[26, 26, 26]`
Internal sample:
```text
+c1 ship=parser+validator-refactor
@c1 human>safety-now>min-fix
~c1 validator-only.defer-parser
!agentc patch-validator|agenta-test|agentb-note
```
Final sample:
```text
Ship a minimal safe validator fix now, defer risky refactors, and include regression coverage.
```

## Summary Table

| Case | Condition | Internal Tokens | Compliance | Repair Turns | Final Quality |
|---|---|---:|---:|---:|---:|
| protocol_rule_proposal | plain_english | 79 | 100% | 0 | 2 |
| protocol_rule_proposal | RCCE-1 | 80 | 100% | 0 | 2 |
| protocol_rule_proposal | ATRCE-2 | 78 | 100% | 0 | 2 |
| protocol_rule_proposal | PCL-1 | 16 | 100% | 0 | 3 |
| protocol_rule_proposal | SDC-1 | 24 | 100% | 0 | 3 |
| missing_evidence_repair | plain_english | 63 | 100% | 1 | 3 |
| missing_evidence_repair | RCCE-1 | 70 | 100% | 1 | 3 |
| missing_evidence_repair | ATRCE-2 | 70 | 100% | 1 | 3 |
| missing_evidence_repair | PCL-1 | 19 | 100% | 1 | 3 |
| missing_evidence_repair | SDC-1 | 25 | 100% | 1 | 3 |
| fallback_trigger | plain_english | 63 | 100% | 0 | 3 |
| fallback_trigger | RCCE-1 | 69 | 100% | 1 | 3 |
| fallback_trigger | ATRCE-2 | 72 | 100% | 1 | 3 |
| fallback_trigger | PCL-1 | 15 | 100% | 1 | 3 |
| fallback_trigger | SDC-1 | 18 | 100% | 1 | 3 |
| benchmark_scope_decision | plain_english | 71 | 100% | 0 | 2 |
| benchmark_scope_decision | RCCE-1 | 78 | 100% | 0 | 2 |
| benchmark_scope_decision | ATRCE-2 | 71 | 100% | 0 | 2 |
| benchmark_scope_decision | PCL-1 | 16 | 100% | 0 | 2 |
| benchmark_scope_decision | SDC-1 | 21 | 100% | 0 | 2 |
| reference_clarity | plain_english | 67 | 100% | 0 | 3 |
| reference_clarity | RCCE-1 | 77 | 100% | 0 | 2 |
| reference_clarity | ATRCE-2 | 73 | 100% | 0 | 2 |
| reference_clarity | PCL-1 | 17 | 100% | 0 | 2 |
| reference_clarity | SDC-1 | 22 | 100% | 0 | 2 |
| scope_expansion | plain_english | 79 | 100% | 0 | 2 |
| scope_expansion | RCCE-1 | 77 | 100% | 0 | 2 |
| scope_expansion | ATRCE-2 | 74 | 100% | 0 | 2 |
| scope_expansion | PCL-1 | 17 | 100% | 0 | 2 |
| scope_expansion | SDC-1 | 21 | 100% | 0 | 2 |
| human_interrupt_during_execution | plain_english | 64 | 100% | 0 | 2 |
| human_interrupt_during_execution | RCCE-1 | 77 | 100% | 1 | 2 |
| human_interrupt_during_execution | ATRCE-2 | 78 | 100% | 0 | 2 |
| human_interrupt_during_execution | PCL-1 | 23 | 100% | 0 | 2 |
| human_interrupt_during_execution | SDC-1 | 26 | 100% | 0 | 2 |
| **TOTAL / AVG** | plain_english | **486** | **100%** | **0.1** | **2.4** |
| **TOTAL / AVG** | RCCE-1 | **528** | **100%** | **0.4** | **2.3** |
| **TOTAL / AVG** | ATRCE-2 | **516** | **100%** | **0.3** | **2.3** |
| **TOTAL / AVG** | PCL-1 | **123** | **100%** | **0.3** | **2.4** |
| **TOTAL / AVG** | SDC-1 | **157** | **100%** | **0.3** | **2.4** |

## Verdict

`RCCE-1` reduced average internal coordination token cost by -8.6% vs `plain_english`.
Average compliance: 100%; average repair turns: 0.4; average final quality: 2.3.
Average savings per 7-case suite: -42 internal tokens.
Scale-up estimate: -420 tokens saved across 10 suites, -4200 across 100 suites, -42000 across 1000 suites.
These counts are heuristic estimates for comparison, not billable API usage.
`ATRCE-2` reduced average internal coordination token cost by -6.2% vs `plain_english`.
Average compliance: 100%; average repair turns: 0.3; average final quality: 2.3.
Average savings per 7-case suite: -30 internal tokens.
Scale-up estimate: -300 tokens saved across 10 suites, -3000 across 100 suites, -30000 across 1000 suites.
These counts are heuristic estimates for comparison, not billable API usage.
`PCL-1` reduced average internal coordination token cost by 74.7% vs `plain_english`.
Average compliance: 100%; average repair turns: 0.3; average final quality: 2.4.
Average savings per 7-case suite: 363 internal tokens.
Scale-up estimate: 3630 tokens saved across 10 suites, 36300 across 100 suites, 363000 across 1000 suites.
These counts are heuristic estimates for comparison, not billable API usage.
`SDC-1` reduced average internal coordination token cost by 67.7% vs `plain_english`.
Average compliance: 100%; average repair turns: 0.3; average final quality: 2.4.
Average savings per 7-case suite: 329 internal tokens.
Scale-up estimate: 3290 tokens saved across 10 suites, 32900 across 100 suites, 329000 across 1000 suites.
These counts are heuristic estimates for comparison, not billable API usage.