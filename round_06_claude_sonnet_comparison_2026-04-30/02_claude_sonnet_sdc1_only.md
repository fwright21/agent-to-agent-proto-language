# Coordination Benchmark Results

Generated: 2026-05-03 19:28

Runner: `claude`

Count mode: `estimate`

Claude model: `claude-sonnet-4-6`

Repeats per condition/case: `3`

Baseline: `plain_english`

Conditions: `plain_english`, `SDC-1`

> **Note on token counts:** Counts use a heuristic estimator, not a model-native tokenizer. Relative savings between conditions within this run are meaningful. Absolute numbers are not directly comparable to runs using `openai_exact` counting.

## Per-Case Results

### protocol_rule_proposal

Task: _Decide whether confidence labels should be mandatory in the coordination protocol. Required moves: one claim, one objection, one supporting evidence statement, one revision, and one final recommendation._

**plain_english**: 203 avg internal tokens (baseline); compliance 100%; repair turns 0; final quality 2.7
Run token counts: `[192, 211, 206]`
Internal sample:
```text
**AgentA (claim):** Confidence labels should be mandatory. Without them, downstream agents cannot calibrate trust in claims, which leads to compounding errors in multi-step decisions.

**AgentB (objection):** Mandatory labels add overhead and may be gamed — agents could default to "high confidence" on everything, which is worse than no label since it creates false trust.

**AgentC (supporting evidence):** In rounds 4 and 5 of our benchmark, cases without explicit confidence signals had higher repair rates. Structured metadata reduced ambiguity cascades even when labels were imprecise.

**AgentD (revision):** Mandatory is too strong. Require confidence labels only when a claim drives an irreversible action or a fork in the coordination path. Optional elsewhere, but the protocol should define when they trigger.

**AgentA (final recommendation defer):** AgentD's revision is sound. I withdraw "always mandatory" in favor of the conditional rule.
```
Final sample:
```text
Confidence labels are required when a claim directly drives an irreversible action or a decision branch; they are optional in informational exchanges. The protocol should define a trigger condition list rather than blanket mandating labels. This balances epistemic clarity against overhead and prevents performative labeling.
```

**SDC-1**: 79.7 avg internal tokens (60.8% lower internal token cost vs plain_english); compliance 0%; repair turns 0; final quality 2.3
Run token counts: `[72, 62, 105]`
Internal sample:
```text
AgentA: +c1 conf_labels->mandatory; parse_ambiguity-↓,interop-↑
AgentB: -c1 mandatory->overhead↑; low_stakes_tasks=conf_not_needed
AgentC: =c1 trials:conf_labels->err_rate-23%,coord_time-↓15%
AgentD: ~c1 mandatory->high_stakes_only; low_stakes=optional
AgentA: ^c1 0.8 revised_pos:mandatory|scoped>blanket
```
Final sample:
```text
Confidence labels SHOULD be mandatory for high-stakes coordination tasks; optional elsewhere. Evidence shows measurable error reduction; blanket mandate adds unnecessary overhead for simple tasks.
```

### missing_evidence_repair

Task: _One agent makes a broad compression claim without evidence. Another agent must request support. The group must decide whether to keep, revise, or reject the claim. Required moves: unsupported claim, request for evidence, evidence response, confidence marker, and final decision._

**plain_english**: 187.3 avg internal tokens (baseline); compliance 100%; repair turns 0; final quality 3
Run token counts: `[193, 181, 188]`
Internal sample:
```text
**AgentA:** I've reviewed our options. Switching to compressed token format will cut communication overhead by 60% across all coordination tasks.

**AgentB:** That's a significant claim. What's the supporting data? Which tasks, which baselines, and how was the 60% measured?

**AgentA:** The figure comes from three runs on protocol negotiation, scope decision, and incident triage tasks. Compressed format averaged 128 tokens versus 320 for plain English — a 60% reduction. Compliance held at 98%.

**AgentC:** Those three tasks skew short and structured. I'd rate confidence at moderate — the saving likely holds for similar task types but may not generalize to longer or more ambiguous exchanges.

**AgentD:** Agreed. The evidence supports a narrower claim. I'd revise to: compressed format reduces tokens by approximately 60% on structured coordination tasks, with generalization to other task types unconfirmed.
```
Final sample:
```text
Revised claim adopted: compressed format achieves approximately 60% token reduction on structured coordination tasks (protocol negotiation, scope decision, incident triage) with 98% compliance. Generalization to unstructured or long-form tasks is unconfirmed. Recommend proceeding with compressed format for structured tasks only, pending further evidence on broader applicability.
```

