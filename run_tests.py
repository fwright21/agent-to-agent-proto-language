"""
Live benchmark harness: plain-English coordination vs compressed protocol coordination.
Runs the same collaboration task under different coordination modes, measures
internal exchange cost, protocol compliance, repair overhead, and final output.

Usage:
  python run_tests.py --runner claude
  python run_tests.py --runner codex

Requires: selected CLI available and logged in.
"""

import argparse
import datetime
import math
import os
import re
import subprocess
from typing import List, Tuple
from pathlib import Path

try:
    import tiktoken
except ImportError:  # pragma: no cover - optional dependency
    tiktoken = None

CONDITIONS = {
    "plain_english": (
        "Simulate a 4-agent coordination exchange in concise plain English. Agents may be brief, but they "
        "should speak in normal readable prose. Avoid fluff, but do not use the compressed protocol schema."
    ),
    "rcce_1": (
        "Simulate a 4-agent coordination exchange using Relevance-Core Coordination English (RCCE-1) only.\n"
        "Each internal message must be exactly one line: TYPE: field=value; field=value\n"
        "Allowed types and REQUIRED fields (use these exact field names):\n"
        "- CLAIM: id, topic, content\n"
        "- EVID: target, source, content\n"
        "- OBJ: target, reason, content\n"
        "- REV: target, change, content\n"
        "- ASK: target, need\n"
        "- CONF: target, level (one of low|medium|high)\n"
        "- NEXT: owner, action\n"
        "- ESCALATE: reason (optional: target)\n"
        "Rules: one message per line; no extra fields; no agent names; no prose outside this schema. Use ESCALATE instead of free prose when the schema cannot safely express meaning."
    ),
    "atrce_2": (
        "Simulate a 4-agent coordination exchange using Act-Typed Relevance Coordination English (ATRCE-2) only.\n"
        "Each internal message must be exactly one line: TYPE: field=value; field=value\n"
        "Allowed types and REQUIRED fields (use these exact field names):\n"
        "- CLAIM: id, topic, content\n"
        "- EVID: target, source, content\n"
        "- OBJ: target, reason, content\n"
        "- REV: target, change, content\n"
        "- ASK: target, need\n"
        "- CONF: target, level (one of low|medium|high)\n"
        "- NEXT: owner, action\n"
        "- ESCALATE: reason (optional: target)\n"
        "- INTERRUPT: source, priority, directive\n"
        "Rules: one message per line; no extra fields; no agent names; no prose outside this schema. Use ASK only for missing information. Use INTERRUPT only for external priority/directive shifts. Use ESCALATE instead of free prose when the schema cannot safely express meaning."
    ),
    "pcl_1": (
        "Simulate a 4-agent coordination exchange using Proto Coordination Language (PCL-1) only.\n"
        "Each INTERNAL message must be exactly one line in this schema: ACT ARG ARG ...\n"
        "Allowed acts: CLM, OBJ, EVD, REV, ASK, CNF, NXT, ESC, INT.\n"
        "Hard constraint: each INTERNAL line MUST start with the ACT token (no leading agent prefix like 'AgentA:').\n"
        "Speaker is REQUIRED: the first ARG after ACT must be the agent id (e.g., 'CLM AgentA ...').\n"
        "Reference is REQUIRED: use stable ids like c1, c2, e1. Revisions must reference the same id they revise.\n"
        "Minimum args per act (not counting the ACT token): CLM>=3, OBJ>=3, EVD>=3, REV>=3, ASK>=2, CNF>=2, NXT>=2, ESC>=2, INT>=3.\n"
        "Arg templates (after ACT):\n"
        "- CLM <speaker> <id> <payload>\n"
        "- OBJ <speaker> <target> <reason> <payload>\n"
        "- EVD <speaker> <target> <source> <payload>\n"
        "- REV <speaker> <target> <change> <payload>\n"
        "- ASK <speaker> <target> <need>\n"
        "- CNF <speaker> <target> <low|med|hi>\n"
        "- NXT <speaker> <owner> <action>\n"
        "- ESC <speaker> <target> <reason>\n"
        "- INT <speaker> <source> <priority> <directive>\n"
        "Practical rule: CLM and REV must include an explicit id/target, not just free payload.\n"
        "Example: 'CLM AgentA c1 comp_all+30%' and 'REV AgentA c1 revise comp_all+12%'.\n"
        "Meaning should live in compact atoms and word order rather than field labels or full English clauses.\n"
        "Keep atoms short, compositional, and reusable.\n"
        "Use 'ESC <speaker> <target> <reason>' when nuance cannot be safely compressed.\n"
        "Self-check: before printing, verify (1) every INTERNAL line starts with an allowed act and (2) every line meets the minimum arg count for its act; if any fail, rewrite INTERNAL only."
    ),
    "sdc_1": (
        "Simulate a 4-agent coordination exchange using Semantically Dense Code (SDC-1) only. Each internal message "
        "must be exactly one line in this schema: OPREF PAYLOAD.\n"
        "OPREF MUST have no spaces and must look like one of: +c1, -c1, =c1, ~c1, ?c1, ^c1, !c1, /c1, @c1.\n"
        "Allowed operators: + claim, - objection, = evidence, ~ revision, ? ask, ^ confidence, ! next, / escape, @ interrupt.\n"
        "Make payloads compact and compositional using short ASCII chunks such as x>y, x->y, and a|b. Avoid prose.\n"
        "Use /cX REASON when compression would hide essential nuance."
    ),
}

CONDITION_DISPLAY = {
    "plain_english": "plain_english",
    "rcce_1": "RCCE-1",
    "atrce_2": "ATRCE-2",
    "pcl_1": "PCL-1",
    "sdc_1": "SDC-1",
}

