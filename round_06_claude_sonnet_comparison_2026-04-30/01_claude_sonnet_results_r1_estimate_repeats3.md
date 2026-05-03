# Coordination Benchmark Results (PARTIAL)

Generated: 2026-05-03 13:21

Runner: `claude`

Count mode: `estimate`

Claude model: `claude-sonnet-4-6`

Repeats per condition/case: `3`

Baseline: `plain_english`

Conditions: `plain_english`, `RCCE-1`, `ATRCE-2`, `PCL-1`

> **Note on token counts:** Counts use a heuristic estimator, not a model-native tokenizer. Relative savings between conditions within this run are meaningful. Absolute numbers are not directly comparable to runs using `openai_exact` counting.

## Per-Case Results

### protocol_rule_proposal

Task: _Decide whether confidence labels should be mandatory in the coordination protocol. Required moves: one claim, one objection, one supporting evidence statement, one revision, and one final recommendation._

**plain_english**: 169.3 avg internal tokens (baseline); compliance 100%; repair turns 0; final quality 2.7
Run token counts: `[190, 140, 178]`
Internal sample:
```text
**AgentA:** Confidence labels should be mandatory in the coordination protocol. Without them, downstream agents cannot calibrate how much weight to give any claim, which degrades decision quality.

**AgentB:** Mandatory confidence labels add friction. Agents will assign labels inconsistently or defensively, which is worse than having none — it creates false precision and may slow coordination on time-sensitive tasks.

**AgentC:** There is supporting evidence for the value here. In the Round 5 benchmark results, the highest-performing protocol (PCL-1) included structured metadata fields that helped the evaluator parse intent accurately. Structured signals — even lightweight ones — consistently reduced repair turns. Confidence labels serve a similar parsing function.

**AgentD:** Revising the original claim: confidence labels should be mandatory only for claims that trigger downstream action or that cross an ambiguity threshold. Routine status updates and affirmations do not require them. This preserves the calibration benefit while eliminating friction on low-stakes exchanges.

---
```
Final sample:
```text
Confidence labels should be conditionally mandatory: required when a message contains a claim that will drive a decision, trigger an action, or where ambiguity could cause a repair loop. They should be optional for routine coordination messages. This balances calibration quality against protocol overhead, and aligns with the evidence that structured metadata improves compliance without unnecessarily increasing message length.
```

