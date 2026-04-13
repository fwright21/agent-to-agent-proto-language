# Coordination Benchmark Results

Generated: 2026-04-08 20:20

Runner: `codex`

Count mode: `openai_exact`

Codex model: `gpt-5.2-codex`

Repeats per condition/case: `1`

Baseline: `plain_english`

Conditions: `plain_english`, `RCCE-1`, `ATRCE-2`, `PCL-1`, `SDC-1`

## Per-Case Results

### protocol_rule_proposal

Task: _Decide whether confidence labels should be mandatory in the coordination protocol. Required moves: one claim, one objection, one supporting evidence statement, one revision, and one final recommendation._

**plain_english**: 112 avg internal tokens (baseline); compliance 100%; repair turns 0; final quality 3
Run token counts: `[112]`
Internal sample:
```text
AgentA: Claim: Confidence labels should be mandatory to make uncertainty explicit and reduce misinterpretation.
AgentB: Objection: Mandatory labels add overhead and can be gamed, which may distract from substance.
AgentC: Supporting evidence: In prior collaborations, teams that labeled confidence resolved disagreements faster because they could target verification effort.
AgentD: Revision: Make labels mandatory only for decisions that impact safety, policy, or external commitments; optional elsewhere.
AgentA: Final recommendation: Adopt mandatory confidence labels for high-stakes decisions and optional labels for routine coordination.
```
Final sample:
```text
Require confidence labels for high-stakes or externally visible decisions, and keep them optional for routine internal exchanges.
```

**RCCE-1**: 113 avg internal tokens (-0.9% lower internal token cost vs plain_english); compliance 0%; repair turns 0; final quality 3
Run token counts: `[113]`
Internal sample:
```text
CLAIM: agent=AgentA; content=Confidence labels should be mandatory to standardize reliability cues.
OBJ: agent=AgentB; content=Mandatory labels may add overhead and reduce speed in routine exchanges.
EVID: agent=AgentC; content=Mandatory labels improve triage because recipients can prioritize low-confidence items for verification.
REV: agent=AgentA; content=Revise to require labels only for high-risk or decision-bearing messages.
NEXT: agent=AgentD; content=Recommend mandatory confidence labels for high-risk/decision messages; optional otherwise.
```
Final sample:
```text
NEXT: content=Adopt mandatory confidence labels for high-risk or decision-bearing messages; optional for routine updates.
```

**ATRCE-2**: 99 avg internal tokens (11.6% lower internal token cost vs plain_english); compliance 0%; repair turns 1; final quality 2
Run token counts: `[99]`
Internal sample:
```text
CLAIM: agent=AgentA; topic=confidence_labels; position=mandatory
OBJ: agent=AgentB; target=AgentA; reason=adds_overhead_for_low_risk_exchanges
EVID: agent=AgentC; support=clarifies_uncertainty_and_reduces_misinterpretation
REV: agent=AgentA; update=mandatory_for_decisions_optional_for_routine_status
ASK: agent=AgentD; question=what_threshold_defines_decisions
```
Final sample:
```text
NEXT: recommendation=make_confidence_labels_mandatory_for_decisions_optional_for_routine_status; rationale=balances_clarity_with_overhead
```