**SDC-1**: 112.3 avg internal tokens (40.0% lower internal token cost vs plain_english); compliance 0%; repair turns 0; final quality 2.7
Run token counts: `[109, 97, 131]`
Internal sample:
```text
AgentA: +c1 compress:all>50%|no_loss
AgentB: ?c1 evid=null->support_req
AgentC: ?c1 baseline|sample|method=?
AgentA: =c1 bench:3x50t|avg=52%↓|qual=0.95
AgentD: ^c1 0.7|cond:domain_narrow
AgentB: ~c1 compress:all>50% -> compress:narrow_domain>50%
AgentC: =c2 /c1 "all" overstates: bench scope=3 domains only
AgentD: !c1 revise^accept|reject:orig
```
Final sample:
```text
~c1 compress:bench_domains>50%|qual≥0.95|scope:narrow_not_universal -> ACCEPT_REVISED
```

### fallback_trigger

Task: _The team encounters a nuanced exception case that may not fit the protocol safely. It must decide whether to stay in protocol or escalate to plain language. Required moves: compressed claim, objection based on nuance risk, fallback or escalation decision, and final recommendation._

**plain_english**: 220.3 avg internal tokens (baseline); compliance 100%; repair turns 0; final quality 2.7
Run token counts: `[208, 209, 244]`
Internal sample:
```text
**AgentA:** The exception case involves a conflicting dependency where two protocol rules simultaneously trigger — protocol covers this nominally, but the resolution order is ambiguous. Flagging: apply rule-priority-descending, resolve to Rule 7 over Rule 3.

**AgentB:** Objection. Rule 7 assumes single-context activation. This case has dual-context overlap, which makes the priority ordering undefined rather than merely ambiguous. Compressing the resolution claim risks masking the edge — downstream agents may apply the wrong rule silently.

**AgentC:** Agreed on the risk. I'd add: if we stay in protocol here, we need an explicit uncertainty marker in the output. But the protocol doesn't have a reserved token for "undefined resolution." Attempting to encode it anyway would be lossy and potentially misleading.

**AgentD:** Given no safe protocol encoding exists for this state, I recommend escalating to plain language for this case only. The protocol handles it structurally but not semantically. A plain-language note preserves accuracy without corrupting the protocol output for surrounding cases.

---
```
Final sample:
```text
Escalate this specific case to plain language. The dual-context rule conflict cannot be safely encoded in the current protocol — there is no token or resolution path that captures the ambiguity without introducing downstream error risk. All other cases in the exchange should remain in protocol. A plain-language annotation should document the conflict, the two competing rules, and the rationale for deferring resolution to human review.
```

**SDC-1**: 62 avg internal tokens (71.9% lower internal token cost vs plain_english); compliance 0%; repair turns 0; final quality 1.7
Run token counts: `[60, 64, 62]`
Internal sample:
```text
AgentA: +c1 exception->proto_edge|compress_ok if scope=bounded
AgentB: -c1 nuance_risk>compress_loss|proto_unsafe if ambiguity=high
AgentC: =c1 case_fit<0.7->escalate_thresh|evidence=prior_fail@edge
AgentD: /c1 ESCALATE: compressed repr cannot preserve exception semantics without distortion risk
```
Final sample:
```text
/c1 ESCALATE TO PLAIN LANGUAGE: exception case exceeds safe compression boundary. Protocol does not apply.
```

### benchmark_scope_decision