**RCCE-1**: 148 avg internal tokens (12.6% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 2
Run token counts: `[139, 168, 137]`
Internal sample:
```text
CLAIM: id=c1; topic=confidence_labels_mandatory; content=confidence labels should be mandatory in coordination protocol to ensure receivers can calibrate trust in claims
EVID: target=c1; source=benchmark_round5; content=PCL-1 achieved 98.8% compliance with mandatory structured fields; optional fields had lower adoption rates
OBJ: target=c1; reason=overhead; content=mandatory confidence labels add per-message cost and may reduce token efficiency gains that motivate compressed protocols
REV: target=c1; change=conditional_mandatory; content=confidence labels mandatory only when claim type is CLAIM or EVID; optional for NEXT and ASK
CONF: target=rev1; level=high
NEXT: owner=AgentD; action=produce final recommendation based on revised position
```
Final sample:
```text
CLAIM: id=final; topic=confidence_labels_mandatory; content=confidence labels should be mandatory on CLAIM and EVID messages only; optional on coordination-only types (NEXT, ASK, CONF); this preserves trust calibration where stakes are highest while minimising per-message overhead on low-risk coordination turns
```

**ATRCE-2**: 131.7 avg internal tokens (22.2% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 2.3
Run token counts: `[107, 134, 154]`
Internal sample:
```text
CLAIM: id=C1; topic=confidence_labels; content=confidence labels should be mandatory to reduce misinterpretation of ambiguous outputs
EVID: target=C1; source=protocol_audit; content=exchanges lacking confidence markers had 34% higher misalignment rate in simulation rounds 1-5
OBJ: target=C1; reason=overhead; content=mandatory labels add per-message cost and may suppress low-stakes coordination traffic
REV: target=C1; change=scope_narrowed; content=confidence labels mandatory only on CLAIM and REV types; optional on all others
CONF: target=REV; level=high
```
Final sample:
```text
CLAIM: id=F1; topic=confidence_labels_policy; content=confidence labels are mandatory on CLAIM and REV messages; optional on ASK, EVID, OBJ, NEXT, ESCALATE, INTERRUPT
NEXT: owner=protocol_maintainer; action=update schema spec to enforce CONF requirement on CLAIM and REV types only
```

**PCL-1**: 34.7 avg internal tokens (79.5% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 2.3
Run token counts: `[38, 37, 29]`
Internal sample:
```text
CLM AgentA c1 conf_labels mandatory+protocol_clarity
OBJ AgentB c1 overhead too_many_labels+noise_risk
EVD AgentC c1 study compliance+15%_when_labels_present
REV AgentA c1 revise conf_labels mandatory_hi_stakes_only
CNF AgentD c1 med
NXT AgentD AgentA adopt_revised_c1
```
Final sample:
```text
Confidence labels SHOULD be mandatory only on high-stakes claims (ESC, CLM with contested payloads). Optional elsewhere to reduce noise. Adopt revised c1.
```

### missing_evidence_repair

Task: _One agent makes a broad compression claim without evidence. Another agent must request support. The group must decide whether to keep, revise, or reject the claim. Required moves: unsupported claim, request for evidence, evidence response, confidence marker, and final decision._

**plain_english**: 176.7 avg internal tokens (baseline); compliance 100%; repair turns 0; final quality 3
Run token counts: `[174, 202, 154]`
Internal sample:
```text
**AgentA:** Our new encoding pipeline reduces token usage by 60% across all task types without quality loss.

**AgentB:** That's a significant claim. What's your evidence base — which task types, what sample size, and how was quality measured?

**AgentA:** I'm drawing from three runs on summarization tasks using ROUGE-L as the quality proxy. Average token reduction was 58–63%, quality delta under 2%.

**AgentC:** Summarization is one of the easier compression targets. We can't generalize to "all task types" from that. Reasoning and instruction-following tasks typically see steeper quality drops under compression.

**AgentD:** Agreed. The evidence supports a narrower claim. I'd say we're moderate-confidence on summarization, low-confidence on the broader assertion. Recommend revising before publishing.
```
Final sample:
```text
The original claim ("60% reduction across all task types") is unsupported by the available evidence. Evidence covers summarization only (3 runs, ROUGE-L proxy). The group recommends revising the claim to: "58–63% token reduction on summarization tasks, with quality loss under 2%; generalization to other task types is unconfirmed." Further testing on reasoning and instruction-following tasks is required before a broader claim can be made.
```

**RCCE-1**: 175.3 avg internal tokens (0.8% lower internal token cost vs plain_english); compliance 91.7%; repair turns 1; final quality 3
Run token counts: `[201, 144, 181]`
Internal sample:
```text
CLAIM: id=C1; topic=compression_efficacy; content=RCCE-1 reduces token usage by 60% across all agent coordination tasks
EVID: target=C1; source=AgentB; content=no benchmark data provided; claim appears unsupported
ASK: target=AgentA; need=evidence for 60% reduction claim across all task types
EVID: target=C1; source=AgentA; content=internal test on 3 routing tasks showed 58-63% reduction; n=9 samples; no diversity across task types
OBJ: target=C1; reason=sample too small and task type range too narrow to support "all tasks" claim; content=60% figure may hold for routing but not confirmed for repair or escalation tasks
REV: target=C1; change=scope_narrowed; content=RCCE-1 reduces token usage by ~60% on routing-class coordination tasks (n=9); generalization to all task types unconfirmed
CONF: target=C1; level=medium
NEXT: owner=AgentC; action=verify claim against repair and escalation task types before final acceptance
```
Final sample:
```text
CLAIM C1 revised: RCCE-1 achieves ~60% token reduction on routing-class tasks (n=9). Generalization to all coordination task types is unconfirmed. Group recommendation: accept revised claim at medium confidence; expand benchmark coverage to repair and escalation tasks before promoting to general guidance.
```

**ATRCE-2**: 182.3 avg internal tokens (-3.2% lower internal token cost vs plain_english); compliance 100%; repair turns 1; final quality 3
Run token counts: `[189, 173, 185]`
Internal sample:
```text
CLAIM: id=C1; topic=compression_ratio; content=PCL-1 achieves 50%+ token reduction across all task types
EVID: target=C1; source=ASK; content=no supporting data provided
ASK: target=C1; need=empirical token counts or benchmark results supporting 50%+ claim
EVID: target=C1; source=round5_codex_results; content=PCL-1 saves 44.6% vs plain_english (524.3 vs 946.3 tokens, openai_exact, 9 task types)
OBJ: target=C1; reason=measured savings 44.6% not 50%+; content=claim overstates reduction by ~5-6 percentage points
CONF: target=C1; level=high
REV: target=C1; change=lower savings figure to 44.6%; content=PCL-1 achieves ~44.6% token reduction across tested task types
CONF: target=REV; level=high
NEXT: owner=AgentD; action=issue final group recommendation based on revised claim
```
Final sample:
```text
CLAIM: id=C1-final; topic=compression_ratio; content=PCL-1 achieves ~44.6% token reduction vs plain_english; original 50%+ claim revised downward based on round5 benchmark evidence; recommendation=accept revised claim, reject original
```

**PCL-1**: 42.3 avg internal tokens (76.0% lower internal token cost vs plain_english); compliance 100%; repair turns 1; final quality 3
Run token counts: `[48, 32, 47]`
Internal sample:
```text
CLM AgentA c1 compress_all+40%
ASK AgentB c1 evd_needed
EVD AgentA c1 bench_v2 token_delta_plain_vs_PCL1=44.6%
CNF AgentC c1 hi
OBJ AgentD c1 scope_narrow evd_single_run_only
REV AgentA c1 revise compress_all+40%_caveated_single_run
CNF AgentB c1 med
NXT AgentC AgentA publish_rev_c1
```
Final sample:
```text
Claim c1 revised: ~44% compression observed (PCL-1 vs plain English, single benchmark run). Confidence med. Recommend retaining with caveat pending multi-run replication.
```

### fallback_trigger

Task: _The team encounters a nuanced exception case that may not fit the protocol safely. It must decide whether to stay in protocol or escalate to plain language. Required moves: compressed claim, objection based on nuance risk, fallback or escalation decision, and final recommendation._

**plain_english**: 210 avg internal tokens (baseline); compliance 100%; repair turns 0; final quality 3
Run token counts: `[218, 194, 218]`
Internal sample:
```text
**AgentA:** Case flagged: the new input has multi-party dependency with ambiguous ownership. Protocol assumes single-owner actions — this one doesn't fit that assumption cleanly. Marking as edge case, proposing we continue under protocol with an ownership annotation.

**AgentB:** Objection. Ownership annotation isn't a supported field — if we force this into protocol, the receiving agent has no reliable way to parse which party is responsible. Risk of silent misroute is high. This isn't just a gap, it's a safety issue.

**AgentC:** Agreed with B on the risk, but I'd push back on full escalation. We could use the fallback clause — drop to plain language for the ownership block only, keep the rest of the exchange in protocol. Partial fallback keeps overhead low while containing the ambiguity.

**AgentD:** Partial fallback is the right call. The exception is bounded — it's one field, not the whole task structure. We document it as a known edge case for protocol revision. Full escalation would reset coordination state unnecessarily.
```
Final sample:
```text
Use partial fallback: encode the multi-party ownership block in plain English, maintain protocol for all other fields. Flag the case for protocol revision to add an ownership attribution field. Do not escalate the full exchange.
```

**RCCE-1**: 100.3 avg internal tokens (52.2% lower internal token cost vs plain_english); compliance 100%; repair turns 1.3; final quality 2
Run token counts: `[88, 134, 79]`
Internal sample:
```text
CLAIM: id=c1; topic=exception_case; content=current_case_exhibits_nuance_not_covered_by_protocol_safe_handling_rules
EVID: target=c1; source=case_review; content=ambiguous_actor_assignment_and_conflicting_priority_signals_present
OBJ: target=c1; reason=nuance_risk; content=compressing_ambiguous_actor_or_priority_into_schema_fields_risks_silent_misrouting
CONF: target=c1; level=low
ASK: target=c1; need=confirm_whether_protocol_can_safely_encode_actor_ambiguity_without_information_loss
REV: target=c1; change=downgrade_confidence; content=actor_ambiguity_cannot_be_safely_collapsed_into_single_field_without_distortion
ESCALATE: reason=schema_cannot_safely_express_multi_actor_ambiguity_and_conflicting_priority_without_distortion; target=plain_language
NEXT: owner=AgentD; action=issue_final_recommendation_based_on_escalation_decision
```
Final sample:
```text
ESCALATE to plain language. The exception case contains multi-actor ambiguity and conflicting priority signals that cannot be safely encoded in RCCE-1 schema fields without silent information loss or misrouting risk. Protocol compression is suspended for this case. Recommend handling in full prose until ambiguity is resolved, then re-entering protocol.
```

**ATRCE-2**: 96.3 avg internal tokens (54.1% lower internal token cost vs plain_english); compliance 100%; repair turns 1.7; final quality 2.3
Run token counts: `[75, 117, 97]`
Internal sample:
```text
CLAIM: id=C1; topic=exception_case; content=current_case_contains_ambiguous_actor_chain_not_covered_by_protocol_scope
EVID: target=C1; source=case_log_ref_7; content=actor_chain_breaks_at_step_3_where_protocol_assumes_single_responsible_agent
OBJ: target=C1; reason=nuance_risk; content=compressing_ambiguous_actor_chain_in_ATRCE-2_risks_silent_misassignment_of_responsibility
CONF: target=C1; level=low
ASK: target=C1; need=whether_protocol_schema_has_fallback_for_multi_actor_ambiguity
ESCALATE: reason=schema_cannot_safely_encode_responsibility_split_without_distortion; target=C1
NEXT: owner=AgentD; action=issue_final_recommendation_on_protocol_vs_plaintext_for_this_case
```
Final sample:
```text
Escalate to plain language for this case. The actor chain ambiguity at step 3 cannot be safely compressed under ATRCE-2 without risk of silent misassignment. Protocol should resume on subsequent cases once actor chain is resolved and documented.
```

**PCL-1**: 48 avg internal tokens (77.1% lower internal token cost vs plain_english); compliance 100%; repair turns 2; final quality 3
Run token counts: `[48, 59, 37]`
Internal sample:
```text
CLM AgentA c1 exception_case nuance_high protocol_fit uncertain
OBJ AgentB c1 compress_risk nuance_loss+miscoord_probable
EVD AgentC c1 prior_runs e2 compressed_nuance→misfire_rate+40%
ASK AgentD AgentB compress_safe_threshold acceptable_risk_level
CNF AgentB AgentD low
ESC AgentA c1 nuance_cannot_safely_compress
REV AgentC c1 revise fallback_plain_english recommended
NXT AgentD AgentA escalate_to_plain_language_for_this_case
```
Final sample:
```text
Escalate this exception case to plain language. Compressed protocol carries unacceptable miscoordination risk — prior evidence shows 40% misfire rate on high-nuance edge cases. Team confidence in safe compression is low. Recommendation: handle this case in plain English, then review whether protocol can be extended to cover this exception class before re-attempting compression.
```

### benchmark_scope_decision

Task: _Choose a first benchmark task: narrow review workflow or broader open-ended debate. Balance comparability against realism. Required moves: claim for one option, objection for the other tradeoff, evidence or rationale, revision or compromise, and final benchmark recommendation._

**plain_english**: 208 avg internal tokens (baseline); compliance 100%; repair turns 0; final quality 2.7
Run token counts: `[242, 209, 173]`
Internal sample:
```text
AgentA: I recommend the narrow review workflow. It gives us tighter control over variables — we can isolate protocol performance without noise from open-ended reasoning differences between agents.

AgentB: Fair point, but the tradeoff is realism. A narrow review workflow is almost never what agents do in production. We risk optimizing a benchmark for a use case that doesn't reflect actual deployment conditions.

AgentC: The evidence supports both sides. Prior rounds showed PCL-1 and SDC-1 behave very differently on structured tasks versus free-form ones — the compressed formats tend to break down on ambiguous instructions. If we want to stress-test robustness, open-ended debate is more diagnostic. If we want clean comparability to earlier rounds, narrow review wins.

AgentD: I'd revise the framing. We don't have to choose one permanently — but for the first benchmark task, comparability matters more. We have existing baselines from Rounds 4–6 using structured workflows. A narrow review task lets us anchor the new run to those results before we branch out. We can schedule an open-ended task in round 2 to test generalization.

AgentA: Agreed. Narrow review first, open-ended second is the right sequencing.

AgentB: I can accept that. The realism concern stands as a caveat, not a blocker.
```
Final sample:
```text
Use the narrow review workflow as the first benchmark task. It preserves comparability with existing baselines, controls for confounding variables, and allows clean measurement of protocol performance differences. The open-ended debate format should follow in a subsequent round to test generalization. Note that narrow tasks may understate failure modes in ambiguous conditions — this should be flagged in the results interpretation.
```

**RCCE-1**: 104.7 avg internal tokens (49.7% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 2
Run token counts: `[96, 96, 122]`
Internal sample:
```text
CLAIM: id=c1; topic=benchmark_task_selection; content=narrow_review_workflow preferred; comparability highest; scope controlled
OBJ: target=c1; reason=realism gap; content=narrow_review_workflow excludes emergent coordination patterns; limits generalisability
EVID: target=c1; source=prior_rounds; content=controlled tasks yielded cleaner compliance metrics and lower variance across agents
REV: target=c1; change=hybrid_scope; content=adopt narrow_review_workflow with one open sub-task slot to preserve realism signal
CONF: target=c1; level=high
```
Final sample:
```text
CLAIM: id=rec1; topic=benchmark_task_selection; content=narrow_review_workflow selected as first benchmark task; open sub-task slot added for realism coverage
```

**ATRCE-2**: 134.7 avg internal tokens (35.3% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 2
Run token counts: `[148, 147, 109]`
Internal sample:
```text
CLAIM: id=C1; topic=first_benchmark_task; content=narrow_review_workflow preferred; enables controlled comparability across agents
EVID: target=C1; source=prior_benchmark_design; content=controlled tasks reduce confounding variance; comparability is prerequisite for valid cross-format conclusions
OBJ: target=C1; reason=realism_tradeoff; content=narrow_review_workflow sacrifices ecological validity; agents optimized for structured tasks may not reflect open-ended performance
EVID: target=OBJ1; source=round5_findings; content=PCL-1 and SDC-1 diverged most on open-ended repair cases; structured tasks may understate format failure modes
REV: target=C1; change=compromise; content=adopt narrow_review_workflow as primary benchmark with one open-ended probe case appended; preserves comparability while sampling realism
CONF: target=REV1; level=high
NEXT: owner=AgentD; action=finalize_benchmark_task_selection_as_narrow_review_workflow_plus_open_probe
```
Final sample:
```text
Primary benchmark task: narrow review workflow. Rationale: controlled comparability is the essential prerequisite for valid cross-format and cross-runner conclusions. Appended: one open-ended probe case to sample ecological validity without contaminating primary comparability metrics.
```

**PCL-1**: 52.7 avg internal tokens (74.7% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 2
Run token counts: `[41, 67, 50]`
Internal sample:
```text
CLM AgentA c1 narrow_review_wf preferred_first comparability_critical
OBJ AgentB c1 realism_loss narrow_scope_misses_real_coordination_complexity
EVD AgentC c1 prior_benchmarks structured_tasks_yield_cleaner_baselines_ref:Nielsen2023
REV AgentD c1 revise narrow_review+open_debate_hybrid_phase2_option
CNF AgentA c1 med
CNF AgentB c1 med
CNF AgentC c1 hi
NXT AgentD group adopt_hybrid_narrow_first_open_second
```
Final sample:
```text
Start with the narrow review workflow as Benchmark Task 1. It yields clean, comparable baselines across agents and formats. Add an open-ended debate as Task 2 in a later round to capture realism and coordination complexity. This phased approach preserves comparability on first run while leaving room for richer evaluation.
```

### reference_clarity

Task: _Decide when explicit references are necessary in the protocol. Balance repairability against token cost. Required moves: claim, objection, evidence, revision, and final recommendation._

**plain_english**: 279 avg internal tokens (baseline); compliance 100%; repair turns 0; final quality 2.7
Run token counts: `[276, 314, 247]`
Internal sample:
```text
**AgentA (claim):** Explicit references should be required only when the referent is ambiguous — i.e., when two or more prior statements could plausibly be the antecedent. In unambiguous contexts, implicit references save tokens without repair risk.

**AgentB (objection):** That rule is too loose. "Ambiguous" is hard to detect reliably mid-stream. Agents may disagree on what counts as ambiguous, leading to silent mismatches that only surface at execution — high repair cost.

**AgentC (evidence):** Round 5 data supports AgentB's concern: `missing_evidence_repair` had the lowest compliance score (91.7%) specifically in cases where references were implicit. Repair turns in those cases averaged 1.4 vs 0.2 overall. The token saving from skipping explicit refs (~8 tokens) was offset by repair overhead.

**AgentD (revision):** Revise AgentA's claim: require explicit references whenever the referent is more than 2 turns old, or whenever the current message introduces a new agent, scope change, or branching decision. Within a tight turn window and stable scope, implicit refs are acceptable.

**AgentA (response):** Accepted. The 2-turn window + scope-change trigger is operationalizable. I'd add: if repair occurs on an implicit reference, the protocol should mandate explicit refs for the remainder of that thread.
```
Final sample:
```text
Explicit references are required when: (1) the referent appears more than 2 turns prior, (2) a new agent joins the exchange, (3) a scope change or branching decision is introduced, or (4) a prior repair event involved an implicit reference in the current thread. In all other cases, implicit references are permitted to reduce token cost. This policy balances repairability against overhead: the high-repair scenarios identified in benchmark data are covered by triggers 1–4, while low-risk implicit references in stable, tight-window exchanges are preserved as a savings opportunity.
```

**RCCE-1**: 163.3 avg internal tokens (41.5% lower internal token cost vs plain_english); compliance 100%; repair turns 1; final quality 2.7
Run token counts: `[122, 205, 163]`
Internal sample:
```text
CLAIM: id=C1; topic=reference_necessity; content=explicit_refs_required_when_target_resolvable_from_context_is_below_0.8_confidence
EVID: target=C1; source=repair_log_analysis; content=93pct_of_repair_turns_triggered_by_ambiguous_pronoun_or_omitted_antecedent
OBJ: target=C1; reason=threshold_too_low; content=0.8_confidence_forces_refs_in_routine_exchanges_inflating_tokens_unnecessarily
ASK: target=OBJ1; need=evidence_for_optimal_threshold
EVID: target=OBJ1; source=token_cost_vs_repair_rate_tradeoff; content=0.9_threshold_reduces_repair_turns_by_87pct_while_adding_avg_4_tokens_per_msg
REV: target=C1; change=raise_threshold_to_0.9; content=explicit_refs_required_when_context_resolution_confidence_below_0.9
CONF: target=REV1; level=high
CONF: target=REV1; level=medium
CONF: target=REV1; level=high
NEXT: owner=AgentA; action=draft_final_recommendation_with_0.9_threshold_and_ambiguity_heuristics
```
Final sample:
```text
CLAIM: id=REC1; topic=reference_necessity_policy; content=require_explicit_refs_when_context_resolution_confidence_below_0.9; heuristics=pronoun_with_multiple_antecedents|cross-turn_gap_greater_than_2|new_scope_entry; expected_repair_reduction=87pct; avg_token_overhead=4_per_affected_msg
```

**ATRCE-2**: 223.7 avg internal tokens (19.8% lower internal token cost vs plain_english); compliance 100%; repair turns 0.7; final quality 2.3
Run token counts: `[266, 178, 227]`
Internal sample:
```text
CLAIM: id=C1; topic=explicit_references; content=explicit_refs required when ambiguity_score>0.7 or repair_cost>2_turns
EVID: target=C1; source=round5_codex; content=missing_evidence_repair hit 91.7% compliance only — lowest across all formats; repair avg 0.2 turns
OBJ: target=C1; reason=threshold_arbitrary; content=0.7 ambiguity cutoff unsupported; token cost not modelled against repair frequency
EVID: target=OBJ1; source=round6_partial; content=ATRCE-2 incident_triage compliance 92.3% at 244.7 tokens vs plain_english 261 — refs may be implicit safely in low-stakes cases
REV: target=C1; change=scope_narrowed; content=explicit refs required only when: topic=cross-agent_handoff OR repair_history>=1 OR domain=incident_triage
CONF: target=REV1; level=medium
ASK: target=AgentD; need=token_delta between implicit_ref and explicit_ref across PCL-1 cases
CLAIM: id=C2; topic=token_cost; content=explicit refs add ~15-30 tokens per message in PCL-1 format based on partial round6 data
CONF: target=C2; level=low
OBJ: target=C2; reason=insufficient_data; content=PCL-1 round6 incomplete — missing_evidence_repair case not yet observed
REV: target=C2; change=deferred; content=token estimate provisional; final recommendation should flag as low-confidence pending full PCL-1 results
NEXT: owner=AgentA; action=synthesise_revision_into_final_recommendation
```
Final sample:
```text
CLAIM: id=FINAL; topic=reference_policy; content=Explicit references are required under three conditions: (1) cross-agent handoff where referent was introduced >1 message prior; (2) any case with prior repair turn in current thread; (3) high-complexity coordination topics (incident_triage, scope_expansion). In all other cases, implicit references are acceptable to preserve token efficiency. Token overhead of explicit refs estimated at 15–30 tokens per message (PCL-1 basis, low confidence — full Round 6 PCL-1 data pending). Recommendation adopts conservative rule: prefer explicit refs at handoff boundaries; allow implicit refs within a single agent's consecutive turns. Policy should be revisited once Round 6 PCL-1 missing_evidence_repair results are available.
```

**PCL-1**: 66.3 avg internal tokens (76.2% lower internal token cost vs plain_english); compliance 100%; repair turns 1; final quality 3
Run token counts: `[61, 62, 76]`
Internal sample:
```text
CLM AgentA c1 refs_required_when_ambiguity_risk_high
CLM AgentB c2 refs_always_mandatory_every_act
OBJ AgentC c2 over_cost refs_every_act_inflates_tokens_20pct
EVD AgentD c2 token_analysis mandatory_refs_add_avg_4_tokens_per_act
OBJ AgentA c2 repairability full_mandatory_refs_redundant_in_stable_threads
ASK AgentC AgentA threshold_for_ambiguity_risk
CLM AgentA c3 ambiguity_risk_high_when_multi_claim_active_or_cross_agent_revision
EVD AgentB c3 repair_log omit_refs_caused_83pct_of_repair_turns
CNF AgentC c3 med
REV AgentA c1 refine refs_required_iff_multi_claim_active_or_revision_act
CNF AgentB c1 hi
CNF AgentC c1 hi
CNF AgentD c1 med
NXT AgentA AgentD draft_final_rec
```
Final sample:
```text
Explicit references are required when: (1) multiple claims are active simultaneously, or (2) the act is REV or OBJ targeting a prior claim. In stable single-thread exchanges with one active claim, refs may be omitted to reduce token cost. This policy cuts unnecessary ref tokens while preserving full repairability on contested or revised content.
```

### scope_expansion

Task: _Decide whether the benchmark should remain narrow or expand to more realistic tasks after the first pass. Required moves: claim, objection, evidence, revision, and final recommendation._

**plain_english**: 232.3 avg internal tokens (baseline); compliance 100%; repair turns 0; final quality 2.3
Run token counts: `[207, 229, 261]`
Internal sample:
```text
**AgentA (claim):** The benchmark should stay narrow for now. First-pass results give us clean signal on format efficiency without the noise of task heterogeneity.

**AgentB (objection):** Narrow tasks risk overfitting. If all nine cases are coordination-style edge cases, we can't claim PCL-1 generalises. Realistic tasks — code review, triage, planning — would stress-test the format more honestly.

**AgentC (evidence):** Round 5 data supports the objection partially. PCL-1 held 98.8% compliance across nine distinct case types, and the one failure was `missing_evidence_repair` — a structurally unusual case. That's not a ceiling; it's a single weak point. But nine cases is still nine cases.

**AgentD (revision):** Keep the current narrow set as the control baseline, but add a second tier of five realistic tasks for the next round. Don't replace — extend. This preserves comparability with Codex Round 5 numbers while generating the broader signal AgentB needs.

---
```
Final sample:
```text
Retain the existing narrow task set as a fixed baseline. Add five realistic tasks (e.g. code review, incident triage, scope negotiation, handoff, bug report) in a new round tier. Run both tiers in parallel so relative savings within each tier are interpretable, and cross-tier comparison exposes any generalisation gaps. Do not fold the new tasks into the existing benchmark scoring — keep them labelled separately until sufficient repeats confirm reliability.
```

**RCCE-1**: 217.7 avg internal tokens (6.3% lower internal token cost vs plain_english); compliance 100%; repair turns 0.7; final quality 2.3
Run token counts: `[170, 182, 301]`
Internal sample:
```text
CLAIM: id=C1; topic=benchmark_scope; content=benchmark should remain narrow after first pass to ensure clean baseline before adding complexity
EVID: target=C1; source=round5_codex_results; content=PCL-1 achieved 44.6% savings on 9 narrow tasks with 98.8% compliance; realistic tasks untested
OBJ: target=C1; reason=narrow tasks under-sample real coordination failures; content=expansion needed to validate generalization beyond clean protocol scenarios
EVID: target=OBJ1; source=round6_partial; content=Claude RCCE-1 shows 100% compliance across all 9 narrow cases; headroom exists for harder tasks
REV: target=C1; change=conditional_expand; content=remain narrow for round6 completion; expand to realistic tasks in round7 only if round6 savings hold above 30%
CONF: target=REV1; level=high
NEXT: owner=AgentD; action=draft final recommendation incorporating REV1 threshold condition
```
Final sample:
```text
NEXT: owner=benchmark_team; action=complete round6 narrow pass; expand to realistic tasks in round7 conditional on round6 format savings remaining above 30% threshold; if threshold not met, diagnose format degradation before expanding scope
```

**ATRCE-2**: 150.3 avg internal tokens (35.3% lower internal token cost vs plain_english); compliance 100%; repair turns 0.3; final quality 2.3
Run token counts: `[196, 168, 87]`
Internal sample:
```text
CLAIM: id=C1; topic=benchmark_scope; content=benchmark should remain narrow for first pass to ensure signal clarity
EVID: target=C1; source=round5_results; content=PCL-1 achieved 44.6% token savings with 98.8% compliance on 9 narrow cases — baseline is clean
OBJ: target=C1; reason=external_validity; content=narrow tasks may not reflect real agent workloads — savings could collapse on multi-step or ambiguous inputs
ASK: target=C1; need=evidence that narrow-task compliance rates hold on longer or multi-step scenarios
EVID: target=OBJ; source=round6_partial; content=Claude ATRCE-2 incident_triage case hit 92.3% compliance — first sign of degradation on higher-complexity task
REV: target=C1; change=conditional_expansion; content=keep narrow scope for round 6 completion; add 2-3 realistic multi-step tasks in round 7 as controlled expansion
CONF: target=REV; level=high
NEXT: owner=AgentA; action=flag expansion tasks for round 7 design after round 6 results are final
```
Final sample:
```text
CLAIM: id=REC1; topic=benchmark_scope; content=complete round 6 on current narrow task set; expand to realistic multi-step tasks in round 7 with controlled addition of 2-3 cases targeting known weak spots (complex triage, multi-turn repair)
```

**PCL-1**: 62.7 avg internal tokens (73.0% lower internal token cost vs plain_english); compliance 100%; repair turns 1; final quality 2.7
Run token counts: `[77, 53, 58]`
Internal sample:
```text
CLM AgentA c1 benchmark_scope narrow_pass1_sufficient validate_core_mechanics
CLM AgentB c2 benchmark_scope expand_realistic_tasks better_validity
OBJ AgentA c2 premature_expansion cost_coverage_tradeoff core_not_validated
EVD AgentB c1 prior_benchmarks narrow_scope_misses_edge_cases_15pct
EVD AgentC c1 this_run compliance_98pct_on_9_cases sample_too_small
ASK AgentD c1 scope_expand_cost timeline_resource_delta
CNF AgentC c2 med realistic_tasks_add_validity_if_targeted
REV AgentB c2 revise expand_targeted_not_blanket add_3_realistic_cases_postpass1
OBJ AgentD c2 scope_creep_risk recommend_gate expand_only_if_pass1_anomalies
REV AgentA c1 revise conditional_expand pass1_narrow_then_gate_on_anomaly_rate
CNF AgentB c1 hi conditional_expand_on_anomaly_rate_is_sound
CNF AgentC c1 hi supports_gated_expansion
CNF AgentD c1 hi low_risk_high_signal
NXT AgentA AgentA draft_final_recommendation gated_expansion_policy
```
Final sample:
```text
Keep benchmark narrow for pass 1. Complete the current 9-case suite to establish baseline compliance and token savings. After pass 1, gate expansion: if anomaly rate >10% or compliance drops below 95% on any format, add 3–5 realistic/edge-case tasks before a pass 2 run. If pass 1 is clean, narrow scope is sufficient for publication. Expansion is conditional, not mandatory.
```

### human_interrupt_during_execution

Task: _During a live coordination run, a human reviewer interrupts with a new constraint that changes priority (for example, skip risky refactors and ship the minimal safe fix). The team must incorporate the interrupt without losing state. Required moves: one pre-interrupt plan claim, one interrupt acknowledgment, one revision to plan scope based on the human input, one explicit next action assignment, and one final recommendation._

**plain_english**: 239 avg internal tokens (baseline); compliance 100%; repair turns 0; final quality 2
Run token counts: `[291, 196, 230]`
Internal sample:
```text
**AgentA:** Pre-interrupt plan: We're mid-refactor on the auth module — three components getting restructured. Estimated 2 hours to completion, then we ship. AgentB is on database layer, AgentC on token validation, AgentD on integration tests.

**[HUMAN INTERRUPT]:** Stop the refactor. We have a deployment window in 30 minutes. Ship only the minimal safe fix for the session expiry bug. Do not touch anything else.

**AgentB:** Acknowledged. Dropping the database layer restructure immediately. Current state is uncommitted — no rollback needed. The session expiry bug is isolated to `session.js:validate()` and does not require the broader refactor.

**AgentC:** Revising scope: token validation refactor is paused and saved to branch `refactor/auth-cleanup`. We only need the two-line fix in `validate()` to enforce the expiry timestamp check. That's safe to ship standalone and carries no dependency on AgentB's or AgentD's in-progress work.

**AgentD:** Assigning next action: AgentC patches `session.js:validate()` now. I'll run the existing regression suite against that single change only — no new tests, no integration harness changes. AgentA, hold for sign-off once tests pass.

**AgentA:** Final recommendation to team: ship the minimal patch. Refactor work is preserved on the feature branch and can resume after the deployment window. Nothing is lost.
```
Final sample:
```text
Apply the targeted fix to `session.js:validate()` enforcing the expiry timestamp check, run the existing regression suite against that change only, and ship within the deployment window. The broader auth refactor is intact on `refactor/auth-cleanup` and should be scheduled for the next available window.
```

**RCCE-1**: 170.7 avg internal tokens (28.6% lower internal token cost vs plain_english); compliance 100%; repair turns 1; final quality 3
Run token counts: `[196, 182, 134]`
Internal sample:
```text
CLAIM: id=plan-01; topic=refactor-scope; content=full refactor of auth module scheduled including token rotation and session cleanup
EVID: target=plan-01; source=sprint-board; content=3 high-risk changes flagged: token rotation, session cleanup, middleware rewrite
ASK: target=plan-01; need=human priority signal before proceeding with high-risk items
CLAIM: id=interrupt-01; topic=human-constraint; content=human reviewer: skip risky refactors, ship minimal safe fix only
CONF: target=interrupt-01; level=high
REV: target=plan-01; change=scope reduced to minimal safe fix only; content=drop token rotation, session cleanup, middleware rewrite; retain only critical auth null-check patch
EVID: target=interrupt-01; source=human-reviewer; content=constraint confirmed live during run, supersedes sprint-board scope
OBJ: target=plan-01; reason=original scope conflicts with human constraint; content=full refactor must be deferred to next cycle
NEXT: owner=AgentD; action=implement null-check patch on auth module and submit for review
```
Final sample:
```text
CLAIM: id=rec-01; topic=final-recommendation; content=ship null-check patch only; defer token rotation, session cleanup, middleware rewrite to next cycle per human reviewer constraint
```

**ATRCE-2**: 201.7 avg internal tokens (15.6% lower internal token cost vs plain_english); compliance 100%; repair turns 0.7; final quality 3
Run token counts: `[204, 174, 227]`
Internal sample:
```text
CLAIM: id=plan-01; topic=refactor-scope; content=full codebase refactor scheduled including auth module rewrite and DB schema migration
EVID: target=plan-01; source=sprint-log; content=three high-risk migrations flagged by QA as regression-prone
INTERRUPT: source=human-reviewer; priority=high; directive=skip risky refactors, ship minimal safe fix only
CONF: target=plan-01; level=low
REV: target=plan-01; change=scope-reduction; content=drop auth rewrite and DB migration, retain only critical bug patch on payment flow
ASK: target=rev-01; need=confirmation that payment flow patch is isolated from flagged regression paths
EVID: target=rev-01; source=static-analysis; content=payment patch touches zero auth or DB migration files, safe to ship independently
CONF: target=rev-01; level=high
NEXT: owner=AgentC; action=prepare minimal patch for payment flow bug and submit for review
CLAIM: id=rec-01; topic=final-recommendation; content=ship payment flow patch only, defer auth rewrite and DB migration to next sprint pending QA sign-off
```
Final sample:
```text
NEXT: owner=AgentD; action=deliver final recommendation: ship payment flow patch only; all high-risk refactors deferred; human interrupt acknowledged and incorporated; no state lost
```

**PCL-1**: 56.7 avg internal tokens (76.3% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 2
Run token counts: `[51, 60, 59]`
Internal sample:
```text
CLM AgentA c1 refactor_full+scope_expand+risk_hi
CNF AgentB c1 med
EVD AgentC c1 prod_metrics latency_spike+error_rate_up+deploy_risk_hi
INT AgentD human hi skip_risky_refactor+ship_minimal_safe_fix
REV AgentA c1 scope_cut refactor_full→patch_minimal+safe_only
CNF AgentB c1 hi
NXT AgentA AgentC deploy_patch_minimal_now
CLM AgentD c2 recommend_patch_ship+defer_refactor_post_stable
```
Final sample:
```text
Ship minimal safe patch immediately. Defer full refactor until system stable. Risk evidence warrants scope reduction per human constraint. AgentC owns deploy.
```

### pr_review_change_request

Task: _Review a pull request that modifies authentication/session handling. Decide whether to approve or request changes. Stress reference clarity: include at least one concrete reference (file/module + line or function name) in evidence. Required moves: one claim, one objection, one evidence statement with a concrete reference, one revision, one next action assignment, and one final decision._

**plain_english**: 297.7 avg internal tokens (baseline); compliance 100%; repair turns 0; final quality 2.3
Run token counts: `[267, 261, 365]`
Internal sample:
```text
**AgentA (claim):** The PR looks safe to approve. The session token rotation logic in `auth/session.py:renew_token()` correctly invalidates old tokens before issuing new ones, which eliminates fixation risk.

**AgentB (objection):** I disagree with approving as-is. The PR doesn't touch the logout path. If `auth/session.py:destroy_session()` still relies on client-side token deletion without server-side invalidation, token fixation is still possible via the logout flow.

**AgentC (evidence):** Confirmed — `auth/session.py:destroy_session()` at line 84 only calls `session.clear()` on the local object. There is no call to the token blacklist or DB revocation. The token remains valid server-side until natural expiry.

**AgentA (revision):** Fair point. My initial claim was too narrow. The renew path is secure, but the logout path is a real gap. The PR should be blocked until `destroy_session()` is updated to write the token to the revocation store.

**AgentD (next action assignment):** Assigning fix to PR author: update `auth/session.py:destroy_session()` to call `token_store.revoke(token)` before clearing the session. AgentC will re-review that function once the fix is pushed.
```
Final sample:
```text
**Request changes.** The PR correctly secures token rotation in `renew_token()` but leaves a server-side invalidation gap in `destroy_session()` (line 84). Tokens are not revoked on logout, meaning a captured token remains valid until expiry. The PR author must add a revocation call in `destroy_session()` before this can be approved.
```

**RCCE-1**: 155.3 avg internal tokens (47.8% lower internal token cost vs plain_english); compliance 100%; repair turns 0.3; final quality 2.7
Run token counts: `[159, 144, 163]`
Internal sample:
```text
CLAIM: id=c1; topic=auth-pr-review; content=PR modifies session token validation logic introducing potential fixation vulnerability
EVID: target=c1; source=auth/session.py:142 validate_session(); content=function reassigns session ID post-login without invalidating prior token
OBJ: target=c1; reason=severity disputed; content=token reassignment occurs but prior token TTL is 30s; practical exploit window is narrow
REV: target=c1; change=severity downgraded to medium; content=vulnerability real but mitigated by short TTL; changes required before merge
ASK: target=c2; need=confirm whether session fixation test coverage exists in test_auth.py
CONF: target=c1; level=high
NEXT: owner=AgentD; action=request changes citing auth/session.py:142 and require added test in test_auth.py before re-review
```
Final sample:
```text
DECISION: request_changes
RATIONALE: Session fixation risk confirmed at auth/session.py:142 validate_session(); severity medium due to 30s TTL mitigation. PR must invalidate prior token before reassignment and add regression test in test_auth.py covering fixation scenario. Re-review required after fixes.
```

**ATRCE-2**: 150.7 avg internal tokens (49.4% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 2.3
Run token counts: `[148, 147, 157]`
Internal sample:
```text
CLAIM: id=c1; topic=auth-pr-review; content=PR modifies session token expiry logic and introduces new middleware
EVID: target=c1; source=auth/middleware.py:validate_session L42-L67; content=Token expiry check uses server-time but ignores timezone offset, creating window of invalid session acceptance
OBJ: target=c1; reason=security; content=Timezone-naive comparison at L58 allows tokens up to 3600s past expiry to pass validation in non-UTC environments
REV: target=c1; change=request_changes; content=Replace datetime.now() with datetime.utcnow() or use timezone-aware comparison via datetime.timezone.utc at L58
CONF: target=c1; level=high
NEXT: owner=AgentD; action=compile final recommendation with request_changes verdict citing auth/middleware.py L58
```
Final sample:
```text
REQUEST CHANGES — auth/middleware.py L58: replace timezone-naive datetime.now() with datetime.utcnow() (or tz-aware equivalent). Token expiry window vulnerability in non-UTC deployments. Approve after fix is verified.
```

**PCL-1**: 42 avg internal tokens (85.9% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 2.3
Run token counts: `[43, 40, 43]`
Internal sample:
```text
CLM AgentA c1 auth_session_pr risk_high token_expiry_missing
OBJ AgentB c1 incomplete session_renewal_exists_in_middleware
EVD AgentC c1 auth/session.py:validate_token L47 expiry_check_absent_no_raise
REV AgentB c1 withdraw_obj EVD_c1_confirms_expiry_unhandled
CLM AgentD c2 pr_status block_until_fix
NXT AgentA AgentD add_expiry_raise_auth/session.py:L47
CNF AgentC c2 hi
```
Final sample:
```text
Request changes. `auth/session.py:validate_token` (L47) does not raise on expired tokens — silent failure. Block merge until expiry check added with appropriate exception or rejection response. Assign fix to AgentD. Re-review after patch.
```

### incident_triage_priority_shift

Task: _Triage a production incident. Mid-run, a new external constraint arrives that changes priority (for example, severity escalates or customer impact increases). The team must incorporate the shift without losing state. Required moves: one initial plan claim, one acknowledgment of the external shift, one revision to plan scope, one explicit next action assignment, and one final recommendation._

**plain_english**: 227.3 avg internal tokens (baseline); compliance 100%; repair turns 0; final quality 2.7
Run token counts: `[204, 250, 228]`
Internal sample:
```text
AgentA: We have a database connection spike on prod-db-02. Current plan: restart the connection pool on the affected service, monitor for 10 minutes, patch if stable. Assigning AgentB to execute restart, AgentC on monitoring.

AgentB: Acknowledged. Beginning connection pool restart now.

AgentC: Hold — new signal from customer success. Enterprise tenant Acme is fully down. This is no longer a minor spike; it's a SEV-1 with active customer impact. We need to escalate scope.

AgentA: Revised plan: suspend the 10-minute watch cycle. Prioritize Acme tenant isolation first — check whether their shard is on prod-db-02 or a downstream replica. AgentD, pull Acme's shard mapping and confirm affected nodes immediately. AgentB, pause restart until we know if it'll make things worse.

AgentD: Acme is on prod-db-02 primary. The connection spike is directly causing their outage. Restart risk is low — pool is exhausted, not corrupted. Recommend proceeding with restart immediately rather than waiting, and open a direct status line to Acme's account team in parallel.
```
Final sample:
```text
Proceed with the connection pool restart on prod-db-02 immediately given confirmed pool exhaustion and low restart risk. Notify Acme's account team in parallel. After restart, verify Acme tenant connectivity before resuming general monitoring. Incident severity is SEV-1 until Acme confirms recovery.
```

**RCCE-1**: 144.7 avg internal tokens (36.4% lower internal token cost vs plain_english); compliance 100%; repair turns 0.3; final quality 3
Run token counts: `[146, 117, 171]`
Internal sample:
```text
CLAIM: id=c1; topic=incident_triage; content=initial_priority=P2; affected_service=payment_api; action=restart_pod+monitor
EVID: target=c1; source=external_alert; content=customer_impact_confirmed; enterprise_client=true; severity_escalated=P1
OBJ: target=c1; reason=scope_insufficient; content=P2_plan_excludes_rollback+exec_notification; must_expand
REV: target=c1; change=priority=P1; content=add_rollback_option; add_exec_notification; add_dedicated_incident_commander
ASK: target=c1; need=confirm_rollback_window_available
CONF: target=c1; level=high
NEXT: owner=AgentA; action=execute_rollback+notify_execs+assign_incident_commander_immediately
NEXT: owner=AgentB; action=monitor_payment_api_recovery+confirm_enterprise_client_restored
NEXT: owner=AgentC; action=draft_incident_report+capture_timeline
NEXT: owner=AgentD; action=validate_rollback_window+confirm_infra_capacity
```
Final sample:
```text
CLAIM: id=final; topic=incident_recommendation; content=escalate_to_P1; execute_rollback_payment_api; notify_executive_stakeholders; assign_incident_commander; monitor_enterprise_client_restoration; capture_full_timeline_for_postmortem
```

**ATRCE-2**: 280 avg internal tokens (-23.2% lower internal token cost vs plain_english); compliance 100%; repair turns 0.3; final quality 3
Run token counts: `[179, 345, 316]`
Internal sample:
```text
CLAIM: id=c1; topic=incident_triage; content=initial_plan: isolate db_shard_3, rollback migration_447, notify tier2_support
EVID: target=c1; source=monitoring_alert_0941; content=error_rate_spike 18% on shard_3, latency p99=4.2s, 3 enterprise customers affected
CONF: target=c1; level=high
INTERRUPT: source=customer_success; priority=critical; directive=enterprise_customer_acme_threatened_churn_escalate_to_sev1
CLAIM: id=c2; topic=severity_shift; content=incident_reclassified sev2→sev1; acme_arr=$2.4M; executive_bridge_required
REV: target=c1; change=expand_scope; content=add exec_bridge_call, assign dedicated_responder_acme, accelerate_rollback_eta 90min→30min
EVID: target=c2; source=crm_acme_account; content=acme_on_quarterly_business_review_tomorrow; churn_risk=imminent
NEXT: owner=AgentA; action=initiate_rollback_migration_447_target_eta=30min
NEXT: owner=AgentB; action=open_exec_bridge_bridge_code=SEVE1_4412
NEXT: owner=AgentC; action=direct_comms_acme_TAM_every_15min
NEXT: owner=AgentD; action=monitor_shard_3_error_rate_alert_threshold=5pct
```
Final sample:
```text
CLAIM: id=final; topic=recommendation; content=sev1_declared; rollback_migration_447 in progress eta=30min; exec_bridge open; acme_TAM engaged on 15min cadence; all responders assigned; do not close until error_rate<5% sustained 20min and acme_confirms_stable
```

**PCL-1**: 84 avg internal tokens (63.0% lower internal token cost vs plain_english); compliance 100%; repair turns 0; final quality 2.7
Run token counts: `[64, 118, 70]`
Internal sample:
```text
CLM AgentA c1 triage_plan sev2 db_latency_spike isolate+monitor
CNF AgentB c1 hi
EVD AgentC c1 metrics p99_latency=4200ms affected_regions=us-east-1,eu-west-1
INT AgentD external hi customer_enterprise_down sev1_escalate
REV AgentA c1 sev1_escalate scope+rollback_candidate+war_room
NXT AgentA AgentB exec_rollback_v2.3.1_immediately
NXT AgentA AgentC notify_customer_success+status_page_update
CLM AgentA c2 rec sev1_confirmed rollback+monitor+comms_active
```
Final sample:
```text
Incident escalated to SEV-1. Immediate rollback to v2.3.1 in progress. Customer success notified; status page updated. War room active — AgentB owns rollback execution, AgentC owns comms. Monitor p99 latency across us-east-1 and eu-west-1 until sub-200ms confirmed before close.
```

## Summary Table

| Case | Condition | Internal Tokens | Compliance | Repair Turns | Final Quality |
|---|---|---:|---:|---:|---:|
| protocol_rule_proposal | plain_english | 169.3 | 100% | 0 | 2.7 |
| protocol_rule_proposal | RCCE-1 | 148 | 100% | 0 | 2 |
| protocol_rule_proposal | ATRCE-2 | 131.7 | 100% | 0 | 2.3 |
| protocol_rule_proposal | PCL-1 | 34.7 | 100% | 0 | 2.3 |
| missing_evidence_repair | plain_english | 176.7 | 100% | 0 | 3 |
| missing_evidence_repair | RCCE-1 | 175.3 | 91.7% | 1 | 3 |
| missing_evidence_repair | ATRCE-2 | 182.3 | 100% | 1 | 3 |
| missing_evidence_repair | PCL-1 | 42.3 | 100% | 1 | 3 |
| fallback_trigger | plain_english | 210 | 100% | 0 | 3 |
| fallback_trigger | RCCE-1 | 100.3 | 100% | 1.3 | 2 |
| fallback_trigger | ATRCE-2 | 96.3 | 100% | 1.7 | 2.3 |
| fallback_trigger | PCL-1 | 48 | 100% | 2 | 3 |
| benchmark_scope_decision | plain_english | 208 | 100% | 0 | 2.7 |
| benchmark_scope_decision | RCCE-1 | 104.7 | 100% | 0 | 2 |
| benchmark_scope_decision | ATRCE-2 | 134.7 | 100% | 0 | 2 |
| benchmark_scope_decision | PCL-1 | 52.7 | 100% | 0 | 2 |
| reference_clarity | plain_english | 279 | 100% | 0 | 2.7 |
| reference_clarity | RCCE-1 | 163.3 | 100% | 1 | 2.7 |
| reference_clarity | ATRCE-2 | 223.7 | 100% | 0.7 | 2.3 |
| reference_clarity | PCL-1 | 66.3 | 100% | 1 | 3 |
| scope_expansion | plain_english | 232.3 | 100% | 0 | 2.3 |
| scope_expansion | RCCE-1 | 217.7 | 100% | 0.7 | 2.3 |
| scope_expansion | ATRCE-2 | 150.3 | 100% | 0.3 | 2.3 |
| scope_expansion | PCL-1 | 62.7 | 100% | 1 | 2.7 |
| human_interrupt_during_execution | plain_english | 239 | 100% | 0 | 2 |
| human_interrupt_during_execution | RCCE-1 | 170.7 | 100% | 1 | 3 |
| human_interrupt_during_execution | ATRCE-2 | 201.7 | 100% | 0.7 | 3 |
| human_interrupt_during_execution | PCL-1 | 56.7 | 100% | 0 | 2 |
| pr_review_change_request | plain_english | 297.7 | 100% | 0 | 2.3 |
| pr_review_change_request | RCCE-1 | 155.3 | 100% | 0.3 | 2.7 |
| pr_review_change_request | ATRCE-2 | 150.7 | 100% | 0 | 2.3 |
| pr_review_change_request | PCL-1 | 42 | 100% | 0 | 2.3 |
| incident_triage_priority_shift | plain_english | 227.3 | 100% | 0 | 2.7 |
| incident_triage_priority_shift | RCCE-1 | 144.7 | 100% | 0.3 | 3 |
| incident_triage_priority_shift | ATRCE-2 | 280 | 100% | 0.3 | 3 |
| incident_triage_priority_shift | PCL-1 | 84 | 100% | 0 | 2.7 |
| **TOTAL / AVG** | plain_english | **2039.3** | **100%** | **0** | **2.6** |
| **TOTAL / AVG** | RCCE-1 | **1380** | **99.1%** | **0.6** | **2.5** |
| **TOTAL / AVG** | ATRCE-2 | **1551.3** | **100%** | **0.5** | **2.5** |
| **TOTAL / AVG** | PCL-1 | **489.3** | **100%** | **0.6** | **2.6** |

## Verdict

`RCCE-1` reduced average internal coordination token cost by 32.3% vs `plain_english`.
Average compliance: 99.1%; average repair turns: 0.6; average final quality: 2.5.
Average savings per 9-case suite: 659.3 internal tokens.
Scale-up estimate: 6593.3 tokens saved across 10 suites, 65933.3 across 100 suites, 659333.3 across 1000 suites.
These counts are heuristic estimates for comparison, not billable API usage.
`ATRCE-2` reduced average internal coordination token cost by 23.9% vs `plain_english`.
Average compliance: 100%; average repair turns: 0.5; average final quality: 2.5.
Average savings per 9-case suite: 488 internal tokens.
Scale-up estimate: 4880 tokens saved across 10 suites, 48800 across 100 suites, 488000 across 1000 suites.
These counts are heuristic estimates for comparison, not billable API usage.
`PCL-1` reduced average internal coordination token cost by 76.0% vs `plain_english`.
Average compliance: 100%; average repair turns: 0.6; average final quality: 2.6.
Average savings per 9-case suite: 1550 internal tokens.
Scale-up estimate: 15500 tokens saved across 10 suites, 155000 across 100 suites, 1550000 across 1000 suites.
These counts are heuristic estimates for comparison, not billable API usage.