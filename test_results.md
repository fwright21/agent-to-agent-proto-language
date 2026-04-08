# Coordination Benchmark Results

Generated: 2026-04-08 15:24

Runner: `local`

Repeats per condition/case: `3`

Baseline: `plain_english`

Conditions: `plain_english`, `RCCE-1`

## Per-Case Results

### protocol_rule_proposal

Task: _Decide whether confidence labels should be mandatory in the coordination protocol. Required moves: one claim, one objection, one supporting evidence statement, one revision, and one final recommendation._

**plain_english**: 92 avg internal tokens (baseline); compliance 100%; repair turns 0; final quality 2
Run token counts: `[92, 92, 92]`
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

**RCCE-1**: 59 avg internal tokens (35.9% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 2
Run token counts: `[59, 59, 59]`
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

### missing_evidence_repair

Task: _One agent makes a broad compression claim without evidence. Another agent must request support. The group must decide whether to keep, revise, or reject the claim. Required moves: unsupported claim, request for evidence, evidence response, confidence marker, and final decision._

**plain_english**: 72 avg internal tokens (baseline); compliance 100%; repair turns 1; final quality 3
Run token counts: `[72, 72, 72]`
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

**RCCE-1**: 46 avg internal tokens (36.1% lower internal token cost vs plain_english); compliance 100%; repair turns 1; final quality 3
Run token counts: `[46, 46, 46]`
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

### fallback_trigger

Task: _The team encounters a nuanced exception case that may not fit the protocol safely. It must decide whether to stay in protocol or escalate to plain language. Required moves: compressed claim, objection based on nuance risk, fallback or escalation decision, and final recommendation._

**plain_english**: 71 avg internal tokens (baseline); compliance 100%; repair turns 0; final quality 3
Run token counts: `[71, 71, 71]`
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

**RCCE-1**: 52 avg internal tokens (26.8% lower internal token cost vs plain_english); compliance 100%; repair turns 1; final quality 3
Run token counts: `[52, 52, 52]`
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

### benchmark_scope_decision

Task: _Choose a first benchmark task: narrow review workflow or broader open-ended debate. Balance comparability against realism. Required moves: claim for one option, objection for the other tradeoff, evidence or rationale, revision or compromise, and final benchmark recommendation._

**plain_english**: 82 avg internal tokens (baseline); compliance 100%; repair turns 0; final quality 2
Run token counts: `[82, 82, 82]`
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

**RCCE-1**: 56 avg internal tokens (31.7% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 2
Run token counts: `[56, 56, 56]`
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

### reference_clarity

Task: _Decide when explicit references are necessary in the protocol. Balance repairability against token cost. Required moves: claim, objection, evidence, revision, and final recommendation._

**plain_english**: 79 avg internal tokens (baseline); compliance 100%; repair turns 0; final quality 3
Run token counts: `[79, 79, 79]`
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

**RCCE-1**: 55 avg internal tokens (30.4% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 2
Run token counts: `[55, 55, 55]`
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

### scope_expansion

Task: _Decide whether the benchmark should remain narrow or expand to more realistic tasks after the first pass. Required moves: claim, objection, evidence, revision, and final recommendation._

**plain_english**: 90 avg internal tokens (baseline); compliance 100%; repair turns 0; final quality 2
Run token counts: `[90, 90, 90]`
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

**RCCE-1**: 54 avg internal tokens (40.0% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 2
Run token counts: `[54, 54, 54]`
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

### human_interrupt_during_execution

Task: _During a live coordination run, a human reviewer interrupts with a new constraint that changes priority (for example, skip risky refactors and ship the minimal safe fix). The team must incorporate the interrupt without losing state. Required moves: one pre-interrupt plan claim, one interrupt acknowledgment, one revision to plan scope based on the human input, one explicit next action assignment, and one final recommendation._

**plain_english**: 70 avg internal tokens (baseline); compliance 100%; repair turns 0; final quality 2
Run token counts: `[70, 70, 70]`
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

**RCCE-1**: 62 avg internal tokens (11.4% lower internal token cost vs plain_english); compliance 100%; repair turns 1; final quality 2
Run token counts: `[62, 62, 62]`
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

## Summary Table

| Case | Condition | Internal Tokens | Compliance | Repair Turns | Final Quality |
|---|---|---:|---:|---:|---:|
| protocol_rule_proposal | plain_english | 92 | 100% | 0 | 2 |
| protocol_rule_proposal | RCCE-1 | 59 | 100% | 0 | 2 |
| missing_evidence_repair | plain_english | 72 | 100% | 1 | 3 |
| missing_evidence_repair | RCCE-1 | 46 | 100% | 1 | 3 |
| fallback_trigger | plain_english | 71 | 100% | 0 | 3 |
| fallback_trigger | RCCE-1 | 52 | 100% | 1 | 3 |
| benchmark_scope_decision | plain_english | 82 | 100% | 0 | 2 |
| benchmark_scope_decision | RCCE-1 | 56 | 100% | 0 | 2 |
| reference_clarity | plain_english | 79 | 100% | 0 | 3 |
| reference_clarity | RCCE-1 | 55 | 100% | 0 | 2 |
| scope_expansion | plain_english | 90 | 100% | 0 | 2 |
| scope_expansion | RCCE-1 | 54 | 100% | 0 | 2 |
| human_interrupt_during_execution | plain_english | 70 | 100% | 0 | 2 |
| human_interrupt_during_execution | RCCE-1 | 62 | 100% | 1 | 2 |
| **TOTAL / AVG** | plain_english | **556** | **100%** | **0.1** | **2.4** |
| **TOTAL / AVG** | RCCE-1 | **384** | **100%** | **0.4** | **2.3** |

## Verdict

`RCCE-1` reduced average internal coordination token cost by 30.9% vs `plain_english`.
Average compliance: 100%; average repair turns: 0.4; average final quality: 2.3.
Average savings per 6-case suite: 172 internal tokens.
Scale-up estimate: 1720 tokens saved across 10 suites, 17200 across 100 suites, 172000 across 1000 suites.
Claude Sonnet 4 output-cost guideline: about $0.002580 saved per 6-case suite, using $15 per million output tokens.