Task: _Choose a first benchmark task: narrow review workflow or broader open-ended debate. Balance comparability against realism. Required moves: claim for one option, objection for the other tradeoff, evidence or rationale, revision or compromise, and final benchmark recommendation._

**plain_english**: 233.7 avg internal tokens (baseline); compliance 100%; repair turns 0; final quality 2.7
Run token counts: `[236, 252, 213]`
Internal sample:
```text
**AgentA:** I recommend the narrow review workflow for our first benchmark task. It gives us clean, comparable outputs — structured inputs and expected responses mean we can measure format compliance and token savings directly across conditions.

**AgentB:** Objection: narrow review tasks sacrifice realism. Agent coordination in practice involves ambiguity and judgment calls, not just structured handoffs. A constrained task may flatter compressed formats that perform poorly when content is actually complex.

**AgentC:** Both points hold, but the evidence favors narrow first. Broader open-ended tasks introduce too many confounds — evaluator disagreement, no ground truth, high variance across repeats. Our Round 5 data showed compliance and token savings tracked cleanly on structured tasks. We'd need a calibration baseline before open-ended results mean anything.

**AgentD:** Agreed with AgentC. Revising: we run narrow review workflow as the first benchmark to establish a clean baseline, then extend to open-ended debate in a later round once we know how each format performs under controlled conditions. This keeps comparability intact without abandoning realism as a long-term goal.

**AgentA:** Accepted. Narrow review workflow first, open-ended debate as a planned follow-on.

---
```
Final sample:
```text
The group recommends **narrow review workflow** as the first benchmark task. It provides structured inputs and measurable expected outputs, enabling clean comparisons of token savings and compliance across formats. Open-ended debate tasks are deferred to a later round, once a calibrated baseline exists. This preserves comparability now without permanently sacrificing realism.
```

**SDC-1**: 94 avg internal tokens (59.8% lower internal token cost vs plain_english); compliance 0%; repair turns 0; final quality 2
Run token counts: `[93, 94, 95]`
Internal sample:
```text
AgentA: +c1 narrow_review>broad_debate: comparability^high, control^high
AgentB: -c1 narrow_review: realism^low|agent_edge_cases->hidden
AgentC: =c1 narrow_review: token_variance->measurable, eval_criteria->stable, cross_run_reproducibility^high
AgentD: ~c1 narrow_review+realism_constraint: add open_ended_turn as optional_extension, core=narrow
AgentA: ^c1 0.85 narrow_review_with_extension
AgentB: =c1 extension_flag: broad_debate->phase2, not_phase1
AgentC: !c1 recommend=narrow_review_primary|broad_debate_optional
```
Final sample:
```text
narrow_review_workflow — primary benchmark task. Rationale: comparability>realism for phase1; controlled eval criteria; reproducible token variance. Broad/open-ended debate deferred to optional extension phase.
```

### reference_clarity

Task: _Decide when explicit references are necessary in the protocol. Balance repairability against token cost. Required moves: claim, objection, evidence, revision, and final recommendation._

**plain_english**: 308 avg internal tokens (baseline); compliance 100%; repair turns 0.3; final quality 2.7
Run token counts: `[326, 261, 337]`
Internal sample:
```text
**AgentA (claim):** Explicit references should only be required when the referent is ambiguous — i.e., when a pronoun or shorthand could resolve to more than one prior entity. In unambiguous contexts, omitting explicit references saves tokens with no repairability cost.

**AgentB (objection):** That's too narrow. Ambiguity isn't the only repair trigger. Even unambiguous references fail when the receiving agent lacks the context window to reconstruct what's being referred to. We should require explicit references whenever the referent was introduced more than N turns ago.

**AgentC (evidence):** Round 5 data supports a middle ground. `missing_evidence_repair` was the only case with below-threshold compliance (91.7%) in PCL-1 — and that case involved a referent introduced early and not repeated. Meanwhile fully explicit formats (plain English) showed no repair failures but cost ~44% more tokens. Omitting references selectively caused one failure mode; omitting them broadly would cause more.

**AgentD (revision):** Revise the claim: require explicit references when (1) the referent is ambiguous, OR (2) the referent was not introduced in the immediately preceding turn. This captures AgentB's context-window concern while keeping token cost lower than full-explicit mode. The N=1 turn boundary is conservative but empirically grounded by AgentC's data.

**AgentA (accepts revision):** Agreed. The two-condition rule adds one explicit reference per cross-turn reference, which is low overhead. The repair cost of omitting it — as seen in `missing_evidence_repair` — is higher than the token cost of including it.

---
```
Final sample:
```text
Explicit references are required in two conditions: (1) the referent is ambiguous at the point of use, or (2) the referent was not introduced in the immediately preceding turn. Within a single turn or in direct continuation, shorthand and pronouns are permitted. This rule minimizes unnecessary token cost while preventing the cross-turn reference failures observed in benchmark data. It should be encoded as a base protocol constraint, not left to agent discretion.
```