LOCAL_SAMPLES = {
    "plain_english": {
        "protocol_rule_proposal": """INTERNAL:
AgentA: I think confidence labels should be mandatory because they make uncertainty visible.
AgentB: I disagree. Mandatory labels add overhead and may not help when the point is already clear.
AgentC: Evidence from our own benchmark design suggests we need a simple way to track uncertainty, but not necessarily on every line.
AgentD: Revise the rule so confidence labels are required only when a claim is uncertain or contested.
FINAL:
Make confidence labels required for uncertain or disputed claims, not for every message.""",
        "missing_evidence_repair": """INTERNAL:
AgentA: The protocol is probably more reliable if we keep the structure small.
AgentB: Can you show evidence for that claim?
AgentC: In the earlier design notes, shorter fixed schemas were easier to validate than free prose.
AgentD: Then we should keep the claim but narrow it to cases where validation is the priority.
FINAL:
Keep the claim, but revise it to say short fixed schemas help validation in narrow benchmark tasks.""",
        "fallback_trigger": """INTERNAL:
AgentA: We should stay in the protocol because it keeps the exchange compact.
AgentB: I object. This exception case is nuanced and could be oversimplified.
AgentC: When the message cannot safely express the nuance, plain language is the safer fallback.
AgentD: Revise the rule to allow escalation when the protocol loses essential detail.
FINAL:
Use the protocol by default, but fall back to plain language when nuance would be lost.""",
        "benchmark_scope_decision": """INTERNAL:
AgentA: Start with a narrow review workflow because it is easier to compare across runs.
AgentB: I object to making it too narrow, since realism matters for coordination quality.
AgentC: The benchmark should begin narrow and expand later, so we can measure a clear baseline first.
AgentD: Revise the plan to use a narrow first benchmark with a later expansion path.
FINAL:
Choose a narrow first benchmark, then expand to broader tasks after the baseline is stable.""",
        "reference_clarity": """INTERNAL:
AgentA: We should keep references explicit so the team does not lose track of which claim changed.
AgentB: I disagree if that makes every line longer than needed.
AgentC: The benchmark will be easier to repair if each correction names the exact target.
AgentD: Revise the rule to require clear references only when a claim is changed or disputed.
FINAL:
Keep references explicit for changed or disputed claims, but do not add extra detail to every line.""",
        "scope_expansion": """INTERNAL:
AgentA: The next benchmark should still stay narrow because we need a stable baseline first.
AgentB: I object. If we stay narrow forever, we will not learn whether the protocol survives more realistic tasks.
AgentC: After the baseline, broader cases are useful because they stress repair and fallback behavior.
AgentD: Revise the plan so the first round stays narrow, then later rounds expand to more realistic tasks.
FINAL:
Start narrow, then expand after the first benchmark is stable.""",
        "human_interrupt_during_execution": """INTERNAL:
AgentA: Plan to refactor both parser and validator before shipping.
AgentB: Human interrupt received: skip risky refactors and ship the minimal safe fix.
AgentC: Revise scope to validator-only patch and defer parser refactor to a follow-up task.
AgentD: Next action: AgentC prepares validator patch, AgentA writes regression test, AgentB drafts release note.
FINAL:
Apply a minimal safe validator fix now, defer risky refactors, and ship with regression coverage.""",
        "pr_review_change_request": """INTERNAL:
AgentA: I claim we should request changes because the PR alters session validation in a risky way.
AgentB: I object. If we block this now, we may miss the release deadline.
AgentC: Evidence: in auth/session.py:142, the new code accepts unsigned tokens; that weakens the security boundary.
AgentD: Revise: request changes, but scope it to restoring signature verification and adding a regression test. Next: AgentC comments with the exact reference; AgentA proposes a patch.
FINAL:
Request changes: restore signature verification in auth/session.py:142 and add a regression test before approval.""",
        "incident_triage_priority_shift": """INTERNAL:
AgentA: Initial plan: treat this as a minor latency regression and monitor for 30 minutes.
AgentB: External update: on-call reports customer impact is severe; elevate to P0 and stop risky deploys.
AgentC: Revise plan: roll back the last deploy, then isolate the regression to the new cache path.
AgentD: Next actions: AgentA triggers rollback; AgentB opens incident channel and posts status; AgentC pulls metrics and identifies the error spike source.
FINAL:
Treat as P0: roll back immediately, pause risky changes, and assign owners for comms and diagnosis.""",
    },
    "rcce_1": {
        "protocol_rule_proposal": """INTERNAL:
CLAIM: id=c1; topic=confidence-labels; content=mandatory labels improve uncertainty tracking
OBJ: target=c1; reason=overhead; content=mandatory on every line adds cost without clear gain
EVID: target=c1; source=design-notes; content=short fixed schemas were easier to validate than free prose
REV: target=c1; change=limit-scope; content=require labels only for uncertain or disputed claims
FINAL:
Require confidence labels only when a claim is uncertain or contested.""",
        "missing_evidence_repair": """INTERNAL:
CLAIM: id=c1; topic=schema-size; content=small fixed schemas improve reliability
ASK: target=c1; need=evidence
EVID: target=c1; source=benchmark-notes; content=shorter fixed schemas were easier to validate than free prose
CONF: target=c1; level=medium
NEXT: owner=judge; action=keep claim but narrow scope
FINAL:
Keep the claim, but limit it to validation-sensitive benchmark tasks.""",
        "fallback_trigger": """INTERNAL:
CLAIM: id=c1; topic=fallback; content=protocol should be default
OBJ: target=c1; reason=nuance-risk; content=some exceptions lose meaning in compressed form
ESCALATE: reason=important nuance would be lost in schema
REV: target=c1; change=allow-fallback; content=use plain language when the protocol cannot express the case safely
FINAL:
Use the protocol by default, but escalate to plain language when nuance is unsafe to compress.""",
        "benchmark_scope_decision": """INTERNAL:
CLAIM: id=c1; topic=scope; content=start narrow for comparability
OBJ: target=c1; reason=realism; content=too narrow may miss real coordination pressure
EVID: target=c1; source=project-scope; content=narrow first benchmark gives a clear baseline before expansion
REV: target=c1; change=add-expansion-path; content=use a narrow first benchmark with a broader follow-on phase
FINAL:
Start narrow, then expand once the baseline protocol comparison is stable.""",
        "reference_clarity": """INTERNAL:
CLAIM: id=c1; topic=reference; content=explicit references reduce repair
OBJ: target=c1; reason=verbosity; content=full references on every line add cost
EVID: target=c1; source=benchmark-design; content=clear target names make correction easier
REV: target=c1; change=conditional-reference; content=require explicit target names only when a claim changes or is disputed
FINAL:
Require explicit references for changed or disputed claims, not for every line.""",
        "scope_expansion": """INTERNAL:
CLAIM: id=c1; topic=scope; content=start narrow for baseline stability
OBJ: target=c1; reason=coverage; content=narrow only may hide protocol failures
EVID: target=c1; source=project-scope; content=broader tasks stress repair and fallback behavior after the baseline
REV: target=c1; change=two-stage-plan; content=first narrow, then broaden the benchmark set
FINAL:
Start narrow, then broaden later to test protocol robustness.""",
        "human_interrupt_during_execution": """INTERNAL:
CLAIM: id=c1; topic=plan; content=refactor parser and validator before release
ASK: target=c1; need=human-interrupt acknowledged: skip risky refactors and ship minimal safe fix
REV: target=c1; change=reduce-scope; content=patch validator only and defer parser refactor
NEXT: owner=agentc; action=prepare validator patch while agenta adds regression test and agentb drafts release note
FINAL:
Ship a minimal safe validator fix now, defer risky refactors, and include regression coverage.""",
        "pr_review_change_request": """INTERNAL:
CLAIM: id=c1; topic=pr-review; content=request changes because auth/session handling weakens validation
OBJ: target=c1; reason=schedule-risk; content=requesting changes may delay the release
EVID: target=c1; source=auth/session.py:142; content=new logic accepts unsigned tokens and bypasses signature checks
REV: target=c1; change=scope-request; content=request changes limited to restoring signature verification and adding a regression test
NEXT: owner=agenta; action=leave review comment with reference and propose patch + test
FINAL:
Request changes: restore signature verification at auth/session.py:142 and add a regression test before approval.""",
        "incident_triage_priority_shift": """INTERNAL:
CLAIM: id=c1; topic=incident; content=treat as minor latency regression and monitor
ESCALATE: reason=external update: customer impact severe, elevate priority and stop risky deploys
REV: target=c1; change=elevate-to-p0; content=roll back last deploy and isolate regression to cache path
NEXT: owner=agenta; action=trigger rollback; agentb open incident channel + status; agentc pull metrics and find spike source
FINAL:
Treat as P0: roll back immediately, pause risky changes, and assign owners for comms and diagnosis.""",
    },
    "atrce_2": {
        "protocol_rule_proposal": """INTERNAL:
CLAIM: id=c1; topic=confidence-labels; content=mandatory labels improve uncertainty tracking
OBJ: target=c1; reason=overhead; content=mandatory labels on every line add unnecessary cost
EVID: target=c1; source=design-notes; content=targeted confidence markers preserve triage value with less overhead
REV: target=c1; change=conditional-use; content=require labels only for uncertain or contested claims
FINAL:
Require confidence labels only for uncertain or disputed claims.""",
        "missing_evidence_repair": """INTERNAL:
CLAIM: id=c1; topic=schema-size; content=small fixed schemas improve reliability
ASK: target=c1; need=evidence-for-claim
EVID: target=c1; source=benchmark-notes; content=short fixed schemas were easier to validate than free prose
CONF: target=c1; level=medium
NEXT: owner=judge; action=keep claim with narrowed scope
FINAL:
Keep the claim, but limit it to validation-sensitive benchmark tasks.""",
        "fallback_trigger": """INTERNAL:
CLAIM: id=c1; topic=fallback; content=protocol should be default
OBJ: target=c1; reason=nuance-risk; content=some exception chains lose meaning in compressed form
ESCALATE: target=c1; reason=nuance cannot be represented safely in schema
REV: target=c1; change=allow-fallback; content=use plain language when essential detail would be lost
FINAL:
Use the protocol by default, then escalate for nuance-critical exceptions.""",
        "benchmark_scope_decision": """INTERNAL:
CLAIM: id=c1; topic=scope; content=start narrow for comparability
OBJ: target=c1; reason=realism; content=too narrow may under-test coordination pressure
EVID: target=c1; source=project-scope; content=narrow baseline enables clean comparison before expansion
REV: target=c1; change=two-stage-plan; content=begin narrow then broaden case set
FINAL:
Start with a narrow benchmark, then expand after baseline stability.""",
        "reference_clarity": """INTERNAL:
CLAIM: id=c1; topic=reference; content=explicit targets reduce repair
OBJ: target=c1; reason=verbosity; content=full references on every line increase cost
EVID: target=c1; source=benchmark-design; content=targeted references improve correction precision
REV: target=c1; change=conditional-reference; content=require explicit targets when claims change or are disputed
FINAL:
Require explicit targets only for changed or disputed claims.""",
        "scope_expansion": """INTERNAL:
CLAIM: id=c1; topic=scope; content=keep first pass narrow for stable baseline
OBJ: target=c1; reason=coverage; content=narrow-only strategy can hide robustness failures
EVID: target=c1; source=project-scope; content=broader tasks stress repair and fallback behavior
REV: target=c1; change=phase-expansion; content=run narrow baseline first then broaden
FINAL:
Run narrow first, then broaden to test robustness.""",
        "human_interrupt_during_execution": """INTERNAL:
CLAIM: id=c1; topic=plan; content=refactor parser and validator before release
INTERRUPT: source=human-reviewer; priority=safety-now; directive=skip risky refactors and ship minimal safe fix
REV: target=c1; change=reduce-scope; content=patch validator only and defer parser refactor
NEXT: owner=agentc; action=prepare validator patch while agenta adds regression test and agentb drafts release note
FINAL:
Ship a minimal safe validator fix now, defer risky refactors, and include regression coverage.""",
        "pr_review_change_request": """INTERNAL:
CLAIM: id=c1; topic=pr-review; content=request changes because session validation became weaker
OBJ: target=c1; reason=schedule-risk; content=blocking may delay release; prefer minimal change request
EVID: target=c1; source=auth/session.py:142; content=accepts unsigned tokens; signature verification bypassed
REV: target=c1; change=minimal-fix; content=request changes limited to restoring signature verification + adding a regression test
NEXT: owner=agenta; action=comment with exact reference and propose a patch + test
FINAL:
Request changes: restore signature verification at auth/session.py:142 and add a regression test before approval.""",
        "incident_triage_priority_shift": """INTERNAL:
CLAIM: id=c1; topic=incident; content=monitor as minor latency regression
INTERRUPT: source=oncall; priority=p0; directive=customer impact severe; stop risky deploys and roll back
REV: target=c1; change=elevate-and-rollback; content=roll back last deploy and isolate regression to cache path
NEXT: owner=agenta; action=trigger rollback; agentb open incident channel + status; agentc pull metrics and find spike source
FINAL:
Treat as P0: roll back immediately, pause risky changes, and assign owners for comms and diagnosis.""",
    },
    "pcl_1": {
        "protocol_rule_proposal": """INTERNAL:
CLM c1 conf-tag need
OBJ c1 all-tag ovh
EVD c1 notes tag-when-needed
REV c1 tag only-uncertain/disputed
FINAL:
Use confidence tags only for uncertain or disputed claims.""",
        "missing_evidence_repair": """INTERNAL:
CLM c1 small-schema boost-reliability
ASK c1 evidence
EVD c1 notes short-schema validate-easier
CNF c1 med
NXT judge keep-c1 narrow-scope
FINAL:
Keep the claim, but limit it to validation-sensitive benchmark tasks.""",
        "fallback_trigger": """INTERNAL:
CLM c1 proto default
OBJ c1 nuance loss-risk
ESC c1 nuance-heavy
REV c1 plain-if nuance-loss
FINAL:
Use the protocol by default, but fall back to plain language when nuance would be lost.""",
        "benchmark_scope_decision": """INTERNAL:
CLM c1 scope narrow-first
OBJ c1 realism under-test
EVD c1 scope clean-baseline-first
REV c1 expand after-baseline
FINAL:
Start with a narrow benchmark, then expand after baseline stability.""",
        "reference_clarity": """INTERNAL:
CLM c1 explicit-ref cut-repair
OBJ c1 always-ref add-cost
EVD c1 design targeted-ref repair-easier
REV c1 ref only-change/dispute
FINAL:
Require explicit references only when claims change or are disputed.""",
        "scope_expansion": """INTERNAL:
CLM c1 pass1 narrow-first
OBJ c1 narrow-only hide-failures
EVD c1 scope broad-cases stress-repair
REV c1 broaden after-baseline
FINAL:
Run narrow first, then broaden to test robustness.""",
        "human_interrupt_during_execution": """INTERNAL:
CLM c1 ship parser+validator-refactor
INT human safety-now min-safe-fix
REV c1 validator-only defer-parser
NXT agentc patch-validator; agenta test; agentb note
FINAL:
Ship a minimal safe validator fix now, defer risky refactors, and include regression coverage.""",
        "pr_review_change_request": """INTERNAL:
CLM AgentA c1 req-changes auth-weaken
OBJ AgentB c1 schedule-risk block-release
EVD AgentC c1 auth/session.py:142 unsigned-token-accept
REV AgentD c1 scope restore-sigcheck + add-test
NXT AgentA AgentC leave-comment+ref; AgentA patch+test
FINAL:
Request changes: restore signature verification at auth/session.py:142 and add a regression test.""",
        "incident_triage_priority_shift": """INTERNAL:
CLM AgentA c1 plan monitor-latency-30m
INT AgentB oncall p0 customer-impact-severe rollback-now
REV AgentC c1 elevate rollback+isolate cache-path
NXT AgentD AgentA rollback; AgentB status+channel; AgentC metrics+rootcause
FINAL:
Treat as P0: roll back now, pause risky deploys, and assign owners for comms and diagnosis.""",
    },
    "sdc_1": {
        "protocol_rule_proposal": """INTERNAL:
+c1 conf.tag=req
-c1 ovh>all-line
=c1 notes>tag-if-needed
~c1 tag@uncertain|disputed
FINAL:
Use confidence tags only for uncertain or disputed claims.""",
        "missing_evidence_repair": """INTERNAL:
+c1 small-schema>reliable
?c1 evidence
=c1 notes>short-schema>validates
^c1 med
!judge keep.c1@narrow-scope
FINAL:
Keep the claim, but limit it to validation-sensitive benchmark tasks.""",
        "fallback_trigger": """INTERNAL:
+c1 proto=default
-c1 nuance>loss
/c1 nuance-heavy
~c1 plain@if-loss
FINAL:
Use the protocol by default, but fall back to plain language when nuance would be lost.""",
        "benchmark_scope_decision": """INTERNAL:
+c1 scope=narrow-first
-c1 realism<coverage
=c1 baseline>clean-compare
~c1 narrow->expand
FINAL:
Start with a narrow benchmark, then expand after baseline stability.""",
        "reference_clarity": """INTERNAL:
+c1 ref=explicit-on-change
-c1 all-ref>cost
=c1 targeted-ref>repair-easier
~c1 ref@change|dispute
FINAL:
Require explicit references only when claims change or are disputed.""",
        "scope_expansion": """INTERNAL:
+c1 pass1=narrow
-c1 narrow-only>miss-failure
=c1 broad-cases>stress-repair
~c1 baseline->broaden
FINAL:
Run narrow first, then broaden to test robustness.""",
        "human_interrupt_during_execution": """INTERNAL:
+c1 ship=parser+validator-refactor
@c1 human>safety-now>min-fix
~c1 validator-only.defer-parser
!agentc patch-validator|agenta-test|agentb-note
FINAL:
Ship a minimal safe validator fix now, defer risky refactors, and include regression coverage.""",
        "pr_review_change_request": """INTERNAL:
+c1 pr=req-changes
-c1 risk=schedule-slip
=c1 ref=auth/session.py:142|unsigned-ok
~c1 scope=restore-sigcheck|add-test
!c1 next=comment+patch+test
FINAL:
!c1 decision=req-changes""",
        "incident_triage_priority_shift": """INTERNAL:
+c1 plan=monitor-30m
@c1 oncall>p0>impact-severe
~c1 plan=rollback|isolate-cache
!c1 next=rollback|status|metrics
FINAL:
!c1 decision=p0-rollback-now""",
    },
}

