# Coordination Benchmark Results

Generated: 2026-04-08 20:59

Runner: `codex`

Count mode: `openai_exact`

Codex model: `gpt-5.2-codex`

Repeats per condition/case: `1`

Baseline: `plain_english`

Conditions: `plain_english`, `RCCE-1`, `ATRCE-2`, `PCL-1`, `SDC-1`

## Per-Case Results

### protocol_rule_proposal

Task: _Decide whether confidence labels should be mandatory in the coordination protocol. Required moves: one claim, one objection, one supporting evidence statement, one revision, and one final recommendation._

**plain_english**: 108 avg internal tokens (baseline); compliance 100%; repair turns 0; final quality 3
Run token counts: `[108]`
Internal sample:
```text
AgentA: I claim confidence labels should be mandatory to make uncertainty explicit and reduce misinterpretation.  
AgentB: Objection: mandatory labels add overhead and may degrade performance in high-speed exchanges.  
AgentC: Supporting evidence: in pilot runs, mandatory uncertainty tags reduced rework because receivers adjusted verification effort appropriately.  
AgentA: Revision: make labels mandatory only for nontrivial claims or when evidence is indirect, and optional for routine updates.  
AgentD: That balances clarity and efficiency; the rule is scoped and practical.
```
Final sample:
```text
Recommend making confidence labels mandatory for nontrivial or indirectly supported claims, while allowing optional labels for routine, low-risk updates.
```

