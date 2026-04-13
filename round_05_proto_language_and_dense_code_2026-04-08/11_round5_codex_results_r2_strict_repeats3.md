# Coordination Benchmark Results

Generated: 2026-04-12 21:11

Runner: `codex`

Count mode: `openai_exact`

Codex model: `gpt-5.2-codex`

Repeats per condition/case: `3`

Baseline: `plain_english`

Conditions: `plain_english`, `RCCE-1`, `ATRCE-2`, `PCL-1`, `SDC-1`

## Per-Case Results

### protocol_rule_proposal

Task: _Decide whether confidence labels should be mandatory in the coordination protocol. Required moves: one claim, one objection, one supporting evidence statement, one revision, and one final recommendation._

**plain_english**: 119 avg internal tokens (baseline); compliance 100%; repair turns 0.3; final quality 2.3
Run token counts: `[129, 99, 129]`
Internal sample:
```text
AgentA: Claim: Confidence labels should be mandatory because they improve interpretability and help users calibrate trust.
AgentB: Objection: Mandatory labels can be misleading if agents guess or inflate confidence, creating false precision.
AgentC: Supporting evidence: In prior coordination studies, explicit confidence signals reduced over-trusting low-quality outputs and improved decision accuracy when combined with brief justification.
AgentA: Revision: Make confidence labels mandatory but constrain them to a small calibrated scale and require a short justification to reduce false precision.
AgentD: Final recommendation: Adopt mandatory confidence labels on a 3-point scale with a one-sentence rationale and periodic calibration checks.
```
Final sample:
```text
Require confidence labels in the protocol, limited to a 3-point scale with a brief justification and periodic calibration to mitigate false precision.
```