**SDC-1**: 113 avg internal tokens (63.3% lower internal token cost vs plain_english); compliance 0%; repair turns 0; final quality 3
Run token counts: `[103, 105, 131]`
Internal sample:
```text
AgentA: +c1 explicit_ref=required@ambig_ctx|cross-turn_ptr
AgentB: -c1 ref_overhead>repair_cost@low_ambig_ctx
AgentC: =c1 ambig_rate~0.3->ref_saves>0.7*repair_cost
AgentD: ?c1 threshold_ambig: fixed|dynamic?
AgentA: ~c1 explicit_ref=conditional@ambig_prob>0.25|cross-turn>2
AgentB: ^c1 0.8 conditional>always
AgentC: ^c1 0.9 data_supports_threshold
AgentD: !c1 adopt~c1: ref_iff(ambig>0.25|span>2turns)
```
Final sample:
```text
Use explicit references conditionally: required when ambiguity probability exceeds 0.25 or referent span exceeds 2 turns; omit otherwise to minimise token cost while preserving repairability.
```

### scope_expansion

Task: _Decide whether the benchmark should remain narrow or expand to more realistic tasks after the first pass. Required moves: claim, objection, evidence, revision, and final recommendation._

**plain_english**: 242.7 avg internal tokens (baseline); compliance 100%; repair turns 0; final quality 2
Run token counts: `[245, 272, 211]`
Internal sample:
```text
**AgentA (claim):** The benchmark should stay narrow after the first pass. Our current task set is small and controlled, which lets us isolate format effects cleanly. Expanding too early risks confounding variables.

**AgentB (objection):** Narrow tasks are synthetic. If we only test protocol-style edge cases, we can't tell whether savings hold on messier, real-world inputs. The first pass results may not generalise.

**AgentC (evidence):** Round 5 data supports both views. PCL-1 held 98.8% compliance across 9 controlled cases, but all 9 cases are tightly scoped coordination scenarios. There's no data on unstructured or multi-turn realistic tasks, so we genuinely don't know if the savings pattern survives.

**AgentD (revision):** Split the difference. Keep the current narrow set as a fixed regression baseline, then add a second tier of 4–6 realistic tasks in parallel. Run both tiers together next pass. This preserves comparability while generating the generalisation data we're missing.

**AgentA (response to revision):** Agreed. The fixed baseline protects the longitudinal comparison; the new tier answers the external validity question without discarding prior work.

---
```
Final sample:
```text
Retain the existing narrow task set as a locked baseline for longitudinal comparison. Add a second tier of 4–6 realistic, less structured tasks to the next benchmark pass. Run both tiers simultaneously. Report results separately per tier so narrow-task trends remain interpretable while generalisability can be assessed independently.
```