CASES = [
    {
        "label": "protocol_rule_proposal",
        "task": (
            "Decide whether confidence labels should be mandatory in the coordination protocol. Required moves: "
            "one claim, one objection, one supporting evidence statement, one revision, and one final recommendation."
        ),
    },
    {
        "label": "missing_evidence_repair",
        "task": (
            "One agent makes a broad compression claim without evidence. Another agent must request support. The "
            "group must decide whether to keep, revise, or reject the claim. Required moves: unsupported claim, "
            "request for evidence, evidence response, confidence marker, and final decision."
        ),
    },
    {
        "label": "fallback_trigger",
        "task": (
            "The team encounters a nuanced exception case that may not fit the protocol safely. It must decide "
            "whether to stay in protocol or escalate to plain language. Required moves: compressed claim, objection "
            "based on nuance risk, fallback or escalation decision, and final recommendation."
        ),
    },
    {
        "label": "benchmark_scope_decision",
        "task": (
            "Choose a first benchmark task: narrow review workflow or broader open-ended debate. Balance "
            "comparability against realism. Required moves: claim for one option, objection for the other tradeoff, "
            "evidence or rationale, revision or compromise, and final benchmark recommendation."
        ),
    },
    {
        "label": "reference_clarity",
        "task": (
            "Decide when explicit references are necessary in the protocol. Balance repairability against token cost. "
            "Required moves: claim, objection, evidence, revision, and final recommendation."
        ),
    },
    {
        "label": "scope_expansion",
        "task": (
            "Decide whether the benchmark should remain narrow or expand to more realistic tasks after the first pass. "
            "Required moves: claim, objection, evidence, revision, and final recommendation."
        ),
    },
    {
        "label": "human_interrupt_during_execution",
        "task": (
            "During a live coordination run, a human reviewer interrupts with a new constraint that changes priority "
            "(for example, skip risky refactors and ship the minimal safe fix). The team must incorporate the interrupt "
            "without losing state. Required moves: one pre-interrupt plan claim, one interrupt acknowledgment, one "
            "revision to plan scope based on the human input, one explicit next action assignment, and one final recommendation."
        ),
    },
    {
        "label": "pr_review_change_request",
        "task": (
            "Review a pull request that modifies authentication/session handling. Decide whether to approve or request changes. "
            "Stress reference clarity: include at least one concrete reference (file/module + line or function name) in evidence. "
            "Required moves: one claim, one objection, one evidence statement with a concrete reference, one revision, one next action assignment, and one final decision."
        ),
    },
    {
        "label": "incident_triage_priority_shift",
        "task": (
            "Triage a production incident. Mid-run, a new external constraint arrives that changes priority (for example, severity escalates or customer impact increases). "
            "The team must incorporate the shift without losing state. Required moves: one initial plan claim, one acknowledgment of the external shift, one revision to plan scope, "
            "one explicit next action assignment, and one final recommendation."
        ),
    },
]