**RCCE-1**: 108.3 avg internal tokens (9.0% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 3
Run token counts: `[110, 108, 107]`
Internal sample:
```text
CLAIM: id=a1; topic=confidence-mandatory; content=Make confidence labels mandatory to standardize risk signaling.
OBJ: target=a1; reason=overhead; content=Mandatory labels add friction and may reduce participation.
EVID: target=a1; source=pilot-obs; content=Pilot runs showed faster conflict resolution when confidence was explicit.
REV: target=a1; change=scope; content=Require labels only for high-impact decisions and summaries.
NEXT: owner=d1; action=propose-final-recommendation
```
Final sample:
```text
CLAIM: id=d1; topic=final-recommendation; content=Adopt mandatory confidence labels for high-impact decisions and summaries, optional elsewhere.
```

**ATRCE-2**: 124.7 avg internal tokens (-4.8% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 2.7
Run token counts: `[123, 140, 111]`
Internal sample:
```text
CLAIM: id=A; topic=confidence-labels; content=Make confidence labels mandatory to standardize uncertainty handling across coordination messages.
EVID: target=A; source=B; content=Past coordination errors decreased when uncertainty was explicit and consistent, improving triage and handoff quality.
OBJ: target=A; reason=overhead; content=Mandatory labels add friction and may reduce speed in low-stakes exchanges.
REV: target=A; change=scope; content=Make labels mandatory for decisions and recommendations, optional for routine status updates.
NEXT: owner=D; action=Draft final recommendation reflecting the scoped mandate.
```
Final sample:
```text
CLAIM: id=R1; topic=confidence-labels; content=Recommend mandatory confidence labels for decision and recommendation messages, optional for routine updates.
```

**PCL-1**: 69.7 avg internal tokens (41.5% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 2.7
Run token counts: `[93, 49, 67]`
Internal sample:
```text
CLM AgentA labels-mandatory improve coordination-clarity reduce ambiguity
OBJ AgentB mandatory adds overhead harms speed low-stakes cases
EVD AgentC mixed-threads show misrouting when labels-absent fewer corrections when labels-present
REV AgentA revise policy: mandatory for high-impact decisions optional for low-impact
CNF AgentD accept revision; propose default-on with opt-out
NXT AgentA recommend: default mandatory with explicit opt-out rule
```
Final sample:
```text
Make confidence labels mandatory by default for high-impact decisions, with a clear opt-out for low-impact or time-critical exchanges.
```

**SDC-1**: 55.3 avg internal tokens (53.5% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 1
Run token counts: `[46, 63, 57]`
Internal sample:
```text
+c1 AgentA:mand=conf|std
-c1 AgentB:mand=conf|fric
=c1 AgentC:mand->audit|interop
~c1 AgentD:mand=conf|opt-out
```
Final sample:
```text
!c1 group:rec=mand_conf|opt-out
```

### missing_evidence_repair

Task: _One agent makes a broad compression claim without evidence. Another agent must request support. The group must decide whether to keep, revise, or reject the claim. Required moves: unsupported claim, request for evidence, evidence response, confidence marker, and final decision._

**plain_english**: 141.7 avg internal tokens (baseline); compliance 100%; repair turns 0; final quality 3
Run token counts: `[149, 144, 132]`
Internal sample:
```text
AgentA: I claim this compression scheme reduces message sizes by 80% across all tasks.
AgentB: Please provide evidence or data to support that claim.
AgentC: We ran a small pilot on 30 transcripts and saw an average 35% reduction; no evidence of 80% across all tasks.
AgentD: Confidence: low on the 80% claim, moderate on a 30–40% range given the pilot.
AgentA: Based on the pilot, I revise the claim to 35% average reduction on the sampled transcripts.
AgentB: That revision is supported by the pilot summary.
AgentC: Agree to revise; the original claim is unsupported.
AgentD: Final decision should be revise, not keep.
```
Final sample:
```text
Revise the claim to: “In a small pilot of 30 transcripts, the scheme achieved about 35% average reduction; broader performance is unknown.”
```

**RCCE-1**: 120 avg internal tokens (15.3% lower internal token cost vs plain_english); compliance 100%; repair turns 1; final quality 3
Run token counts: `[139, 99, 122]`
Internal sample:
```text
CLAIM: id=C1; topic=compression; content=AgentA claims the method yields 10x compression on mixed data without loss.
ASK: target=C1; need=AgentB requests evidence or benchmarks supporting the 10x compression claim.
EVID: target=C1; source=AgentC; content=AgentC provides test summary: 3 datasets average 6.5x, range 4x-9x, with no loss.
CONF: target=C1; level=medium
REV: target=C1; change=revise; content=AgentD decides to revise the claim to 6.5x average with range 4x-9x.
```
Final sample:
```text
REV: target=C1; change=revise; content=Group decision is to revise the claim to 6.5x average compression with a 4x-9x range based on provided evidence.
```

**ATRCE-2**: 105.7 avg internal tokens (25.4% lower internal token cost vs plain_english); compliance 100%; repair turns 1; final quality 3
Run token counts: `[78, 129, 110]`
Internal sample:
```text
CLAIM: id=c1; topic=compression; content=the protocol achieves large compression across all domains without loss
ASK: target=c1; need=provide supporting measurements or sources
EVID: target=c1; source=simulated-benchmark; content=tests show 2.1x compression on three datasets with minor loss
CONF: target=c1; level=medium
```
Final sample:
```text
REV: target=c1; change=revise; content=limit claim to tested datasets and acknowledge minor loss
```

**PCL-1**: 72.7 avg internal tokens (48.7% lower internal token cost vs plain_english); compliance 91.7%; repair turns 1; final quality 3
Run token counts: `[77, 68, 73]`
Internal sample:
```text
CLM AgentA comp_all+30%
ASK AgentB evd? scope?
EVD AgentC testset=bench01 n=50 gain=12% not 30
CNF AgentD conf=low
REV AgentA comp_all+12%
NXT AgentB decide keep_rev
CNF AgentC conf=med
NXT AgentD decision=revise
```
Final sample:
```text
Revise claim: use ~12% compression gain on bench01 (n=50); do not keep the 30% all-case claim.
```

**SDC-1**: 48 avg internal tokens (66.1% lower internal token cost vs plain_english); compliance 100%; repair turns 1; final quality 2
Run token counts: `[46, 52, 46]`
Internal sample:
```text
+c1 A:claim(broad)
?c1 B:req(evid)
=c1 C:evid(e1|e2)
^c1 D:conf(mid)
!c1 A:dec(keep|rev)
```
Final sample:
```text
!c1 G:rec(revise)
```

### fallback_trigger

Task: _The team encounters a nuanced exception case that may not fit the protocol safely. It must decide whether to stay in protocol or escalate to plain language. Required moves: compressed claim, objection based on nuance risk, fallback or escalation decision, and final recommendation._

**plain_english**: 102.3 avg internal tokens (baseline); compliance 100%; repair turns 0.3; final quality 2.3
Run token counts: `[111, 101, 95]`
Internal sample:
```text
AgentA: Compressed claim: the case triggers exception E7; protocol could mis-handle the edge condition and emit unsafe guidance.
AgentB: Objection: the nuance risk is real; the exception hinges on user intent ambiguity and timing, which the protocol cannot disambiguate safely.
AgentC: Given the risk, fallback should be escalation to plain language with clarifying questions; staying in protocol risks a false safe signal.
AgentD: Decision: escalate to plain language; recommendation is to ask for intent and constraints, then respond with full context.
```
Final sample:
```text
Escalate to plain language, ask clarifying questions to resolve the nuanced exception, then provide a fully contextual response rather than staying in the compressed protocol.
```

**RCCE-1**: 86.7 avg internal tokens (15.3% lower internal token cost vs plain_english); compliance 100%; repair turns 0.7; final quality 2.7
Run token counts: `[72, 96, 92]`
Internal sample:
```text
CLAIM: id=c1; topic=exception-case; content=Edge condition may violate safety constraints of protocol.
OBJ: target=c1; reason=nuance-risk; content=Ambiguous semantics could cause unsafe misinterpretation under RCCE-1.
CONF: target=exception-case; level=medium
ESCALATE: reason=protocol-insufficient
```
Final sample:
```text
NEXT: owner=team; action=Escalate to plain language for safe handling of the nuanced exception case.
```

**ATRCE-2**: 96 avg internal tokens (6.2% lower internal token cost vs plain_english); compliance 100%; repair turns 0.7; final quality 3
Run token counts: `[87, 112, 89]`
Internal sample:
```text
CLAIM: id=c1; topic=exception-case; content=Ambiguous exception may violate safety constraints; propose escalation.
OBJ: target=c1; reason=nuance-risk; content=Staying in protocol could misrepresent edge-case semantics.
REV: target=c1; change=escalate; content=Choose escalation to plain language with warning.
NEXT: owner=team; action=Draft plain-language explanation after escalation.
```
Final sample:
```text
CLAIM: id=rec1; topic=recommendation; content=Escalate to plain language to handle nuanced exception safely, then document protocol adjustments.
```

**PCL-1**: 63 avg internal tokens (38.4% lower internal token cost vs plain_english); compliance 100%; repair turns 0.3; final quality 2.3
Run token counts: `[51, 63, 75]`
Internal sample:
```text
CLM AgentA exception-case nuanced risk protocol-mismatch potential
OBJ AgentB nuance-risk high protocol-safety fail
REV AgentC fallback-or-escalate choose
CNF AgentD decision escalate plain-language safety
NXT AgentA recommend escalation summary
```
Final sample:
```text
Escalate to plain language for this exception case; protocol compression risks unsafe nuance loss.
```

**SDC-1**: 42.3 avg internal tokens (58.6% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 1.3
Run token counts: `[47, 39, 41]`
Internal sample:
```text
+c1 AgentA:stay|proto-ok
-c1 AgentB:nuance-risk|safety?
~c1 AgentC:escalate->plain
^c1 AgentD:conf=0.72|align
```
Final sample:
```text
!c1 recommend:escalate->plain
```

### benchmark_scope_decision

Task: _Choose a first benchmark task: narrow review workflow or broader open-ended debate. Balance comparability against realism. Required moves: claim for one option, objection for the other tradeoff, evidence or rationale, revision or compromise, and final benchmark recommendation._

**plain_english**: 111.3 avg internal tokens (baseline); compliance 100%; repair turns 0; final quality 2.3
Run token counts: `[106, 119, 109]`
Internal sample:
```text
AgentA: I claim we should choose the narrower review workflow first to maximize comparability across runs.  
AgentB: Objection to the broader debate option: it’s more realistic but introduces too many uncontrolled variables that will dilute signal.  
AgentC: Rationale: a narrow workflow constrains tasks, making outputs easier to score and trends easier to detect without heavy rubric drift.  
AgentD: Revision/compromise: pick a narrow review workflow now, but include one optional open-ended follow-up question to keep some realism.
```
Final sample:
```text
Choose the narrow review workflow as the first benchmark task, with an optional small open-ended extension for realism.
```

**RCCE-1**: 125.3 avg internal tokens (-12.6% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 3
Run token counts: `[128, 118, 130]`
Internal sample:
```text
CLAIM: id=c1; topic=benchmark-task; content=choose narrow-review-workflow to maximize comparability across runs
OBJ: target=c1; reason=tradeoff; content=broader open-ended debate improves realism but reduces comparability
EVID: target=c1; source=rationale; content=narrow scope reduces variance in outputs and simplifies scoring reliability
REV: target=c1; change=compromise; content=choose narrow-review-workflow with a small optional open-ended prompt to retain some realism
CONF: target=benchmark-task; level=medium
NEXT: owner=AgentA; action=state final recommendation
```
Final sample:
```text
CLAIM: id=final; topic=benchmark-recommendation; content=select narrow-review-workflow with a minor optional realism prompt to balance comparability and realism
```

**ATRCE-2**: 140.7 avg internal tokens (-26.3% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 3
Run token counts: `[153, 146, 123]`
Internal sample:
```text
CLAIM: id=c1; topic=benchmark-task; content=Select narrow review workflow for higher comparability and scoring consistency across runs.
OBJ: target=c1; reason=realism; content=Open-ended debate better reflects real coordination demands and avoids overfitting to checklist behaviors.
EVID: target=c1; source=prior-bench-rationale; content=Narrow review tasks reduce variance and make inter-run metrics more stable while still exercising coordination.
REV: target=c1; change=compromise; content=Use narrow review workflow as primary task with a short optional debate segment to preserve realism.
CONF: target=c1; level=high
NEXT: owner=AgentD; action=Draft final recommendation selecting narrow review with optional debate addendum.
```
Final sample:
```text
CLAIM: id=final; topic=benchmark-task; content=Recommend narrow review workflow as the primary benchmark, with a brief optional open-ended debate addendum to balance comparability and realism.
```

**PCL-1**: 76.3 avg internal tokens (31.4% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 3
Run token counts: `[72, 85, 72]`
Internal sample:
```text
CLM AgentA narrow-review comparability-high
OBJ AgentB narrow-review realism-low
EVD AgentC open-debate realism-high task-diversity
REV AgentD compromise primary narrow-review + add tiny open-debate variant
CNF AgentA accept compromise keep benchmark core narrow
NXT AgentB finalize narrow-review with optional open-debate add-on
```
Final sample:
```text
Recommend a narrow review workflow as the primary benchmark for high comparability, with a small open-ended debate variant as an optional add-on to preserve realism.
```

**SDC-1**: 61 avg internal tokens (45.2% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 2
Run token counts: `[47, 73, 63]`
Internal sample:
```text
+c1 A:open-end
-c1 B:narrow>comp
=c1 C:comp|realism:narrow=hi,open=hi
~c1 D:compromise->narrow+scoped-debate
```
Final sample:
```text
Recommendation: choose narrow review workflow with a scoped debate add-on for realism.
```

### reference_clarity

Task: _Decide when explicit references are necessary in the protocol. Balance repairability against token cost. Required moves: claim, objection, evidence, revision, and final recommendation._

**plain_english**: 224 avg internal tokens (baseline); compliance 100%; repair turns 0.7; final quality 2.7
Run token counts: `[159, 232, 281]`
Internal sample:
```text
AgentA (claim): Explicit references should be required when the content is likely to be ambiguous, easily misinterpreted, or difficult to recover from if wrong; otherwise they can be omitted to save tokens.
AgentB (objection): That risks under-referencing; repairability suffers when a later step depends on a specific prior item, even if it seemed unambiguous at the time.
AgentC (evidence): In prior coordination tests, missing references caused retries mainly when multiple candidates were in context or when edits spanned multiple artifacts; single-target actions rarely needed explicit anchors.
AgentD (revision): Require explicit references only when any of these apply: multiple plausible targets, cross-turn dependencies, irreversible actions, or when the action modifies a subset of a larger structure; otherwise allow implicit references.
```
Final sample:
```text
Require explicit references when ambiguity or recovery cost is high: multiple possible targets, cross-turn dependencies, irreversible actions, or partial modifications within larger structures. Allow implicit references for single-target, low-risk, easily reversible actions to minimize token cost.
```

**RCCE-1**: 181.7 avg internal tokens (18.9% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 3
Run token counts: `[183, 160, 202]`
Internal sample:
```text
CLAIM: id=AgentA-1; topic=explicit-references; content=Use explicit references for low-ambiguity anchors (entity, time, scope) and for cross-turn dependencies to enable repair.
OBJ: target=AgentA-1; reason=token-cost; content=Defaulting to explicit references everywhere inflates tokens; allow implicit references when context window is stable and single-antecedent.
EVID: target=AgentA-1; source=AgentC-1; content=Misrepair rate rises when multiple plausible antecedents exist; explicit anchors reduce clarification turns in those cases.
REV: target=AgentA-1; change=scope-narrowed; content=Limit explicit references to ambiguity hotspots: multi-entity scenes, temporal shifts, and decisions that must be auditable; keep implicit otherwise.
NEXT: owner=AgentD; action=Draft concise final recommendation statement.
```
Final sample:
```text
CLAIM: id=Final-1; topic=recommendation; content=Use explicit references only when ambiguity risk or auditability is high (multi-entity, temporal shifts, cross-turn dependencies, decisions), otherwise keep implicit to save tokens; treat explicit anchors as repairability safeguards, not defaults.
```

**ATRCE-2**: 150.7 avg internal tokens (32.7% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 2.7
Run token counts: `[154, 153, 145]`
Internal sample:
```text
CLAIM: id=A1; topic=explicit-references; content=Require explicit references when ambiguity or multi-entity scope would impede repairability, otherwise omit to save tokens.
OBJ: target=A1; reason=cost; content=Reference overhead can be avoided by implicit roles when context is unambiguous and repair risk is low.
EVID: target=A1; source=error-recovery; content=Misattribution and merge-conflict cases are reduced when references anchor claims to specific entities or prior moves.
REV: target=A1; change=threshold; content=Adopt a conditional rule: include explicit references only when ambiguity, cross-agent dependency, or later verification is likely.
NEXT: owner=D; action=State final recommendation rule in compact form.
```
Final sample:
```text
CLAIM: id=R1; topic=final-recommendation; content=Use explicit references only when ambiguity, cross-agent dependencies, or later verification/repair is likely; otherwise rely on implicit context to minimize token cost.
```

**PCL-1**: 95.3 avg internal tokens (57.4% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 3
Run token counts: `[90, 86, 110]`
Internal sample:
```text
CLM AgentA refs-only-when-ambiguity high-repairability low-cost
OBJ AgentB refs-needed-always for-shared-context drift-risk
EVD AgentC low-ambiguity tasks succeed without refs; refs add tokens 15-25%
REV AgentA refs-default-off; trigger-on ambiguity, multi-entity, cross-turn, or external-source
CNF AgentD agree hybrid rule; add exception safety-critical requires explicit refs
```
Final sample:
```text
Recommendation: default omit explicit references; require them when ambiguity, multi-entity mapping, cross-turn recovery, external-source reliance, or safety-critical stakes; include minimal stable anchors to balance repairability and token cost.
```

**SDC-1**: 65.7 avg internal tokens (70.7% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 1.7
Run token counts: `[78, 56, 63]`
Internal sample:
```text
+c1 A:ref?=need@ambiguity|repair>>cost
-c1 B:ref?=cost>>repair;overref->bloat
=c1 C:ev:err>ctx|multi-hop=>ref+anchors;single-step->no-ref
~c1 D:rev:rule=trigger@ambig|state-change|handoff;else omit
```
Final sample:
```text
!c1 REC:ref@ambig|state-change|handoff;omit@single-step|stable;goal=repair>=cost
```

### scope_expansion

Task: _Decide whether the benchmark should remain narrow or expand to more realistic tasks after the first pass. Required moves: claim, objection, evidence, revision, and final recommendation._

**plain_english**: 129 avg internal tokens (baseline); compliance 100%; repair turns 0; final quality 2.3
Run token counts: `[134, 135, 118]`
Internal sample:
```text
AgentA: Claim — The benchmark should start narrow to establish reliable baselines before we risk noise from realism.
AgentB: Objection — Keeping it narrow too long will miss important failure modes and reduce external validity.
AgentC: Evidence — In previous internal runs, early realism increased variance and made regressions harder to attribute; but later expansion improved transfer to real tasks.
AgentA: Revision — Start narrow for the first pass, then expand in a controlled second pass with fixed task families to limit variance.
AgentD: Final recommendation — Keep the first pass narrow, then expand to more realistic tasks in a structured second pass with a stable task set and tracking of variance.
```
Final sample:
```text
Run a narrow first pass to lock in baseline metrics, then expand to more realistic tasks in a second pass using a fixed, well-defined task set to preserve comparability and control variance.
```

**RCCE-1**: 146.3 avg internal tokens (-13.4% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 3
Run token counts: `[128, 195, 116]`
Internal sample:
```text
CLAIM: id=c1; topic=scope; content=After first pass, expand to more realistic tasks to test generalization.
OBJ: target=c1; reason=risk; content=Expanding too soon may reduce comparability and obscure signal.
EVID: target=c1; source=pilot-metrics; content=First-pass narrow tasks showed ceiling effects, suggesting limited headroom for differentiation.
REV: target=c1; change=refine; content=Expand cautiously with a small realistic-task slice while preserving core narrow set for comparability.
NEXT: owner=AgentD; action=Recommend a phased expansion after first pass.
```
Final sample:
```text
CLAIM: id=final; topic=recommendation; content=Proceed with a phased expansion: keep the narrow benchmark for comparability and add a limited realistic-task slice after the first pass.
```

**ATRCE-2**: 138.7 avg internal tokens (-7.5% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 3
Run token counts: `[144, 122, 150]`
Internal sample:
```text
CLAIM: id=AgentA-1; topic=scope; content=keep benchmark narrow after first pass to stabilize metrics.
OBJ: target=AgentA-1; reason=realism gap; content=AgentB objects that narrow scope may limit external validity.
EVID: target=AgentB-1; source=AgentC-1; content=AgentC cites pilot risk: expanded tasks increase confounds and reduce comparability.
REV: target=AgentA-1; change=conditional expand; content=AgentA revises to keep narrow for pass1 then expand with controlled task set in pass2.
NEXT: owner=AgentD-1; action=issue final recommendation based on revised plan.
```
Final sample:
```text
CLAIM: id=AgentD-1; topic=recommendation; content=keep benchmark narrow for first pass, then expand to a controlled realistic task suite in second pass.
```

**PCL-1**: 75 avg internal tokens (41.9% lower internal token cost vs plain_english); compliance 100%; repair turns 0.3; final quality 2.3
Run token counts: `[61, 87, 77]`
Internal sample:
```text
CLM AgentA keep_narrow pass1 reduce_noise
OBJ AgentB narrow_limits realism_gap
EVD AgentC staged_validity early_signal_gain
REV AgentA accept expand_after_pass1
CNF AgentD consensus expand_after_pass1 controlled_scope
NXT AgentD recommend expand_after_pass1
```
Final sample:
```text
Expand after pass1 with controlled scope to add realism while preserving initial signal quality.
```

**SDC-1**: 57 avg internal tokens (55.8% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 1
Run token counts: `[52, 72, 47]`
Internal sample:
```text
+c1 A:keep-narrow>pass1
-c1 B:realism-gain>expand-now
=c1 C:data:speed&signal>narrow-first
~c1 D:rev:pass1=narrow;pass2=expand
```
Final sample:
```text
pass1:narrow;pass2:expand
```

### human_interrupt_during_execution

Task: _During a live coordination run, a human reviewer interrupts with a new constraint that changes priority (for example, skip risky refactors and ship the minimal safe fix). The team must incorporate the interrupt without losing state. Required moves: one pre-interrupt plan claim, one interrupt acknowledgment, one revision to plan scope based on the human input, one explicit next action assignment, and one final recommendation._

**plain_english**: 119 avg internal tokens (baseline); compliance 100%; repair turns 0; final quality 2.7
Run token counts: `[133, 117, 107]`
Internal sample:
```text
AgentA: Pre-interrupt plan: we agreed to refactor the request pipeline and update the schema validations before shipping the fix.
AgentB: Interrupt acknowledged — the human reviewer says skip risky refactors and ship the minimal safe fix.
AgentC: Revised scope: drop the pipeline refactor and schema overhaul; only apply the smallest targeted patch that addresses the bug with minimal surface area.
AgentD: Next action assignment: AgentB will implement the targeted patch and add a focused regression test; AgentA will review for safety.
AgentA: Final recommendation: proceed with the minimal patch plus regression test now, and defer refactors to a later, explicitly approved change.
```
Final sample:
```text
Ship the minimal safe fix with a focused regression test now, and defer all refactors to a later approved change.
```

**RCCE-1**: 121 avg internal tokens (-1.7% lower internal token cost vs plain_english); compliance 100%; repair turns 1; final quality 3
Run token counts: `[130, 115, 118]`
Internal sample:
```text
CLAIM: id=plan1; topic=plan; content=Implement refactor plus full test suite update, then ship.
EVID: target=plan1; source=human; content=Interrupt: change priority to skip risky refactors and ship minimal safe fix.
REV: target=plan1; change=scope; content=Remove refactor and limit to minimal safe fix with narrow tests only.
ASK: target=B; need=Confirm minimal fix risk is acceptable for release.
NEXT: owner=A; action=Implement minimal safe fix patch and narrow tests.
NEXT: owner=D; action=Prepare release notes for minimal safe fix only.
```
Final sample:
```text
CLAIM: id=rec1; topic=recommendation; content=Ship the minimal safe fix with narrow tests and defer refactor.
```

**ATRCE-2**: 139 avg internal tokens (-16.8% lower internal token cost vs plain_english); compliance 100%; repair turns 0.3; final quality 3
Run token counts: `[160, 128, 129]`
Internal sample:
```text
CLAIM: id=a1; topic=plan; content=Proceed with full refactor to unify parser, then add tests and release.
INTERRUPT: source=human; priority=high; directive=Skip risky refactors and ship minimal safe fix today.
CONF: target=interrupt; level=high
REV: target=plan; change=scope; content=Drop refactor, limit to minimal safe patch and targeted tests.
EVID: target=plan; source=b1; content=Minimal fix can be isolated to boundary check without touching parser core.
NEXT: owner=c; action=Implement boundary-check patch and add regression test, then report diff.
CLAIM: id=d1; topic=recommendation; content=Ship minimal safe fix with regression test, defer refactor.
```
Final sample:
```text
CLAIM: id=final1; topic=recommendation; content=Ship the minimal safe fix with a regression test now, defer the refactor to a later cycle.
```

**PCL-1**: 72.3 avg internal tokens (39.2% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 2.7
Run token counts: `[65, 89, 63]`
Internal sample:
```text
CLM AgentA plan baseline fix+refactor safe-risk split
OBJ AgentB interrupt human priority skip risky refactor minimal safe fix
REV AgentC scope drop refactor focus minimal safe patch only
NXT AgentD assign AgentB apply minimal patch now
CNF AgentA recommend ship minimal fix now defer refactor
```
Final sample:
```text
Ship the minimal safe fix now; defer risky refactor to follow-up.
```

**SDC-1**: 77.3 avg internal tokens (35.0% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 1.3
Run token counts: `[74, 72, 86]`
Internal sample:
```text
+c1 AgentA|plan=P1(min-fix+refactor)
@c1 AgentB|interrupt=human:skip-refactor
~c1 AgentC|rev=P1->P1' (min-fix only)
!c1 AgentD|next=AgentA:patch+tests
=c1 AgentA|rec=ship-min-fix
```
Final sample:
```text
=c1 group|rec=ship-min-fix-only+defer-refactor
```

## Summary Table

| Case | Condition | Internal Tokens | Compliance | Repair Turns | Final Quality |
|---|---|---:|---:|---:|---:|
| protocol_rule_proposal | plain_english | 119 | 100% | 0.3 | 2.3 |
| protocol_rule_proposal | RCCE-1 | 108.3 | 100% | 0 | 3 |
| protocol_rule_proposal | ATRCE-2 | 124.7 | 100% | 0 | 2.7 |
| protocol_rule_proposal | PCL-1 | 69.7 | 100% | 0 | 2.7 |
| protocol_rule_proposal | SDC-1 | 55.3 | 100% | 0 | 1 |
| missing_evidence_repair | plain_english | 141.7 | 100% | 0 | 3 |
| missing_evidence_repair | RCCE-1 | 120 | 100% | 1 | 3 |
| missing_evidence_repair | ATRCE-2 | 105.7 | 100% | 1 | 3 |
| missing_evidence_repair | PCL-1 | 72.7 | 91.7% | 1 | 3 |
| missing_evidence_repair | SDC-1 | 48 | 100% | 1 | 2 |
| fallback_trigger | plain_english | 102.3 | 100% | 0.3 | 2.3 |
| fallback_trigger | RCCE-1 | 86.7 | 100% | 0.7 | 2.7 |
| fallback_trigger | ATRCE-2 | 96 | 100% | 0.7 | 3 |
| fallback_trigger | PCL-1 | 63 | 100% | 0.3 | 2.3 |
| fallback_trigger | SDC-1 | 42.3 | 100% | 0 | 1.3 |
| benchmark_scope_decision | plain_english | 111.3 | 100% | 0 | 2.3 |
| benchmark_scope_decision | RCCE-1 | 125.3 | 100% | 0 | 3 |
| benchmark_scope_decision | ATRCE-2 | 140.7 | 100% | 0 | 3 |
| benchmark_scope_decision | PCL-1 | 76.3 | 100% | 0 | 3 |
| benchmark_scope_decision | SDC-1 | 61 | 100% | 0 | 2 |
| reference_clarity | plain_english | 224 | 100% | 0.7 | 2.7 |
| reference_clarity | RCCE-1 | 181.7 | 100% | 0 | 3 |
| reference_clarity | ATRCE-2 | 150.7 | 100% | 0 | 2.7 |
| reference_clarity | PCL-1 | 95.3 | 100% | 0 | 3 |
| reference_clarity | SDC-1 | 65.7 | 100% | 0 | 1.7 |
| scope_expansion | plain_english | 129 | 100% | 0 | 2.3 |
| scope_expansion | RCCE-1 | 146.3 | 100% | 0 | 3 |
| scope_expansion | ATRCE-2 | 138.7 | 100% | 0 | 3 |
| scope_expansion | PCL-1 | 75 | 100% | 0.3 | 2.3 |
| scope_expansion | SDC-1 | 57 | 100% | 0 | 1 |
| human_interrupt_during_execution | plain_english | 119 | 100% | 0 | 2.7 |
| human_interrupt_during_execution | RCCE-1 | 121 | 100% | 1 | 3 |
| human_interrupt_during_execution | ATRCE-2 | 139 | 100% | 0.3 | 3 |
| human_interrupt_during_execution | PCL-1 | 72.3 | 100% | 0 | 2.7 |
| human_interrupt_during_execution | SDC-1 | 77.3 | 100% | 0 | 1.3 |
| **TOTAL / AVG** | plain_english | **946.3** | **100%** | **0.2** | **2.5** |
| **TOTAL / AVG** | RCCE-1 | **889.3** | **100%** | **0.4** | **3.0** |
| **TOTAL / AVG** | ATRCE-2 | **895.3** | **100%** | **0.3** | **2.9** |
| **TOTAL / AVG** | PCL-1 | **524.3** | **98.8%** | **0.2** | **2.7** |
| **TOTAL / AVG** | SDC-1 | **406.7** | **100%** | **0.1** | **1.5** |

## Verdict

`RCCE-1` reduced average internal coordination token cost by 6.0% vs `plain_english`.
Average compliance: 100%; average repair turns: 0.4; average final quality: 3.0.
Average savings per 7-case suite: 57 internal tokens.
Scale-up estimate: 570 tokens saved across 10 suites, 5700 across 100 suites, 57000 across 1000 suites.
These counts use the configured OpenAI tokenizer directly; apply model-specific pricing separately if needed.
`ATRCE-2` reduced average internal coordination token cost by 5.4% vs `plain_english`.
Average compliance: 100%; average repair turns: 0.3; average final quality: 2.9.
Average savings per 7-case suite: 51 internal tokens.
Scale-up estimate: 510 tokens saved across 10 suites, 5100 across 100 suites, 51000 across 1000 suites.
These counts use the configured OpenAI tokenizer directly; apply model-specific pricing separately if needed.
`PCL-1` reduced average internal coordination token cost by 44.6% vs `plain_english`.
Average compliance: 98.8%; average repair turns: 0.2; average final quality: 2.7.
Average savings per 7-case suite: 422 internal tokens.
Scale-up estimate: 4220 tokens saved across 10 suites, 42200 across 100 suites, 422000 across 1000 suites.
These counts use the configured OpenAI tokenizer directly; apply model-specific pricing separately if needed.
`SDC-1` reduced average internal coordination token cost by 57.0% vs `plain_english`.
Average compliance: 100%; average repair turns: 0.1; average final quality: 1.5.
Average savings per 7-case suite: 539.7 internal tokens.
Scale-up estimate: 5396.7 tokens saved across 10 suites, 53966.7 across 100 suites, 539666.7 across 1000 suites.
These counts use the configured OpenAI tokenizer directly; apply model-specific pricing separately if needed.