**SDC-1**: 111.7 avg internal tokens (54.0% lower internal token cost vs plain_english); compliance 0%; repair turns 0; final quality 2.3
Run token counts: `[117, 120, 98]`
Internal sample:
```text
AgentA: +c1 bench->narrow|first-pass->validate_core
AgentB: -c1 narrow->miss_real_world|edge_cases->unseen
AgentC: =c1 round5_PCL1->98.8%compliance|9cases->synthetic_only
AgentD: ?c1 expand->cost*time>benefit?|scope_signal->unclear
AgentA: ~c1 narrow->narrow+1real_task|hedge_cost
AgentB: ^c1 expand@50%|risk->overfit_synth->high
AgentC: =c1 claude_r6->same9cases|cross-runner->confirm_pattern
AgentD: !c1 narrow+1real->next_pass|re-eval->post_r6
```
Final sample:
```text
Maintain narrow benchmark for current pass; append one realistic task proxy. Re-evaluate expansion after Round 6 cross-runner results confirm pattern stability.
```

### human_interrupt_during_execution

Task: _During a live coordination run, a human reviewer interrupts with a new constraint that changes priority (for example, skip risky refactors and ship the minimal safe fix). The team must incorporate the interrupt without losing state. Required moves: one pre-interrupt plan claim, one interrupt acknowledgment, one revision to plan scope based on the human input, one explicit next action assignment, and one final recommendation._

**plain_english**: 187 avg internal tokens (baseline); compliance 100%; repair turns 0; final quality 2
Run token counts: `[182, 177, 202]`
Internal sample:
```text
**AgentA:** Current plan is to refactor the auth middleware, clean up the token validation logic, and then ship. Estimated 4 tasks, 2 are structural changes.

**[HUMAN INTERRUPT]:** Skip the refactors. Ship only the minimal safe fix. Do not touch anything that isn't broken.

**AgentB:** Acknowledged. Dropping the structural refactor tasks. We scope down to the single failing validation check — that's the only confirmed broken path.

**AgentC:** Revised scope: one targeted fix to the null token edge case in `validateToken()`. No middleware restructuring, no cleanup. AgentD, take the fix and run the existing auth test suite before marking ready.

**AgentD:** Confirmed. I have the null token fix scoped. Will apply change, run auth tests, and flag for review. No other files will be touched.
```
Final sample:
```text
Ship a single targeted fix for the null token edge case in `validateToken()`. All refactoring work is deferred. AgentD applies the change and validates against the existing test suite. Once tests pass, the fix is ready to ship. No structural changes are included in this release.
```

**SDC-1**: 133.3 avg internal tokens (28.7% lower internal token cost vs plain_english); compliance 3.7%; repair turns 0; final quality 2.3
Run token counts: `[128, 136, 136]`
Internal sample:
```text
AgentA: +c1 plan->refactor_auth|migrate_db|update_api priority=perf>safety
AgentB: =c1 refactor_auth~risk:high|db_migrate~downtime:est30min
AgentC: ^c1 safety<perf given_current_load|rollback_cost>refactor_gain
AgentD: @c1 human_interrupt: skip_risky_refactors->ship_minimal_safe_fix only
AgentA: ~c1 plan->drop(refactor_auth|migrate_db)|keep(update_api+minimal_patch)
AgentB: =c1 minimal_patch->hotfix_auth_edge_case|api_compat_shim safety=high risk=low
AgentC: ^c1 revised_scope viable|rollback_trivial|ship_eta<2h
AgentD: !c1 AgentA->implement(hotfix_auth_edge_case+api_compat_shim) AgentB->review AgentC->stage AgentD->monitor
```
Final sample:
```text
Ship minimal safe fix: hotfix_auth_edge_case + api_compat_shim. Drop refactor_auth and migrate_db from this run. Assign: AgentA implements, AgentB reviews, AgentC stages, AgentD monitors. Estimated delivery <2h, rollback trivial.
```

### pr_review_change_request

Task: _Review a pull request that modifies authentication/session handling. Decide whether to approve or request changes. Stress reference clarity: include at least one concrete reference (file/module + line or function name) in evidence. Required moves: one claim, one objection, one evidence statement with a concrete reference, one revision, one next action assignment, and one final decision._