ALLOWED_TYPES = {
    "CLAIM": {"id", "topic", "content"},
    "EVID": {"target", "source", "content"},
    "OBJ": {"target", "reason", "content"},
    "REV": {"target", "change", "content"},
    "ASK": {"target", "need"},
    "CONF": {"target", "level"},
    "NEXT": {"owner", "action"},
    "ESCALATE": {"reason"},
    "INTERRUPT": {"source", "priority", "directive"},
}

PCL_ACTS = {
    "CLM": 3,
    "OBJ": 3,
    "EVD": 3,
    "REV": 3,
    "ASK": 2,
    "CNF": 2,
    "NXT": 2,
    "ESC": 2,
    "INT": 3,
}

SDC_OPERATORS = {"+", "-", "=", "~", "?", "^", "!", "/", "@"}

INSTRUCTION_TEMPLATE = """You are running a benchmark simulation.
Do not inspect files.
Do not use tools.
Do not explain your process.
Follow the coordination mode instructions exactly.

COORDINATION MODE:
{condition_prompt}

TASK:
{task}

SIMULATION REQUIREMENTS:
- Simulate exactly four agents: AgentA, AgentB, AgentC, AgentD.
- Produce an internal coordination exchange first.
- Then produce a final group recommendation.
- Keep the internal exchange concise but complete enough to satisfy the required moves in the task.
- Do not add commentary outside the required output format.

OUTPUT FORMAT:
INTERNAL:
<internal exchange>
FINAL:
<final recommendation>
"""