**RCCE-1**: 124 avg internal tokens (-14.8% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 3
Run token counts: `[124]`
Internal sample:
```text
CLAIM: id=C1; topic=confidence-mandate; content=AgentA proposes confidence labels mandatory for each coordination message to reduce ambiguity.
OBJ: target=C1; reason=overhead; content=AgentB objects that mandatory confidence adds friction and slows small exchanges.
EVID: target=C1; source=protocol-analysis; content=AgentC notes ambiguity drops in similar protocols when confidence is required, especially for conflicting claims.
REV: target=C1; change=scope; content=AgentA revises to mandate confidence only for CLAIM, EVID, and REV types, not for ASK or NEXT.
```
Final sample:
```text
CLAIM: id=R1; topic=decision; content=Recommend making confidence labels mandatory for CLAIM, EVID, and REV messages, optional elsewhere.
```

**ATRCE-2**: 122 avg internal tokens (-13.0% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 3
Run token counts: `[122]`
Internal sample:
```text
CLAIM: id=c1; topic=confidence-mandatory; content=Make confidence labels mandatory to improve clarity and decision accountability.
OBJ: target=c1; reason=overhead; content=Mandatory labels may slow coordination and add noise in low-risk exchanges.
EVID: target=c1; source=prior-simulations; content=Benchmarks show reduced rework when confidence is explicit at decision points.
REV: target=c1; change=scope; content=Make confidence labels mandatory only for decisions and recommendations, optional elsewhere.
NEXT: owner=AgentD; action=adopt-revised-policy
```
Final sample:
```text
CLAIM: id=final1; topic=confidence-mandatory; content=Recommendation: require confidence labels for decisions and recommendations; keep them optional for routine updates.
```

**PCL-1**: 58 avg internal tokens (46.3% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 2
Run token counts: `[58]`
Internal sample:
```text
CLM AgentA conf-label mandatory improves audit
OBJ AgentB mandatory adds friction low-signal
EVD AgentC incident postmortems show unlabeled claims misrouted
REV AgentA revise mandate to high-impact scopes only
CNF AgentD rec mandatory for high-impact optional otherwise
```
Final sample:
```text
CNF Group conf-label mandatory high-impact optional low-impact
```

**SDC-1**: 55 avg internal tokens (49.1% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 1
Run token counts: `[55]`
Internal sample:
```text
+c1 A:mandatory?yes->clarity|compare
-c1 B:mandatory?no->burden|friction
=c1 C:pilot->labels↑resolve|↓misalign
~c1 D:default=required|opt_out?->balance
```
Final sample:
```text
!c1 rec:mandatory_default|opt_out_rare|spec=v1
```

### missing_evidence_repair

Task: _One agent makes a broad compression claim without evidence. Another agent must request support. The group must decide whether to keep, revise, or reject the claim. Required moves: unsupported claim, request for evidence, evidence response, confidence marker, and final decision._

**plain_english**: 77 avg internal tokens (baseline); compliance 100%; repair turns 0; final quality 3
Run token counts: `[77]`
Internal sample:
```text
AgentA: I claim our compression scheme will cut all messages by 70% across every workload.
AgentB: Can you provide evidence or measurements to support that claim?
AgentA: I don’t have data yet, it’s based on intuition from similar systems.
AgentC: Confidence: low.
AgentD: Given no evidence, we should revise the claim to a tentative hypothesis.
```
Final sample:
```text
Revise the claim to a hypothesis pending benchmarks; do not keep the original broad assertion.
```

**RCCE-1**: 99 avg internal tokens (-28.6% lower internal token cost vs plain_english); compliance 100%; repair turns 1; final quality 3
Run token counts: `[99]`
Internal sample:
```text
CLAIM: id=c1; topic=compression; content=Protocol X reduces token count by 70% across domains
ASK: target=c1; need=Provide supporting benchmarks or samples
EVID: target=c1; source=bench1; content=10-doc sample shows 68-74% reduction with lossless reconstruction
CONF: target=c1; level=medium
REV: target=c1; change=keep; content=Accept claim with note: based on small sample
```
Final sample:
```text
REV: target=c1; change=keep; content=Keep claim with note: evidence is limited to small benchmark sample
```

**ATRCE-2**: 134 avg internal tokens (-74.0% lower internal token cost vs plain_english); compliance 100%; repair turns 1; final quality 3
Run token counts: `[134]`
Internal sample:
```text
CLAIM: id=c1; topic=global-compression; content=Adaptive chunking with shared dictionaries reduces message size by 60% across all domains.
ASK: target=c1; need=Provide evidence or data supporting the 60% reduction claim.
EVID: target=c1; source=benchmarks-v1; content=Across 12 datasets, median reduction was 58%, with 6 datasets at or above 60%.
CONF: target=c1; level=medium
REV: target=c1; change=revise; content=Revise to “median ~58% with some datasets ≥60%” and limit scope to tested datasets.
```
Final sample:
```text
REV: target=c1; change=revise; content=Adopt revised claim: “Adaptive chunking with shared dictionaries achieved a median ~58% reduction on 12 tested datasets, with some ≥60%.”
```

**PCL-1**: 83 avg internal tokens (-7.8% lower internal token cost vs plain_english); compliance 100%; repair turns 1; final quality 3
Run token counts: `[83]`
Internal sample:
```text
CLM AgentA compress-win all-msgs rate-2x
ASK AgentB need-evidence compress-win all-msgs rate-2x
EVD AgentA sample-20 pairs size-avg 45->22
REV AgentC evidence-thin scope-narrow revise claim-to sample-20 only
CNF AgentD conf-medium revise
NXT AgentD decide revise claim-to sample-20 only
```
Final sample:
```text
NXT group decide revise claim-to sample-20 only
```

**SDC-1**: 49 avg internal tokens (36.4% lower internal token cost vs plain_english); compliance 100%; repair turns 1; final quality 2
Run token counts: `[49]`
Internal sample:
```text
+c1 A:claim=x
?c1 B:req=ev(x)
=c1 C:ev=x->e1
^c1 D:conf=mid
!c1 A:dec=revise(x|e1)
```
Final sample:
```text
!c1 group:revise(x->x')
```

### fallback_trigger

Task: _The team encounters a nuanced exception case that may not fit the protocol safely. It must decide whether to stay in protocol or escalate to plain language. Required moves: compressed claim, objection based on nuance risk, fallback or escalation decision, and final recommendation._

**plain_english**: 104 avg internal tokens (baseline); compliance 100%; repair turns 0; final quality 3
Run token counts: `[104]`
Internal sample:
```text
AgentA: Compressed claim: The edge case seems safe to encode in protocol with a minor extension, so we can proceed in protocol.
AgentB: Objection: The nuance risk is that the exception changes intent mid-utterance, and the protocol could silently misclassify it, which is unsafe.
AgentC: Given that risk, I favor escalation to plain language for this case rather than forcing a brittle encoding.
AgentD: Decision: escalate to plain language for this exception; keep protocol for standard cases.
```
Final sample:
```text
Recommend escalating this nuanced exception to plain language for safety, while keeping protocol for routine cases.
```

**RCCE-1**: 141 avg internal tokens (-35.6% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 0
Run token counts: `[141]`
Internal sample:
```text
CLAIM: id=c1; topic=exception-case; content=Compressed: case has ambiguous edge condition that could breach protocol safety if interpreted narrowly.
OBJ: target=c1; reason=nuance-risk; content=Nuance implies hidden constraints; staying in protocol may omit critical qualifiers and increase misuse risk.
NEXT: owner=coordination; action=escalate-to-plain-language-for-safe-clarification.
REV: target=c1; change=update; content=Recommendation adjusted to allow escalation when ambiguity threatens safety or correctness.
CLAIM: id=final1; topic=recommendation; content=Escalate to plain language to clarify constraints, then re-enter protocol after resolving ambiguity.
```
Final sample:
```text

```

**ATRCE-2**: 98 avg internal tokens (5.8% lower internal token cost vs plain_english); compliance 100%; repair turns 1; final quality 3
Run token counts: `[98]`
Internal sample:
```text
CLAIM: id=c1; topic=exception-case; content=Edge case introduces ambiguity in ATRCE-2 constraints and may be unsafe to express fully in schema.
OBJ: target=c1; reason=nuance-risk; content=Schema may omit critical qualifiers, risking misinterpretation and unsafe guidance.
ESCALATE: reason=Protocol cannot safely capture nuanced exception; target=plain-language
NEXT: owner=AgentD; action=Issue escalation and provide minimal safe summary constraints.
```
Final sample:
```text
CLAIM: id=rec1; topic=recommendation; content=Escalate to plain language with explicit safety qualifiers; avoid forcing ATRCE-2 for this exception.
```

**PCL-1**: 35 avg internal tokens (66.3% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 2
Run token counts: `[35]`
Internal sample:
```text
CLM AgentA stay-proto ok-case
OBJ AgentB nuance-risk exception-unsafe
CNF AgentC ESC plain-language safety-first
NXT AgentD recommend ESC
```
Final sample:
```text
NXT Group ESC plain-language recommendation
```

**SDC-1**: 58 avg internal tokens (44.2% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 2
Run token counts: `[58]`
Internal sample:
```text
+c1 AgentA:excp? risk=nuance|safety
-c1 AgentB:nuance>protocol risk=high
~c1 AgentC:decision=escalate->plain
!c1 AgentD:rec=plain|note=protocol-unsafe
```
Final sample:
```text
~c1 group:escalate->plain;recommend=exit-protocol|explain-exception
```

### benchmark_scope_decision

Task: _Choose a first benchmark task: narrow review workflow or broader open-ended debate. Balance comparability against realism. Required moves: claim for one option, objection for the other tradeoff, evidence or rationale, revision or compromise, and final benchmark recommendation._

**plain_english**: 181 avg internal tokens (baseline); compliance 100%; repair turns 0; final quality 3
Run token counts: `[181]`
Internal sample:
```text
AgentA: I claim we should choose the narrow review workflow for the first benchmark; it offers comparability and clearer scoring. The tradeoff is reduced realism versus a broader debate.
AgentB: I object that the narrow workflow may be too artificial; a broader open-ended debate better reflects real collaboration. Evidence: benchmarks that feel real expose edge cases and coordination failures.
AgentC: Rationale for narrow: reproducibility matters early; fewer variables make it easier to detect regressions. But I concede realism is weaker.
AgentD: Revision: we can pick narrow now but frame it with a small debate element in the prompt to preserve some realism. That’s a compromise on comparability vs realism.
AgentA: I can accept that compromise, but still recommend labeling it as a narrow review workflow benchmark to keep scoring tight.
AgentB: Agreed if the debate element is constrained and doesn’t explode scope.
```
Final sample:
```text
Recommend a narrow review workflow as the first benchmark, with a constrained debate element to retain some realism while preserving comparability and scoring clarity.
```

**RCCE-1**: 103 avg internal tokens (43.1% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 2
Run token counts: `[103]`
Internal sample:
```text
CLAIM: id=1; topic=benchmark-task; content=narrow-review-workflow
OBJ: target=broader-open-ended-debate; reason=lower-comparability; content=greater-realism-but-harder-to-compare
EVID: target=narrow-review-workflow; source=benchmarking-practice; content=controlled-scope-increases-repeatability-and-score-stability
REV: target=benchmark-task; change=compromise; content=narrow-review-with-small-open-ended-appendix
```
Final sample:
```text
CLAIM: id=final; topic=benchmark-recommendation; content=narrow-review-workflow-with-minimal-open-ended-appendix
```

**ATRCE-2**: 150 avg internal tokens (17.1% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 3
Run token counts: `[150]`
Internal sample:
```text
CLAIM: id=1; topic=benchmark-task; content=Choose narrow review workflow to maximize comparability and controlled variables
OBJ: target=benchmark-task; reason=realism-gap; content=Broader open-ended debate better reflects real-world coordination but reduces comparability
EVID: target=benchmark-task; source=method-rationale; content=Narrow workflows yield consistent artifacts and measurable outcomes; open debates add uncontrolled variance
REV: target=benchmark-task; change=hybrid-scope; content=Adopt narrow review workflow with a short open-ended segment for realism while preserving comparability
CONF: target=benchmark-task; level=high
NEXT: owner=benchmark-task; action=Recommend the hybrid narrow-first benchmark as final choice
```
Final sample:
```text
CLAIM: id=final; topic=recommendation; content=Use a narrow review workflow as the primary benchmark, augmented by a brief open-ended debate segment to balance comparability with realism
```

**PCL-1**: 60 avg internal tokens (66.9% lower internal token cost vs plain_english); compliance 0%; repair turns 0; final quality 3
Run token counts: `[60]`
Internal sample:
```text
AgentA CLM narrow_review comparability_high realism_ok
AgentB OBJ narrow_review realism_low open_debate_realism_high
AgentC EVD benchmark_goal repeatability_need variance_control
AgentD REV hybrid narrow_core plus debate_extension
AgentA CNF hybrid accept; NXT recommend_hybrid
```
Final sample:
```text
CLM recommend_hybrid narrow_core then open_debate_extension balance comparability realism
```

**SDC-1**: 55 avg internal tokens (69.6% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 1
Run token counts: `[55]`
Internal sample:
```text
+c1 AgentA|nrw>cmp
-c1 AgentB|oed>rlm
=c1 AgentC|nrw:hi-cmp|lo-var
~c1 AgentD|cmp:hyb|nrw-core+oed-scope
```
Final sample:
```text
!c1 rec=cmp-hyb(nrw-core|oed-scope)
```

### reference_clarity

Task: _Decide when explicit references are necessary in the protocol. Balance repairability against token cost. Required moves: claim, objection, evidence, revision, and final recommendation._

**plain_english**: 126 avg internal tokens (baseline); compliance 100%; repair turns 1; final quality 3
Run token counts: `[126]`
Internal sample:
```text
AgentA: Claim: Explicit references are necessary when ambiguity would block repair, such as resolving pronouns or linking steps to concrete prior data.  
AgentB: Objection: If we add references too often, token cost spikes and the protocol loses its compression advantage.  
AgentC: Evidence: In past repairs, failures mostly came from unclear entity binding and missing source anchors, not from lack of stylistic detail; short references fixed the issue with small overhead.  
AgentD: Revision: Use a threshold rule—require explicit references only for cross-turn dependencies, reused entities, or when multiple candidates exist; otherwise allow implicit context.
```
Final sample:
```text
Use explicit references only when they materially improve repairability: cross-turn dependencies, reused entities, or any case with multiple plausible antecedents. Skip references for local, single-entity steps to save tokens.
```

**RCCE-1**: 144 avg internal tokens (-14.3% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 3
Run token counts: `[144]`
Internal sample:
```text
CLAIM: id=1; topic=explicit-references; content=Use explicit references only when ambiguity or external binding would block repair.
OBJ: target=1; reason=token-cost; content=Defaulting to explicit references inflates tokens; prefer implicit links when local context is clear.
EVID: target=1; source=repair-history; content=Missing explicit references caused mis-repair in 3 of 5 ambiguous edits; explicit IDs enabled fast recovery.
REV: target=1; change=rule-narrowed; content=Require explicit references only for cross-turn dependencies, multi-entity ambiguity, or external artifacts; otherwise implicit.
NEXT: owner=4; action=confirm-group-recommendation
```
Final sample:
```text
CLAIM: id=final; topic=explicit-references; content=Require explicit references only for cross-turn dependencies, multi-entity ambiguity, or external artifacts; otherwise keep implicit to save tokens while preserving repairability.
```

**ATRCE-2**: 156 avg internal tokens (-23.8% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 3
Run token counts: `[156]`
Internal sample:
```text
CLAIM: id=c1; topic=explicit-references; content=Use explicit references when ambiguity would break repairability or when anchoring cross-turn dependencies.
OBJ: target=c1; reason=token-cost; content=Defaulting to explicit references inflates tokens and may be unnecessary for short, local context.
EVID: target=c1; source=pattern; content=Without explicit anchors, multi-claim chains often misattach during repair, causing rework.
REV: target=c1; change=scope; content=Limit explicit references to cross-turn dependencies, multi-entity disambiguation, and contested claims; keep implicit elsewhere.
CONF: target=c1; level=high
NEXT: owner=AgentD; action=Summarize rule for final recommendation.
```
Final sample:
```text
CLAIM: id=rec1; topic=explicit-references; content=Use explicit references only for cross-turn dependencies, multi-entity disambiguation, and contested claims; keep implicit references elsewhere to reduce token cost while preserving repairability.
```

**PCL-1**: 138 avg internal tokens (-9.5% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 3
Run token counts: `[138]`
Internal sample:
```text
CLM AgentA refs-explicit-when-ambig high-repair low-cost
OBJ AgentB refs-explicit-cost token-heavy if-context-stable skip
EVD AgentC failures-likely without refs: misbind, drift, merge
REV AgentA rule-refine explicit refs for unstable, low for stable-local
CLM AgentD balance: explicit refs for cross-agent, optional intra-turn
EVD AgentB data: long refs increase cost, short handles ok
REV AgentD propose: ref-needed if ambiguity>1 or edits>1 hop
CNF AgentC agree rule-threshold ambiguity>1, unstable>10%
NXT AgentA draft-reco
```
Final sample:
```text
CLM Group reco: use explicit refs when ambiguity>1, cross-agent hops, or unstable info; omit for stable-local to save tokens
```

**SDC-1**: 87 avg internal tokens (31.0% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 1
Run token counts: `[87]`
Internal sample:
```text
+c1 A:ref?=>need@repair>cost;rule:explicit@boundary
-c1 B:obj=ref?too-costly;if ctx-stable->implicit ok
=c1 C:evd=failures:ambig->repair↑;explicit@handshake|state-change reduces retries
~c1 D:rev=policy:explicit when new-entity|state-shift|conflict else implicit
```
Final sample:
```text
!c1 REC=explicit@boundary|state-shift|conflict;implicit@stable_ctx;aim repair>token
```

### scope_expansion

Task: _Decide whether the benchmark should remain narrow or expand to more realistic tasks after the first pass. Required moves: claim, objection, evidence, revision, and final recommendation._

**plain_english**: 128 avg internal tokens (baseline); compliance 100%; repair turns 0; final quality 3
Run token counts: `[128]`
Internal sample:
```text
AgentA: Claim — We should expand to more realistic tasks after the first pass to validate external validity.
AgentB: Objection — Expanding too early risks confounding baseline measurements; narrow scope protects comparability.
AgentC: Evidence — Past benchmarks show early expansion uncovers integration failures that narrow tasks miss, while a staged approach preserves baseline clarity.
AgentA: Revision — Keep the first pass narrow for clean baselines, then expand in a controlled second pass with defined realism tiers.
AgentD: Final recommendation — Proceed with a narrow first pass, then expand to realistic tasks in the second pass using tiered complexity and fixed success metrics.
```
Final sample:
```text
Keep the first pass narrow to establish clean baselines, then expand to realistic tasks in a staged second pass with defined tiers and metrics.
```

**RCCE-1**: 133 avg internal tokens (-3.9% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 3
Run token counts: `[133]`
Internal sample:
```text
CLAIM: id=c1; topic=scope; content=Keep benchmark narrow for pass1, expand after pass1 if stability holds
OBJ: target=c1; reason=validity; content=Narrow pass1 may miss realistic failure modes
EVID: target=c1; source=s1; content=Pilot data shows stable signal on core tasks, realism gaps appear only in long-horizon tests
REV: target=c1; change=add-guard; content=Expand after pass1 with staged realism and rollback triggers
CONF: target=c1; level=high
NEXT: owner=group; action=Adopt staged expansion policy after first pass
```
Final sample:
```text
CLAIM: id=f1; topic=recommendation; content=Proceed with a narrow first pass, then expand to more realistic tasks in a staged manner with rollback triggers once pass1 stability criteria are met
```

**ATRCE-2**: 142 avg internal tokens (-10.9% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 3
Run token counts: `[142]`
Internal sample:
```text
CLAIM: id=c1; topic=scope; content=Keep the benchmark narrow for the first pass to stabilize metrics and reduce confounds.
OBJ: target=c1; reason=coverage; content=A narrow pass risks missing failure modes that only appear in realistic tasks.
EVID: target=c1; source=pilot-results; content=Early runs show high variance when task types expand, reducing comparability across models.
REV: target=c1; change=refine; content=Maintain a narrow first pass, but predefine a small expansion set for pass two.
CONF: target=c1; level=high
NEXT: owner=a2; action=Draft pass-two expansion set criteria and success thresholds.
```
Final sample:
```text
CLAIM: id=rec1; topic=recommendation; content=Remain narrow for the first pass, then expand with a predefined realistic task set in pass two.
```

**PCL-1**: 50 avg internal tokens (60.9% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 3
Run token counts: `[50]`
Internal sample:
```text
CLM AgentA narrow-first risk-low
OBJ AgentB narrow-first realism-low
EVD AgentC pass1 scope-tight time-save signal-fast
REV AgentA update expand-after-pass1 guardrails
NXT AgentD recommend expand-after-pass1
```
Final sample:
```text
Expand after pass1 with guardrails; keep pass1 narrow for signal.
```

**SDC-1**: 40 avg internal tokens (68.8% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 2
Run token counts: `[40]`
Internal sample:
```text
+c1 A:narrow->firstpass
-c1 B:realism>coverage
=c1 C:pass1fit|risk>low
~c1 D:condexpand@pass2
```
Final sample:
```text
!c1 group:keep_narrow_pass1;expand_pass2_if_OK
```

### human_interrupt_during_execution

Task: _During a live coordination run, a human reviewer interrupts with a new constraint that changes priority (for example, skip risky refactors and ship the minimal safe fix). The team must incorporate the interrupt without losing state. Required moves: one pre-interrupt plan claim, one interrupt acknowledgment, one revision to plan scope based on the human input, one explicit next action assignment, and one final recommendation._

**plain_english**: 134 avg internal tokens (baseline); compliance 100%; repair turns 0; final quality 2
Run token counts: `[134]`
Internal sample:
```text
AgentA: Plan claim pre-interrupt: we will refactor the parser and storage layers in one pass to remove duplication, then add tests and ship.
AgentB: Human interrupt acknowledged: reviewer says skip risky refactors and ship the minimal safe fix.
AgentC: Revising scope: drop parser/storage refactor; limit to a targeted null-check fix and a small regression test.
AgentD: Next action assignment: AgentB, implement the null-check fix in the existing flow and add a single test; AgentA will draft the release note.
AgentA: Final recommendation: proceed with the minimal fix plus one test now, schedule refactor for later after release.
```
Final sample:
```text
Ship the minimal safe fix with a single regression test today, defer the refactor to a later cycle.
```

**RCCE-1**: 119 avg internal tokens (11.2% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 3
Run token counts: `[119]`
Internal sample:
```text
CLAIM: id=plan-1; topic=release; content=Proceed with refactor + fix, then run full tests before ship
EVID: target=plan-1; source=interrupt; content=Human reviewer: skip risky refactor and ship minimal safe fix now
REV: target=plan-1; change=scope; content=Drop refactor; implement minimal safe fix only; defer full test sweep to smoke tests
NEXT: owner=AgentB; action=Implement minimal safe fix and run smoke tests
CONF: target=plan-1; level=high
```
Final sample:
```text
CLAIM: id=recommend-1; topic=release; content=Ship minimal safe fix now; defer refactor and broader tests to a follow-up ticket
```

**ATRCE-2**: 112 avg internal tokens (16.4% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 3
Run token counts: `[112]`
Internal sample:
```text
CLAIM: id=plan1; topic=release; content=AgentA proposes plan to refactor module and add full tests before shipping fix.
INTERRUPT: source=human; priority=high; directive=skip risky refactors and ship minimal safe fix.
CONF: target=interrupt; level=high
REV: target=plan1; change=scope; content=AgentB updates plan to minimal safe fix only, defers refactor and extra tests.
NEXT: owner=AgentC; action=prepare minimal patch and targeted regression test.
```
Final sample:
```text
CLAIM: id=final1; topic=recommendation; content=AgentD recommends shipping the minimal safe fix now and scheduling refactor later.
```

**PCL-1**: 58 avg internal tokens (56.7% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 2
Run token counts: `[58]`
Internal sample:
```text
CLM AgentA plan v1 safe-fix + refactor
INT AgentD human-irq skip-refactor ship-min
REV AgentA plan v2 scope=min-fix defer-refactor
NXT AgentB patch minimal-fix now
CNF AgentC rec ship-min monitor
```
Final sample:
```text
CNF group rec ship-min now defer-refactor
```

**SDC-1**: 77 avg internal tokens (42.5% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 1
Run token counts: `[77]`
Internal sample:
```text
+c1 AgentA|plan:minfix>refactor_later
@c1 AgentB|ack:human_interrupt
~c1 AgentC|rev:scope=minsafe_fix|skip_risky
!c1 AgentD|next:AgentA->patch_min|AgentB->tests
^c1 AgentA|rec:ship_min_fix|defer_refactor
```
Final sample:
```text
^c1 group|rec:ship_min_fix|risk=low
```

## Summary Table

| Case | Condition | Internal Tokens | Compliance | Repair Turns | Final Quality |
|---|---|---:|---:|---:|---:|
| protocol_rule_proposal | plain_english | 108 | 100% | 0 | 3 |
| protocol_rule_proposal | RCCE-1 | 124 | 100% | 0 | 3 |
| protocol_rule_proposal | ATRCE-2 | 122 | 100% | 0 | 3 |
| protocol_rule_proposal | PCL-1 | 58 | 100% | 0 | 2 |
| protocol_rule_proposal | SDC-1 | 55 | 100% | 0 | 1 |
| missing_evidence_repair | plain_english | 77 | 100% | 0 | 3 |
| missing_evidence_repair | RCCE-1 | 99 | 100% | 1 | 3 |
| missing_evidence_repair | ATRCE-2 | 134 | 100% | 1 | 3 |
| missing_evidence_repair | PCL-1 | 83 | 100% | 1 | 3 |
| missing_evidence_repair | SDC-1 | 49 | 100% | 1 | 2 |
| fallback_trigger | plain_english | 104 | 100% | 0 | 3 |
| fallback_trigger | RCCE-1 | 141 | 100% | 0 | 0 |
| fallback_trigger | ATRCE-2 | 98 | 100% | 1 | 3 |
| fallback_trigger | PCL-1 | 35 | 100% | 0 | 2 |
| fallback_trigger | SDC-1 | 58 | 100% | 0 | 2 |
| benchmark_scope_decision | plain_english | 181 | 100% | 0 | 3 |
| benchmark_scope_decision | RCCE-1 | 103 | 100% | 0 | 2 |
| benchmark_scope_decision | ATRCE-2 | 150 | 100% | 0 | 3 |
| benchmark_scope_decision | PCL-1 | 60 | 0% | 0 | 3 |
| benchmark_scope_decision | SDC-1 | 55 | 100% | 0 | 1 |
| reference_clarity | plain_english | 126 | 100% | 1 | 3 |
| reference_clarity | RCCE-1 | 144 | 100% | 0 | 3 |
| reference_clarity | ATRCE-2 | 156 | 100% | 0 | 3 |
| reference_clarity | PCL-1 | 138 | 100% | 0 | 3 |
| reference_clarity | SDC-1 | 87 | 100% | 0 | 1 |
| scope_expansion | plain_english | 128 | 100% | 0 | 3 |
| scope_expansion | RCCE-1 | 133 | 100% | 0 | 3 |
| scope_expansion | ATRCE-2 | 142 | 100% | 0 | 3 |
| scope_expansion | PCL-1 | 50 | 100% | 0 | 3 |
| scope_expansion | SDC-1 | 40 | 100% | 0 | 2 |
| human_interrupt_during_execution | plain_english | 134 | 100% | 0 | 2 |
| human_interrupt_during_execution | RCCE-1 | 119 | 100% | 0 | 3 |
| human_interrupt_during_execution | ATRCE-2 | 112 | 100% | 0 | 3 |
| human_interrupt_during_execution | PCL-1 | 58 | 100% | 0 | 2 |
| human_interrupt_during_execution | SDC-1 | 77 | 100% | 0 | 1 |
| **TOTAL / AVG** | plain_english | **858** | **100%** | **0.1** | **2.9** |
| **TOTAL / AVG** | RCCE-1 | **863** | **100%** | **0.1** | **2.4** |
| **TOTAL / AVG** | ATRCE-2 | **914** | **100%** | **0.3** | **3** |
| **TOTAL / AVG** | PCL-1 | **482** | **85.7%** | **0.1** | **2.6** |
| **TOTAL / AVG** | SDC-1 | **421** | **100%** | **0.1** | **1.4** |

## Verdict

`RCCE-1` reduced average internal coordination token cost by -0.6% vs `plain_english`.
Average compliance: 100%; average repair turns: 0.1; average final quality: 2.4.
Average savings per 7-case suite: -5 internal tokens.
Scale-up estimate: -50 tokens saved across 10 suites, -500 across 100 suites, -5000 across 1000 suites.
These counts use the configured OpenAI tokenizer directly; apply model-specific pricing separately if needed.
`ATRCE-2` reduced average internal coordination token cost by -6.5% vs `plain_english`.
Average compliance: 100%; average repair turns: 0.3; average final quality: 3.
Average savings per 7-case suite: -56 internal tokens.
Scale-up estimate: -560 tokens saved across 10 suites, -5600 across 100 suites, -56000 across 1000 suites.
These counts use the configured OpenAI tokenizer directly; apply model-specific pricing separately if needed.
`PCL-1` reduced average internal coordination token cost by 43.8% vs `plain_english`.
Average compliance: 85.7%; average repair turns: 0.1; average final quality: 2.6.
Average savings per 7-case suite: 376 internal tokens.
Scale-up estimate: 3760 tokens saved across 10 suites, 37600 across 100 suites, 376000 across 1000 suites.
These counts use the configured OpenAI tokenizer directly; apply model-specific pricing separately if needed.
`SDC-1` reduced average internal coordination token cost by 50.9% vs `plain_english`.
Average compliance: 100%; average repair turns: 0.1; average final quality: 1.4.
Average savings per 7-case suite: 437 internal tokens.
Scale-up estimate: 4370 tokens saved across 10 suites, 43700 across 100 suites, 437000 across 1000 suites.
These counts use the configured OpenAI tokenizer directly; apply model-specific pricing separately if needed.