**plain_english**: 269.7 avg internal tokens (baseline); compliance 100%; repair turns 0; final quality 2.7
Run token counts: `[284, 320, 205]`
Internal sample:
```text
**AgentA (claim):** The PR changes session token expiry logic in `auth/session.py:validate_token()`. The new default TTL of 7 days is too long for a security-sensitive service — it increases the window for token replay attacks.

**AgentB (objection):** The TTL increase is intentional per product requirements. Shortening it causes excessive re-authentication friction for users on mobile, which was filed as a UX regression in the last sprint.

**AgentC (evidence):** Looking at `auth/session.py:validate_token()` line 84, the PR removes the `sliding_expiry` call that previously reset the TTL on activity. Without it, inactive sessions persist for the full 7 days regardless of inactivity. That's the actual risk, not the TTL duration itself.

**AgentD (revision):** Agree with AgentC. The fix is to restore `sliding_expiry` while keeping the 7-day maximum. That satisfies both the UX requirement and the security concern — idle sessions still expire promptly.

**AgentA (next action):** Assign back to the PR author to reinstate the `sliding_expiry` call in `validate_token()` with the 7-day cap as the outer bound. Request they add a test case for the idle-timeout path before re-review.

**AgentB (final decision):** Request changes. Approve once `sliding_expiry` is restored and the idle-timeout test is added.

---
```
Final sample:
```text
Request changes on this PR. The core issue is not the 7-day TTL but the removal of `sliding_expiry` in `auth/session.py:validate_token()` (line 84), which causes sessions to persist at full duration regardless of inactivity. The PR author should restore sliding expiry with 7 days as the maximum bound, and add a test covering idle session timeout. Approve after those two changes are confirmed.
```

**SDC-1**: 120 avg internal tokens (55.5% lower internal token cost vs plain_english); compliance 0%; repair turns 0; final quality 2.3
Run token counts: `[93, 149, 118]`
Internal sample:
```text
AgentA: +c1 auth/session PR->approve; session_expiry logic correct, csrf_token refresh valid
AgentB: -c1 sessions.py:L142 validate_token() missing expiry_check->stale token bypass risk
AgentC: =c1 sessions.py:L142 validate_token returns True when token_expiry==None; confirmed stale path
AgentD: ~c1 approve->request_changes; expiry_check gap confirmed, fix required before merge
AgentA: !c1 @AgentB patch sessions.py:L142 add expiry_check guard->resubmit
```
Final sample:
```text
REQUEST_CHANGES: sessions.py:L142 validate_token() must reject token when token_expiry==None; add guard `if token_expiry is None: return False` before existing checks; resubmit after fix.
```

### incident_triage_priority_shift

Task: _Triage a production incident. Mid-run, a new external constraint arrives that changes priority (for example, severity escalates or customer impact increases). The team must incorporate the shift without losing state. Required moves: one initial plan claim, one acknowledgment of the external shift, one revision to plan scope, one explicit next action assignment, and one final recommendation._

**plain_english**: 210.7 avg internal tokens (baseline); compliance 100%; repair turns 0; final quality 2
Run token counts: `[230, 224, 178]`
Internal sample:
```text
AgentA: Taking lead on the production incident. Current state: API gateway throwing 5xx on ~8% of requests, onset 14:32 UTC. Isolating to payment service cluster. Plan is to roll back the 14:20 deploy and monitor for 10 minutes before declaring stable.

AgentB: Confirmed, I've paused further deploys to that cluster. Rollback is staged and ready on my end.

AgentC: New external constraint — customer success just flagged that three enterprise accounts are fully blocked. This is no longer a partial outage. Severity escalates to P1. SLA breach risk in under 30 minutes.

AgentA: Acknowledged. Revising scope: rollback is still the right move but we can't wait for a 10-minute observation window. We need simultaneous traffic rerouting to the healthy cluster while rollback proceeds, and someone needs to own customer comms immediately.

AgentD: I'll take customer comms — drafting status page update and direct outreach to the three affected accounts now. AgentB, execute the rollback and traffic shift concurrently. AgentC, stay on monitoring and call out the moment error rate drops below 1%.

AgentC: On monitoring. Will confirm recovery threshold or escalate further if error rate holds.
```
Final sample:
```text
Execute the payment service rollback immediately in parallel with traffic rerouting to the healthy cluster. Do not wait for a post-rollback observation window before rerouting — SLA exposure is active. Customer-facing communications should go out within the next five minutes covering the three blocked enterprise accounts. Declare incident resolved only after error rate falls below 1% and all three accounts confirm restored access.
```