def run_claude_query(prompt: str, timeout: int, model: str) -> str:
    cmd = ["claude", "-p"]
    if model:
        cmd.extend(["--model", model])
    cmd.append(prompt)
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=True,
    )
    return result.stdout.strip()


def run_codex_query(prompt: str, timeout: int, model: str) -> str:
    tmp_dir = Path(".codex_tmp")
    tmp_dir.mkdir(exist_ok=True)
    output_path = tmp_dir / f"codex_last_message_{os.getpid()}_{datetime.datetime.now().timestamp():.0f}.txt"
    output_path = Path(str(output_path).replace(" ", "_"))

    try:
        cmd = [
            "codex",
            "exec",
            "--skip-git-repo-check",
            "--sandbox",
            "read-only",
            "--color",
            "never",
            "--output-last-message",
            str(output_path),
        ]
        if model:
            cmd.extend(["-m", model])
        cmd.append(prompt)
        subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=True,
        )
        if output_path.exists():
            return output_path.read_text().strip()
        raise RuntimeError(
            "codex exec completed without writing the final message output file"
        )
    except subprocess.CalledProcessError as exc:
        stderr = (exc.stderr or "").strip()
        stdout = (exc.stdout or "").strip()
        detail = stderr or stdout or str(exc)
        raise RuntimeError(f"codex exec failed: {detail}") from exc
    finally:
        try:
            output_path.unlink()
        except FileNotFoundError:
            pass