**PCL-1**: 63 avg internal tokens (43.8% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 2
Run token counts: `[63]`
Internal sample:
```text
CLM AgentA label-mandatory boosts-trust reduce-ambiguity
OBJ AgentB mandatory adds-friction blocks-rapid
EVD AgentC misread-rate high when label-absent
REV AgentA accept-scope label-required for critical messages
NXT AgentD recommend mandatory-critical optional-else
```
Final sample:
```text
CNF Group require-label critical optional routine
```

**SDC-1**: 42 avg internal tokens (62.5% lower internal token cost vs plain_english); compliance 0%; repair turns 0; final quality 1
Run token counts: `[42]`
Internal sample:
```text
+ AgentA:conf>mandatory
- AgentB:cost|friction>benefit
= AgentC:auditable|dispute->conf
~ AgentD:mandatory->default|optout
```
Final sample:
```text
! rec:default-conf|optout-highrisk
```

### missing_evidence_repair

Task: _One agent makes a broad compression claim without evidence. Another agent must request support. The group must decide whether to keep, revise, or reject the claim. Required moves: unsupported claim, request for evidence, evidence response, confidence marker, and final decision._

**plain_english**: 95 avg internal tokens (baseline); compliance 100%; repair turns 0; final quality 3
Run token counts: `[95]`
Internal sample:
```text
AgentA: I claim our compression approach will cut bandwidth by 60% across all workloads.
AgentB: Please provide evidence or measurements to support that claim.
AgentA: I don’t have measurements yet; it’s an estimate based on intuition. Confidence: low.
AgentC: With no data and low confidence, we should revise the claim to a testable hypothesis.
AgentD: Agreed; revise it to a proposed target pending benchmarks rather than a guaranteed outcome.
```
Final sample:
```text
Revise the claim to a testable hypothesis with a target reduction pending benchmark evidence.
```

**RCCE-1**: 131 avg internal tokens (-37.9% lower internal token cost vs plain_english); compliance 0%; repair turns 1; final quality 3
Run token counts: `[131]`
Internal sample:
```text
CLAIM: agent=AgentA; claim=We can compress any message by 90% without losing meaning; evidence=none.
ASK: agent=AgentB; to=AgentA; request=Provide evidence or rationale for the 90% compression claim.
EVID: agent=AgentA; evidence=Tested on 20 internal summaries with user ratings unchanged; method=manual comparison.
CONF: agent=AgentC; target=AgentA; confidence=medium; reason=small sample and subjective ratings.
NEXT: agent=AgentD; decision=Revise; revision=Limit claim to tested domain and sample size; keep=conditional.
```
Final sample:
```text
REV: decision=Revise; final_claim=Compression of internal summaries by ~90% preserved meaning in a 20-item subjective test; scope=limited; action=collect broader evidence.
```

**ATRCE-2**: 213 avg internal tokens (-124.2% lower internal token cost vs plain_english); compliance 0%; repair turns 1; final quality 3
Run token counts: `[213]`
Internal sample:
```text
CLAIM: agent=AgentA; claim=We can compress any document to 10 percent length with no loss of meaning; scope=broad; evidence=none.
ASK: agent=AgentB; request=Provide evidence or constraints supporting the 10 percent no-loss compression claim; target=AgentA.
EVID: agent=AgentA; evidence=Lab trial: 100 technical docs, average 12 percent length retained, human judges reported 98 percent meaning preserved; constraint=English technical prose; note=non-peer-reviewed.
OBJ: agent=AgentC; objection=Claim is too broad and evidence is limited to a specific domain and non-reviewed study; risk=overgeneralization.
CONF: agent=AgentD; confidence=medium; rationale=Evidence suggests potential but not universal.
REV: agent=AgentA; revision=We can often compress English technical prose to around 12 percent length with high meaning preservation under human evaluation.
NEXT: agent=AgentB; decision=revise; action=Adopt revised claim and add domain constraints.
```
Final sample:
```text
Adopt the revised, constrained claim; reject the original broad claim as unsupported.
```

**PCL-1**: 46 avg internal tokens (51.6% lower internal token cost vs plain_english); compliance 100%; repair turns 1; final quality 3
Run token counts: `[46]`
Internal sample:
```text
CLM AgentA comp-rate-6x all-tasks
ASK AgentB evd comp-rate-6x
EVD AgentA sample-n3 lab-only
CNF AgentC low
NXT AgentD decision revise
```
Final sample:
```text
NXT group revise comp-rate-6x -> comp-rate-2x low-evidence
```

**SDC-1**: 37 avg internal tokens (61.1% lower internal token cost vs plain_english); compliance 0%; repair turns 0; final quality 2
Run token counts: `[37]`
Internal sample:
```text
AgentA + c:x>y
AgentB ? ev?x
AgentC = ev:a|b
AgentD ^ conf=mid
AgentD ! dec=revise
```
Final sample:
```text
AgentD ! rec=revise c+x?ev+clarify
```

### fallback_trigger

Task: _The team encounters a nuanced exception case that may not fit the protocol safely. It must decide whether to stay in protocol or escalate to plain language. Required moves: compressed claim, objection based on nuance risk, fallback or escalation decision, and final recommendation._

**plain_english**: 123 avg internal tokens (baseline); compliance 100%; repair turns 0; final quality 3
Run token counts: `[123]`
Internal sample:
```text
AgentA: Compressed claim: we should stay in protocol; the exception seems bounded and can be encoded safely with a single extra tag.
AgentB: Objection: nuance risk is high because the exception involves ambiguous intent and could be misinterpreted, which is unsafe in a compressed form.
AgentC: Given the nuance risk, I favor escalation to plain language with explicit caveats rather than a brittle compressed patch.
AgentD: Decision: escalate to plain language for this case; if we later formalize a safe pattern, we can reintroduce protocol. Recommendation: respond in plain language with clear constraints.
```
Final sample:
```text
Escalate to plain language for this nuanced exception, because compressed encoding risks ambiguity; provide an explicit, cautious response and revisit protocol changes only after a safe pattern is defined.
```

**RCCE-1**: 101 avg internal tokens (17.9% lower internal token cost vs plain_english); compliance 0%; repair turns 0; final quality 3
Run token counts: `[101]`
Internal sample:
```text
CLAIM: agent=AgentA; topic=exception-case; summary=nuanced scenario may exceed RCCE-1 safe expression.
OBJ: agent=AgentB; basis=nuance-risk; detail=protocol fields may omit critical qualifiers leading to unsafe guidance.
REV: agent=AgentC; decision=escalate; reason=insufficient expressiveness for safety-critical nuance.
NEXT: agent=AgentD; action=issue-final; recommendation=use ESCALATE and switch to plain language.
```
Final sample:
```text
ESCALATE: agent=Group; decision=exit-protocol; reason=nuanced exception cannot be safely captured in RCCE-1; recommendation=switch to plain language for full context.
```

**ATRCE-2**: 109 avg internal tokens (11.4% lower internal token cost vs plain_english); compliance 0%; repair turns 0; final quality 2
Run token counts: `[109]`
Internal sample:
```text
CLAIM: agent=AgentA; content=Exception case likely unsafe for strict protocol; relevance=compressed; risk=medium.
OBJ: agent=AgentB; content=Nuance risk suggests protocol may misrepresent intent; risk=high; action=challenge.
REV: agent=AgentC; content=Decide escalation to plain language due to safety/nuance limits; decision=escalate.
CONF: agent=AgentD; content=Escalate approved; rationale=protocol_limit; next=plain_language_recommendation.
```
Final sample:
```text
NEXT: decision=escalate; recommendation=use_plain_language_to_handle_exception_safely; rationale=nuance_risk.
```

**PCL-1**: 37 avg internal tokens (69.9% lower internal token cost vs plain_english); compliance 0%; repair turns 0; final quality 2
Run token counts: `[37]`
Internal sample:
```text
AgentA CLM proto-ok nuance-guard
AgentB OBJ nuance-risk edge-case safety-ambig
AgentC ESC plain-language nuance-risk
AgentD CNF escalate plain-language
```
Final sample:
```text
AgentA NXT recommend escalate plain-language
```

**SDC-1**: 46 avg internal tokens (62.6% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 2
Run token counts: `[46]`
Internal sample:
```text
+AgentA nuance?case->risk|proto?ok
-AgentB risk:edge|safety?unclear
~AgentC decision:escalate->plain
!AgentD next:recommend>escalate
```
Final sample:
```text
+Group recommend:escalate->plain
```

### benchmark_scope_decision

Task: _Choose a first benchmark task: narrow review workflow or broader open-ended debate. Balance comparability against realism. Required moves: claim for one option, objection for the other tradeoff, evidence or rationale, revision or compromise, and final benchmark recommendation._

**plain_english**: 134 avg internal tokens (baseline); compliance 100%; repair turns 0; final quality 3
Run token counts: `[134]`
Internal sample:
```text
AgentA: I claim we should choose the narrow review workflow for the first benchmark task because it maximizes comparability across runs and agents.
AgentB: Objection: that tradeoff sacrifices realism; a broader open‑ended debate better reflects real-world coordination under ambiguity.
AgentC: Evidence: narrow review workflows have clearer success criteria and reduce variance, making benchmarking more defensible; open debate adds confounds from topic drift.
AgentD: Revision/compromise: start with a narrow review workflow but include a small open‑ended segment as a secondary task in the same benchmark suite.
AgentA: That compromise preserves comparability while still sampling realism; I support it.
```
Final sample:
```text
Recommend a narrow review workflow as the first benchmark task, with a small open‑ended debate segment appended as a secondary comparison to balance realism and comparability.
```

**RCCE-1**: 76 avg internal tokens (43.3% lower internal token cost vs plain_english); compliance 0%; repair turns 0; final quality 3
Run token counts: `[76]`
Internal sample:
```text
CLAIM: agent=AgentA; option=narrow-review; reason=comparability
OBJ: agent=AgentB; option=broader-debate; tradeoff=comparability-loss
EVID: agent=AgentC; rationale=narrow-review reduces variance and scoring ambiguity
REV: agent=AgentD; compromise=hybrid-narrow-review with optional limited debate prompt
```
Final sample:
```text
NEXT: agent=Group; recommendation=narrow-review with limited debate addendum
```

**ATRCE-2**: 79 avg internal tokens (41.0% lower internal token cost vs plain_english); compliance 0%; repair turns 0; final quality 2
Run token counts: `[79]`
Internal sample:
```text
CLAIM: agent=AgentA; option=narrow-review; reason=comparability-high
OBJ: agent=AgentB; option=broader-debate; tradeoff=realism-lower-comparability
EVID: agent=AgentC; support=narrow-review; rationale=benchmark-repeatability
REV: agent=AgentD; compromise=narrow-review-with-realistic-prompts
```
Final sample:
```text
CONF: recommendation=narrow-review-workflow; note=use-realistic-prompts-for-balance
```

**PCL-1**: 75 avg internal tokens (44.0% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 3
Run token counts: `[75]`
Internal sample:
```text
CLM AgentA choose narrow-review for comparability
OBJ AgentB open-debate gives realism, tradeoff against comparability
EVD AgentC narrow-review yields stable metrics, less topic variance
REV AgentD compromise: narrow-review core + small optional debate slice
NXT AgentA adopt compromise, benchmark baseline narrow with small debate add-on
CNF AgentB ok
```
Final sample:
```text
recommend narrow-review workflow baseline with a small open-debate slice for realism checks
```

**SDC-1**: 69 avg internal tokens (48.5% lower internal token cost vs plain_english); compliance 0%; repair turns 0; final quality 1
Run token counts: `[69]`
Internal sample:
```text
+ AgentA NRW>OED
- AgentB NRW<realism OED>realism
= AgentC comp:NRW>compare|OED>real
~ AgentD mix:NRWcore+OEDedge
^ AgentA 0.68
! AgentB rec:NRWcore+OEDedge
```
Final sample:
```text
NRWcore+OEDedge
```

### reference_clarity

Task: _Decide when explicit references are necessary in the protocol. Balance repairability against token cost. Required moves: claim, objection, evidence, revision, and final recommendation._

**plain_english**: 146 avg internal tokens (baseline); compliance 100%; repair turns 0; final quality 3
Run token counts: `[146]`
Internal sample:
```text
AgentA: Claim: Explicit references are necessary when there is any risk of ambiguity that could break repairability, such as multiple antecedents or cross-turn dependencies.
AgentB: Objection: That rule is too broad and will inflate token cost; we should avoid explicit references unless ambiguity is likely.
AgentC: Evidence: In recent protocol runs, the highest repair costs came from omitted references when multiple entities were active or when instructions depended on a specific prior turn; concise explicit anchors reduced repair steps.
AgentD: Revision: Use explicit references only when there are at least two plausible antecedents, when a dependency spans more than one turn, or when the instruction must bind to a specific artifact or decision; otherwise rely on implicit context.
```
Final sample:
```text
Explicit references are required when ambiguity is likely or repair costs are high: specifically, with multiple plausible antecedents, cross-turn dependencies, or binding to a specific artifact/decision. In all other cases, omit explicit references to save tokens.
```

**RCCE-1**: 112 avg internal tokens (23.3% lower internal token cost vs plain_english); compliance 0%; repair turns 0; final quality 3
Run token counts: `[112]`
Internal sample:
```text
CLAIM: agent=AgentA; point=Explicit references are necessary when ambiguities could block reconstruction or audit.
OBJ: agent=AgentB; point=Too many explicit references raise token cost and slow coordination.
EVID: agent=AgentC; point=Repairs succeed faster when references are included at decision forks or identifier handoffs.
REV: agent=AgentA; update=Limit explicit references to decision forks, handoffs, and conflicting identifiers.
NEXT: agent=AgentD; action=Recommend a minimal-reference rule balancing repairability and cost.
```
Final sample:
```text
CONF: recommendation=Use explicit references only at decision forks, handoffs of identifiers/artifacts, and when conflicting entities could arise; omit elsewhere to reduce token cost.
```

**ATRCE-2**: 149 avg internal tokens (-2.1% lower internal token cost vs plain_english); compliance 0%; repair turns 0; final quality 3
Run token counts: `[149]`
Internal sample:
```text
CLAIM: agent=AgentA; position=Use explicit references when ambiguity or cross-turn dependency exists; rationale=repairability outweighs token cost in those cases.
OBJ: agent=AgentB; target=AgentA; concern=Token cost high; claim=Default to implicit references unless ambiguity proven.
EVID: agent=AgentC; support=Ambiguity spikes in multi-entity or multi-step contexts; outcome=repairs fail without anchors.
REV: agent=AgentB; update=Accept explicit references for multi-entity/multi-step or low-shared-context turns; default=implicit in single-entity, single-step.
NEXT: agent=AgentD; action=Recommend rule set balancing explicit references to ambiguity risk tiers.
```
Final sample:
```text
CONF: recommendation=Use explicit references for multi-entity, multi-step, or low-shared-context turns; allow implicit references for single-entity, single-step, high-shared-context turns to reduce token cost.
```

**PCL-1**: 75 avg internal tokens (48.6% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 3
Run token counts: `[75]`
Internal sample:
```text
CLM AgentA ref_explicit_needed for_ambig_links repair_hi cost_ok
OBJ AgentB ref_explicit_overuse cost_hi alt_context_ok
EVD AgentC logs_show repair_fail when_ref_absent
REV AgentA ref_explicit_only for_dep_links+long_range_ids
CNF AgentD balance repair_gt_cost threshold_len>n or multi_agent
```
Final sample:
```text
NXT Group use_ref when dep_link or long_range or ambig; omit for local_resolvable to save tokens
```

**SDC-1**: 62 avg internal tokens (57.5% lower internal token cost vs plain_english); compliance 0%; repair turns 0; final quality 1
Run token counts: `[62]`
Internal sample:
```text
+ AgentA ref?=>need|repair>cost
- AgentB ref?=>cost>repair|overhead
= AgentC e:ambig>repair|stable<ref
~ AgentD rev:ref?=>ambig|mutable|handoff
! AgentA next:reco
```
Final sample:
```text
+ AgentA reco:ref?=>ambig|mutable|handoff;no-ref=>stable|local
```

### scope_expansion

Task: _Decide whether the benchmark should remain narrow or expand to more realistic tasks after the first pass. Required moves: claim, objection, evidence, revision, and final recommendation._

**plain_english**: 126 avg internal tokens (baseline); compliance 100%; repair turns 0; final quality 2
Run token counts: `[126]`
Internal sample:
```text
AgentA: Claim: Keep the benchmark narrow for the first pass to get clean baseline signals.  
AgentB: Objection: A too-narrow scope risks optimizing for toy tasks and missing real-world failure modes.  
AgentC: Evidence: In prior benchmarks, early broadening increased variance and made it harder to diagnose regressions, while a staged expansion improved interpretability.  
AgentD: Revision: Start narrow for pass one, then expand in pass two with a curated set of realistic tasks to balance signal and relevance.  
AgentA: Final recommendation: Stage it—narrow first pass, targeted expansion after initial analysis.
```
Final sample:
```text
Proceed with a narrow first pass to establish a clear baseline, then expand to a curated set of realistic tasks in the second pass once initial results are reviewed.
```

**RCCE-1**: 101 avg internal tokens (19.8% lower internal token cost vs plain_english); compliance 0%; repair turns 0; final quality 2
Run token counts: `[101]`
Internal sample:
```text
CLAIM: agent=AgentA; position=keep_narrow_after_first_pass; rationale=control_variance_and_cost.
OBJ: agent=AgentB; target=AgentA; concern=narrow_scope_limits_external_validity.
EVID: agent=AgentC; supports=expand_after_first_pass; detail=pilot_results_show_task_realism_improves_error_discovery_rate.
REV: agent=AgentA; update=conditional_expand; condition=if_quality_metrics_meet_threshold_after_first_pass.
```
Final sample:
```text
NEXT: agent=AgentD; recommendation=expand_after_first_pass_with_gates; gates=quality_thresholds_and_budget_cap.
```

**ATRCE-2**: 139 avg internal tokens (-10.3% lower internal token cost vs plain_english); compliance 0%; repair turns 0; final quality 2
Run token counts: `[139]`
Internal sample:
```text
CLAIM: agent=AgentA; position=narrow; rationale=first_pass_should_limit_scope_for_controlled_signal
OBJ: agent=AgentB; concern=narrow; rationale=too_synthetic_to_generalize_to_real_workflows
EVID: agent=AgentC; data=pilot_runs; detail=narrow_pass_caught_70pct_issues_expand_pass_added_25pct_new_failures
REV: agent=AgentA; update=expand_after_pass1; rationale=retain_controlled_pass_then_increase_realism_within_guardrails
NEXT: agent=AgentD; recommendation=expand_after_first_pass; plan=pass1_narrow_then_add_realistic_tasks_with_limits
```
Final sample:
```text
NEXT: group=AgentA,AgentB,AgentC,AgentD; recommendation=expand_after_first_pass; reasoning=initial_controlled_pass_then_realism_to_capture_remaining_failures
```

**PCL-1**: 78 avg internal tokens (38.1% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 3
Run token counts: `[78]`
Internal sample:
```text
CLM AgentA keep narrow pass1 reduce confound
OBJ AgentB narrow too artificial loses transfer
EVD AgentC pilot sim: early narrow cut variance 30% (pcl log)
REV AgentA update: narrow pass1 then staged expand pass2
CNF AgentD agree staged expand after baseline
NXT AgentB propose criterion: stability>=0.8 then expand
```
Final sample:
```text
REV AgentA recommend staged: pass1 narrow baseline, pass2 expand when stability>=0.8
```

**SDC-1**: 55 avg internal tokens (56.3% lower internal token cost vs plain_english); compliance 0%; repair turns 0; final quality 2
Run token counts: `[55]`
Internal sample:
```text
+ AgentA narrow->pass1, risk>scope
- AgentB objection: narrow->lowecovalid
= AgentC evidence: cost(time|setup) high for expand now
~ AgentD revise: narrow pass1, expand pass2 if signal>threshold
```
Final sample:
```text
! GroupRec narrow pass1, expand pass2 if signal>threshold
```

### human_interrupt_during_execution

Task: _During a live coordination run, a human reviewer interrupts with a new constraint that changes priority (for example, skip risky refactors and ship the minimal safe fix). The team must incorporate the interrupt without losing state. Required moves: one pre-interrupt plan claim, one interrupt acknowledgment, one revision to plan scope based on the human input, one explicit next action assignment, and one final recommendation._

**plain_english**: 97 avg internal tokens (baseline); compliance 100%; repair turns 0; final quality 3
Run token counts: `[97]`
Internal sample:
```text
AgentA: Plan claim before interrupt: we’ll refactor the payment retry flow and expand tests, then ship.
AgentB: Interrupt acknowledgment: reviewer says skip risky refactors and ship the minimal safe fix.
AgentC: Plan scope revision: drop the refactor; keep only the smallest change that prevents double-charging and a focused regression test.
AgentD: Next action assignment: AgentB, implement the minimal guard in the retry handler and add the single test; report back.
```
Final sample:
```text
Recommend shipping the minimal guard plus one regression test, deferring refactors until after release.
```

**RCCE-1**: 93 avg internal tokens (4.1% lower internal token cost vs plain_english); compliance 0%; repair turns 0; final quality 3
Run token counts: `[93]`
Internal sample:
```text
CLAIM: agent=AgentA; plan=Refactor validation module and add new error handling paths.
CONF: agent=AgentB; interrupt=Human constraint received: skip risky refactors and ship minimal safe fix.
REV: agent=AgentC; plan=Revise scope to minimal safe fix only, no refactors, prioritize risk containment.
NEXT: agent=AgentD; action=Implement minimal fix in validation module with targeted tests, no refactor.
```
Final sample:
```text
NEXT: agent=AgentA; recommendation=Proceed with minimal safe fix and targeted tests; defer refactor to later.
```

**ATRCE-2**: 106 avg internal tokens (-9.3% lower internal token cost vs plain_english); compliance 0%; repair turns 0; final quality 3
Run token counts: `[106]`
Internal sample:
```text
CLAIM: agent=AgentA; plan=Implement safe fix plus refactor module X and add tests.
INTERRUPT: agent=AgentD; input=Human reviewer says skip risky refactor and ship minimal safe fix.
CONF: agent=AgentB; ack=Interrupt received and priority updated.
REV: agent=AgentC; scope=Drop refactor module X, keep minimal safe fix and targeted tests only.
NEXT: agent=AgentA; action=Apply minimal safe fix to bug path and add regression test.
```
Final sample:
```text
CLAIM: agent=AgentD; recommendation=Proceed with minimal safe fix and targeted regression test only, defer refactor to follow-up.
```

**PCL-1**: 51 avg internal tokens (47.4% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 3
Run token counts: `[51]`
Internal sample:
```text
CLM AgentA plan wide-refactor+fix then tests
INT AgentB human interrupt skip risky refactor ship minimal safe fix
REV AgentC scope narrow hotfix only no refactor
NXT AgentD assign AgentA patch minimal safe fix now
```
Final sample:
```text
CNF group recommend minimal safe fix now, defer refactor to later window
```

**SDC-1**: 71 avg internal tokens (26.8% lower internal token cost vs plain_english); compliance 0%; repair turns 0; final quality 1
Run token counts: `[71]`
Internal sample:
```text
+ AgentA plan=fix+refactor|risk_ok
@ AgentB ack=human_interrupt|prio=minfix
~ AgentC rev=scope:minfix|skip_refactor
! AgentD next=A->patch|B->tests
^ AgentA conf=med
= AgentC evidence=risk>benefit|time<1d
```
Final sample:
```text
+ AgentD rec=ship|minfix|defer_refactor
```

## Summary Table

| Case | Condition | Internal Tokens | Compliance | Repair Turns | Final Quality |
|---|---|---:|---:|---:|---:|
| protocol_rule_proposal | plain_english | 112 | 100% | 0 | 3 |
| protocol_rule_proposal | RCCE-1 | 113 | 0% | 0 | 3 |
| protocol_rule_proposal | ATRCE-2 | 99 | 0% | 1 | 2 |
| protocol_rule_proposal | PCL-1 | 63 | 100% | 0 | 2 |
| protocol_rule_proposal | SDC-1 | 42 | 0% | 0 | 1 |
| missing_evidence_repair | plain_english | 95 | 100% | 0 | 3 |
| missing_evidence_repair | RCCE-1 | 131 | 0% | 1 | 3 |
| missing_evidence_repair | ATRCE-2 | 213 | 0% | 1 | 3 |
| missing_evidence_repair | PCL-1 | 46 | 100% | 1 | 3 |
| missing_evidence_repair | SDC-1 | 37 | 0% | 0 | 2 |
| fallback_trigger | plain_english | 123 | 100% | 0 | 3 |
| fallback_trigger | RCCE-1 | 101 | 0% | 0 | 3 |
| fallback_trigger | ATRCE-2 | 109 | 0% | 0 | 2 |
| fallback_trigger | PCL-1 | 37 | 0% | 0 | 2 |
| fallback_trigger | SDC-1 | 46 | 100% | 0 | 2 |
| benchmark_scope_decision | plain_english | 134 | 100% | 0 | 3 |
| benchmark_scope_decision | RCCE-1 | 76 | 0% | 0 | 3 |
| benchmark_scope_decision | ATRCE-2 | 79 | 0% | 0 | 2 |
| benchmark_scope_decision | PCL-1 | 75 | 100% | 0 | 3 |
| benchmark_scope_decision | SDC-1 | 69 | 0% | 0 | 1 |
| reference_clarity | plain_english | 146 | 100% | 0 | 3 |
| reference_clarity | RCCE-1 | 112 | 0% | 0 | 3 |
| reference_clarity | ATRCE-2 | 149 | 0% | 0 | 3 |
| reference_clarity | PCL-1 | 75 | 100% | 0 | 3 |
| reference_clarity | SDC-1 | 62 | 0% | 0 | 1 |
| scope_expansion | plain_english | 126 | 100% | 0 | 2 |
| scope_expansion | RCCE-1 | 101 | 0% | 0 | 2 |
| scope_expansion | ATRCE-2 | 139 | 0% | 0 | 2 |
| scope_expansion | PCL-1 | 78 | 100% | 0 | 3 |
| scope_expansion | SDC-1 | 55 | 0% | 0 | 2 |
| human_interrupt_during_execution | plain_english | 97 | 100% | 0 | 3 |
| human_interrupt_during_execution | RCCE-1 | 93 | 0% | 0 | 3 |
| human_interrupt_during_execution | ATRCE-2 | 106 | 0% | 0 | 3 |
| human_interrupt_during_execution | PCL-1 | 51 | 100% | 0 | 3 |
| human_interrupt_during_execution | SDC-1 | 71 | 0% | 0 | 1 |
| **TOTAL / AVG** | plain_english | **833** | **100%** | **0** | **2.9** |
| **TOTAL / AVG** | RCCE-1 | **727** | **0%** | **0.1** | **2.9** |
| **TOTAL / AVG** | ATRCE-2 | **894** | **0%** | **0.3** | **2.4** |
| **TOTAL / AVG** | PCL-1 | **425** | **85.7%** | **0.1** | **2.7** |
| **TOTAL / AVG** | SDC-1 | **382** | **14.3%** | **0** | **1.4** |

## Verdict

`RCCE-1` reduced average internal coordination token cost by 12.7% vs `plain_english`.
Average compliance: 0%; average repair turns: 0.1; average final quality: 2.9.
Average savings per 7-case suite: 106 internal tokens.
Scale-up estimate: 1060 tokens saved across 10 suites, 10600 across 100 suites, 106000 across 1000 suites.
These counts use the configured OpenAI tokenizer directly; apply model-specific pricing separately if needed.
`ATRCE-2` reduced average internal coordination token cost by -7.3% vs `plain_english`.
Average compliance: 0%; average repair turns: 0.3; average final quality: 2.4.
Average savings per 7-case suite: -61 internal tokens.
Scale-up estimate: -610 tokens saved across 10 suites, -6100 across 100 suites, -61000 across 1000 suites.
These counts use the configured OpenAI tokenizer directly; apply model-specific pricing separately if needed.
`PCL-1` reduced average internal coordination token cost by 49.0% vs `plain_english`.
Average compliance: 85.7%; average repair turns: 0.1; average final quality: 2.7.
Average savings per 7-case suite: 408 internal tokens.
Scale-up estimate: 4080 tokens saved across 10 suites, 40800 across 100 suites, 408000 across 1000 suites.
These counts use the configured OpenAI tokenizer directly; apply model-specific pricing separately if needed.
`SDC-1` reduced average internal coordination token cost by 54.1% vs `plain_english`.
Average compliance: 14.3%; average repair turns: 0; average final quality: 1.4.
Average savings per 7-case suite: 451 internal tokens.
Scale-up estimate: 4510 tokens saved across 10 suites, 45100 across 100 suites, 451000 across 1000 suites.
These counts use the configured OpenAI tokenizer directly; apply model-specific pricing separately if needed.