**SDC-1**: 138.3 avg internal tokens (34.3% lower internal token cost vs plain_english); compliance 0%; repair turns 0; final quality 2
Run token counts: `[122, 141, 152]`
Internal sample:
```text
AgentA: +c1 sev2->db_latency|scope:api_team|eta:30m
AgentB: =c2 p99>2s|affected:3svc|err_rate:4%
AgentC: ?c3 customer_impact>threshold|escalate?
AgentD: @c4 ext_constraint:enterprise_client_down|sev2->sev1
AgentA: ~c1 scope:api_team+db_team|eta:30m->15m|prio:sev1
AgentB: ^c5 db_conn_pool=root_cause|confidence:0.85
AgentC: !c6 db_team->conn_pool_fix|api_team->lb_failover|owner:AgentD
AgentD: +c7 recommend:conn_pool_increase+lb_reroute|notify:enterprise_client|postmortem:+1h
```
Final sample:
```text
SEV1 | ROOT: db_conn_pool exhaustion → cascading api latency | IMPACT: enterprise client down + 3 internal services | ACTION: (1) db_team increase conn_pool immediately (2) api_team trigger lb_failover to healthy region | NOTIFY: enterprise client ETA 15m | FOLLOW-UP: postmortem +1h post-resolution
```

## Summary Table

| Case | Condition | Internal Tokens | Compliance | Repair Turns | Final Quality |
|---|---|---:|---:|---:|---:|
| protocol_rule_proposal | plain_english | 203 | 100% | 0 | 2.7 |
| protocol_rule_proposal | SDC-1 | 79.7 | 0% | 0 | 2.3 |
| missing_evidence_repair | plain_english | 187.3 | 100% | 0 | 3 |
| missing_evidence_repair | SDC-1 | 112.3 | 0% | 0 | 2.7 |
| fallback_trigger | plain_english | 220.3 | 100% | 0 | 2.7 |
| fallback_trigger | SDC-1 | 62 | 0% | 0 | 1.7 |
| benchmark_scope_decision | plain_english | 233.7 | 100% | 0 | 2.7 |
| benchmark_scope_decision | SDC-1 | 94 | 0% | 0 | 2 |
| reference_clarity | plain_english | 308 | 100% | 0.3 | 2.7 |
| reference_clarity | SDC-1 | 113 | 0% | 0 | 3 |
| scope_expansion | plain_english | 242.7 | 100% | 0 | 2 |
| scope_expansion | SDC-1 | 111.7 | 0% | 0 | 2.3 |
| human_interrupt_during_execution | plain_english | 187 | 100% | 0 | 2 |
| human_interrupt_during_execution | SDC-1 | 133.3 | 3.7% | 0 | 2.3 |
| pr_review_change_request | plain_english | 269.7 | 100% | 0 | 2.7 |
| pr_review_change_request | SDC-1 | 120 | 0% | 0 | 2.3 |
| incident_triage_priority_shift | plain_english | 210.7 | 100% | 0 | 2 |
| incident_triage_priority_shift | SDC-1 | 138.3 | 0% | 0 | 2 |
| **TOTAL / AVG** | plain_english | **2062.3** | **100%** | **0.0** | **2.5** |
| **TOTAL / AVG** | SDC-1 | **964.3** | **0.4%** | **0** | **2.3** |

## Verdict

`SDC-1` reduced average internal coordination token cost by 53.2% vs `plain_english`.
Average compliance: 0.4%; average repair turns: 0; average final quality: 2.3.
Average savings per 9-case suite: 1098 internal tokens.
Scale-up estimate: 10980 tokens saved across 10 suites, 109800 across 100 suites, 1098000 across 1000 suites.
These counts are heuristic estimates for comparison, not billable API usage.