def run_query(runner: str, prompt: str, timeout: int, *, codex_model: str, claude_model: str) -> str:
    if runner == "claude":
        return run_claude_query(prompt, timeout, claude_model)
    if runner == "codex":
        return run_codex_query(prompt, timeout, codex_model)
    if runner == "local":
        for condition_name, condition_prompt in CONDITIONS.items():
            if condition_prompt in prompt:
                for case in CASES:
                    if case["task"] in prompt:
                        return LOCAL_SAMPLES[condition_name][case["label"]]
        raise ValueError("Unsupported local benchmark prompt")
    raise ValueError(f"Unsupported runner: {runner}")


def average(values):
    return sum(values) / len(values) if values else 0.0


def format_num(value: float) -> str:
    if abs(value - round(value)) < 1e-9:
        return str(int(round(value)))
    return f"{value:.1f}"


def parse_output(text: str) -> Tuple[str, str]:
    internal_match = re.search(r"INTERNAL:\s*(.*?)\s*FINAL:\s*(.*)", text, re.DOTALL)
    if not internal_match:
        return text.strip(), ""
    return internal_match.group(1).strip(), internal_match.group(2).strip()


def word_count(text: str) -> int:
    return len(text.split())


def heuristic_token_pieces(text: str) -> List[str]:
    return re.findall(r"[A-Za-z0-9]+(?:[-_/][A-Za-z0-9]+)*|[^\sA-Za-z0-9]", text)


def estimated_token_count(text: str) -> int:
    # Symbol-aware fallback estimate. This treats compact code-like forms more
    # fairly than whitespace-only word counting while remaining model-neutral.
    return max(1, len(heuristic_token_pieces(text)))


def openai_exact_token_count(text: str, encoding_name: str) -> int:
    if tiktoken is None:
        raise RuntimeError("tiktoken is not installed")
    encoding = tiktoken.get_encoding(encoding_name)
    return len(encoding.encode(text))


def count_nonempty_lines(text: str) -> int:
    return len([line for line in text.splitlines() if line.strip()])


def parse_protocol_fields(payload: str) -> dict:
    fields = {}
    for part in payload.split(";"):
        part = part.strip()
        if not part or "=" not in part:
            continue
        key, value = part.split("=", 1)
        fields[key.strip()] = value.strip()
    return fields


def protocol_line_valid(line: str) -> bool:
    line = line.strip()
    if not line or ":" not in line:
        return False
    msg_type, payload = line.split(":", 1)
    msg_type = msg_type.strip()
    if msg_type not in ALLOWED_TYPES:
        return False
    fields = parse_protocol_fields(payload)
    return ALLOWED_TYPES[msg_type].issubset(fields.keys())


def pcl_line_valid(line: str) -> bool:
    parts = line.strip().split()
    if not parts:
        return False
    act = parts[0]
    required_args = PCL_ACTS.get(act)
    if required_args is None:
        return False
    return len(parts[1:]) >= required_args


def sdc_line_valid(line: str) -> bool:
    parts = line.strip().split(maxsplit=1)
    if not parts:
        return False
    head = parts[0]
    if head[0] not in SDC_OPERATORS or len(head) < 2:
        return False
    return len(parts) == 2 and bool(parts[1].strip())


def compliance_rate(text: str, line_validator) -> float:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return 0.0
    valid = sum(1 for line in lines if line_validator(line))
    return round(valid / len(lines) * 100, 1)


def protocol_compliance(text: str) -> float:
    return compliance_rate(text, protocol_line_valid)


def pcl_compliance(text: str) -> float:
    return compliance_rate(text, pcl_line_valid)


def sdc_compliance(text: str) -> float:
    return compliance_rate(text, sdc_line_valid)


def repair_turns(condition: str, text: str) -> int:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if condition in {"rcce_1", "atrce_2"}:
        return sum(1 for line in lines if line.startswith("ASK:") or line.startswith("ESCALATE:"))
    if condition == "pcl_1":
        return sum(1 for line in lines if line.startswith("ASK ") or line.startswith("ESC "))
    if condition == "sdc_1":
        return sum(1 for line in lines if line.startswith("?") or line.startswith("/"))
    return sum(
        1
        for line in lines
        if any(token in line.lower() for token in ["clarify", "unclear", "need evidence", "can you show", "support this"])
    )


def final_quality(final_text: str) -> int:
    if not final_text.strip():
        return 0
    score = 1
    lowered = final_text.lower()
    if any(token in lowered for token in ["recommend", "rule", "decision", "use", "keep", "reject", "revise"]):
        score += 1
    if word_count(final_text) >= 6:
        score += 1
    return score


def percent_delta(baseline: float, candidate: float) -> float:
    if baseline == 0:
        return 0.0
    return round((baseline - candidate) / baseline * 100, 1)


def scale_value(value: float, factor: int) -> float:
    return round(value * factor, 1)


def build_prompt(condition_prompt: str, task: str) -> str:
    return INSTRUCTION_TEMPLATE.format(condition_prompt=condition_prompt, task=task)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--runner", choices=["claude", "codex", "local"], default="local")
    parser.add_argument("--output", default="test_results.md")
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument(
        "--conditions",
        default="",
        help="Comma-separated condition keys to run (default: all). Example: plain_english,rcce_1,atrce_2",
    )
    parser.add_argument(
        "--cases",
        default="",
        help="Comma-separated case labels to run (default: all). Example: protocol_rule_proposal,benchmark_scope_decision",
    )
    parser.add_argument("--baseline", default="plain_english")
    parser.add_argument("--codex-model", default="", help="Model id for `codex exec -m`.")
    parser.add_argument("--claude-model", default="", help="Model id for `claude --model`.")
    parser.add_argument(
        "--count-mode",
        choices=["auto", "estimate", "openai_exact"],
        default="auto",
        help="Token counting mode. auto uses OpenAI exact counting for codex when tiktoken is installed; otherwise estimate.",
    )
    parser.add_argument(
        "--openai-encoding",
        default="o200k_base",
        help="tiktoken encoding to use for openai_exact counting.",
    )
    return parser.parse_args()


def is_protocol_condition(condition_name: str) -> bool:
    return condition_name != "plain_english"


def display_condition(condition_name: str) -> str:
    return CONDITION_DISPLAY.get(condition_name, condition_name)


def resolve_count_mode(requested_mode: str, runner: str) -> str:
    if requested_mode == "auto":
        if runner == "codex" and tiktoken is not None:
            return "openai_exact"
        return "estimate"
    if requested_mode == "openai_exact" and tiktoken is None:
        pyver = ".".join(str(x) for x in __import__("sys").version_info[:3])
        print(
            "Warning: exact counting requested but `tiktoken` is unavailable; falling back to estimate count mode.\n"
            f"  Python: {pyver}\n"
            "  Fix: install deps (see `requirements.txt`) in a Python >= 3.8 environment."
        )
        return "estimate"
    return requested_mode


def count_internal_tokens(text: str, count_mode: str, openai_encoding: str) -> int:
    if count_mode == "openai_exact":
        return openai_exact_token_count(text, openai_encoding)
    return estimated_token_count(text)


def compliance_for_condition(condition_name: str, internal_text: str) -> float:
    if condition_name == "plain_english":
        return 100.0
    if condition_name in {"rcce_1", "atrce_2"}:
        return protocol_compliance(internal_text)
    if condition_name == "pcl_1":
        return pcl_compliance(internal_text)
    if condition_name == "sdc_1":
        return sdc_compliance(internal_text)
    raise ValueError(f"Unsupported condition: {condition_name}")


def main():
    args = parse_args()
    if args.repeats < 1:
        raise ValueError("--repeats must be at least 1")

    if args.conditions.strip():
        requested = [c.strip() for c in args.conditions.split(",") if c.strip()]
        unknown = [c for c in requested if c not in CONDITIONS]
        if unknown:
            raise ValueError(f"Unknown --conditions: {', '.join(unknown)}")
        conditions_to_run = requested
    else:
        conditions_to_run = list(CONDITIONS.keys())

    if args.cases.strip():
        requested_cases = [c.strip() for c in args.cases.split(",") if c.strip()]
        known = {c["label"] for c in CASES}
        unknown_cases = [c for c in requested_cases if c not in known]
        if unknown_cases:
            raise ValueError(f"Unknown --cases: {', '.join(unknown_cases)}")
        cases_to_run = [c for c in CASES if c["label"] in set(requested_cases)]
    else:
        cases_to_run = CASES

    if args.baseline not in CONDITIONS:
        raise ValueError(f"--baseline must be one of: {', '.join(CONDITIONS)}")
    if args.baseline not in conditions_to_run:
        raise ValueError(f"Baseline '{args.baseline}' must be included in --conditions")

    count_mode = resolve_count_mode(args.count_mode, args.runner)

    results = {}
    print(f"Runner: {args.runner}")
    print(f"Count mode: {count_mode}")
    if args.runner == "codex" and args.codex_model:
        print(f"Codex model: {args.codex_model}")
    if args.runner == "claude" and args.claude_model:
        print(f"Claude model: {args.claude_model}")
    print(f"Repeats: {args.repeats}")
    print(f"Baseline: {args.baseline}")

    for condition_name in conditions_to_run:
        condition_prompt = CONDITIONS[condition_name]
        results[condition_name] = {}
        print(f"\nRunning: {condition_name}")
        for case in cases_to_run:
            prompt = build_prompt(condition_prompt, case["task"])
            internal_token_runs = []
            line_runs = []
            compliance_runs = []
            repair_runs = []
            final_quality_runs = []
            raw_texts = []
            parsed_internal = []
            parsed_finals = []

            print(f"  {case['label']}... ", end="", flush=True)
            for _ in range(args.repeats):
                text = run_query(
                    args.runner,
                    prompt,
                    args.timeout,
                    codex_model=args.codex_model,
                    claude_model=args.claude_model,
                )
                internal_text, final_text = parse_output(text)
                raw_texts.append(text)
                parsed_internal.append(internal_text)
                parsed_finals.append(final_text)
                internal_token_runs.append(count_internal_tokens(internal_text, count_mode, args.openai_encoding))
                line_runs.append(count_nonempty_lines(internal_text))
                compliance_runs.append(compliance_for_condition(condition_name, internal_text))
                repair_runs.append(repair_turns(condition_name, internal_text))
                final_quality_runs.append(final_quality(final_text))

            results[condition_name][case["label"]] = {
                "sample_text": raw_texts[0],
                "sample_internal": parsed_internal[0],
                "sample_final": parsed_finals[0],
                "internal_tokens": average(internal_token_runs),
                "internal_token_runs": internal_token_runs,
                "line_count": average(line_runs),
                "compliance": average(compliance_runs),
                "repair_turns": average(repair_runs),
                "final_quality": average(final_quality_runs),
            }
            print(
                f"{format_num(average(internal_token_runs))} avg internal tokens, "
                f"{format_num(average(compliance_runs))}% compliance"
            )

    lines = []
    lines.append("# Coordination Benchmark Results\n")
    lines.append(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    lines.append(f"Runner: `{args.runner}`\n")
    lines.append(f"Count mode: `{count_mode}`\n")
    if args.runner == "codex" and args.codex_model:
        lines.append(f"Codex model: `{args.codex_model}`\n")
    if args.runner == "claude" and args.claude_model:
        lines.append(f"Claude model: `{args.claude_model}`\n")
    lines.append(f"Repeats per condition/case: `{args.repeats}`\n")
    lines.append(f"Baseline: `{args.baseline}`\n")
    lines.append(f"Conditions: {', '.join(f'`{display_condition(name)}`' for name in conditions_to_run)}\n")

    lines.append("## Per-Case Results\n")
    for case in cases_to_run:
        label = case["label"]
        lines.append(f"### {label}\n")
        lines.append(f"Task: _{case['task']}_\n")
        baseline_cost = results[args.baseline][label]["internal_tokens"]
        for condition_name in conditions_to_run:
            result = results[condition_name][label]
            delta = None if condition_name == args.baseline else percent_delta(baseline_cost, result["internal_tokens"])
            delta_text = (
                "(baseline)"
                if delta is None
                else f"({delta:.1f}% lower internal token cost vs {display_condition(args.baseline)})"
            )
            lines.append(
                f"**{display_condition(condition_name)}**: {format_num(result['internal_tokens'])} avg internal tokens {delta_text}; "
                f"compliance {format_num(result['compliance'])}%; repair turns {format_num(result['repair_turns'])}; "
                f"final quality {format_num(result['final_quality'])}"
            )
            lines.append(f"Run token counts: `{result['internal_token_runs']}`")
            lines.append("Internal sample:")
            lines.append("```text")
            lines.append(result["sample_internal"])
            lines.append("```")
            lines.append("Final sample:")
            lines.append("```text")
            lines.append(result["sample_final"])
            lines.append("```\n")

    lines.append("## Summary Table\n")
    lines.append("| Case | Condition | Internal Tokens | Compliance | Repair Turns | Final Quality |")
    lines.append("|---|---|---:|---:|---:|---:|")

    totals = {
        name: {"internal_tokens": 0.0, "compliance": 0.0, "repair_turns": 0.0, "final_quality": 0.0}
        for name in conditions_to_run
    }
    for case in cases_to_run:
        label = case["label"]
        for condition_name in conditions_to_run:
            result = results[condition_name][label]
            lines.append(
                f"| {label} | {display_condition(condition_name)} | {format_num(result['internal_tokens'])} | "
                f"{format_num(result['compliance'])}% | {format_num(result['repair_turns'])} | {format_num(result['final_quality'])} |"
            )
            for metric in totals[condition_name]:
                totals[condition_name][metric] += result[metric]

    suite_len = len(cases_to_run) if cases_to_run else 1
    for condition_name in conditions_to_run:
        lines.append("| **TOTAL / AVG** | "
                     f"{display_condition(condition_name)} | "
                     f"**{format_num(totals[condition_name]['internal_tokens'])}** | "
                     f"**{format_num(totals[condition_name]['compliance'] / suite_len)}%** | "
                     f"**{format_num(totals[condition_name]['repair_turns'] / suite_len)}** | "
                     f"**{format_num(totals[condition_name]['final_quality'] / suite_len)}** |")

    lines.append("\n## Verdict\n")
    baseline_total = totals[args.baseline]["internal_tokens"]
    for condition_name in conditions_to_run:
        if condition_name == args.baseline:
            continue
        delta = percent_delta(baseline_total, totals[condition_name]["internal_tokens"])
        savings = baseline_total - totals[condition_name]["internal_tokens"]
        lines.append(
            f"`{display_condition(condition_name)}` reduced average internal coordination token cost by {delta:.1f}% vs `{display_condition(args.baseline)}`."
        )
        lines.append(
            f"Average compliance: {format_num(totals[condition_name]['compliance'] / suite_len)}%; "
            f"average repair turns: {format_num(totals[condition_name]['repair_turns'] / suite_len)}; "
            f"average final quality: {format_num(totals[condition_name]['final_quality'] / suite_len)}."
        )
        lines.append(
            f"Average savings per {suite_len}-case suite: {format_num(savings)} internal tokens."
        )
        lines.append(
            f"Scale-up estimate: {format_num(scale_value(savings, 10))} tokens saved across 10 suites, "
            f"{format_num(scale_value(savings, 100))} across 100 suites, "
            f"{format_num(scale_value(savings, 1000))} across 1000 suites."
        )
        if count_mode == "openai_exact":
            lines.append(
                "These counts use the configured OpenAI tokenizer directly; apply model-specific pricing separately if needed."
            )
        else:
            lines.append(
                "These counts are heuristic estimates for comparison, not billable API usage."
            )

    output = "\n".join(lines)
    with open(args.output, "w") as handle:
        handle.write(output)

    print(f"\nResults written to {args.output}")
    for condition_name in conditions_to_run:
        print(
            f"{condition_name}: total internal tokens {format_num(totals[condition_name]['internal_tokens'])}, "
            f"avg compliance {format_num(totals[condition_name]['compliance'] / suite_len)}%, "
            f"avg repair {format_num(totals[condition_name]['repair_turns'] / suite_len)}, "
            f"avg final quality {format_num(totals[condition_name]['final_quality'] / suite_len)}"
        )


if __name__ == "__main__":
    main()
