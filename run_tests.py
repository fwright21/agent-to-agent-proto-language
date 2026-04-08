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
import re
import subprocess
import tempfile
from typing import Tuple
from pathlib import Path

CONDITIONS = {
    "plain_english": (
        "Simulate a 4-agent coordination exchange in concise plain English. Agents may be brief, but they "
        "should speak in normal readable prose. Avoid fluff, but do not use the compressed protocol schema."
    ),
    "rcce_1": (
        "Simulate a 4-agent coordination exchange using Relevance-Core Coordination English (RCCE-1) only. Each "
        "internal message must be exactly one line in this schema: TYPE: field=value; field=value. Allowed "
        "types: CLAIM, EVID, OBJ, REV, ASK, CONF, NEXT, ESCALATE. One message, one purpose. Use ESCALATE "
        "instead of free prose when the protocol cannot safely express a message."
    ),
    "atrce_2": (
        "Simulate a 4-agent coordination exchange using Act-Typed Relevance Coordination English (ATRCE-2) only. Each "
        "internal message must be exactly one line in this schema: TYPE: field=value; field=value. Allowed "
        "types: CLAIM, EVID, OBJ, REV, ASK, CONF, NEXT, ESCALATE, INTERRUPT. One message, one purpose. Use "
        "ASK only for missing information. Use INTERRUPT for external priority/directive shifts. Use ESCALATE "
        "instead of free prose when the protocol cannot safely express a message."
    ),
}

CONDITION_DISPLAY = {
    "plain_english": "plain_english",
    "rcce_1": "RCCE-1",
    "atrce_2": "ATRCE-2",
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


def run_claude_query(prompt: str, timeout: int) -> str:
    result = subprocess.run(
        ["claude", "-p", prompt],
        capture_output=True,
        text=True,
        timeout=timeout,
        check=True,
    )
    return result.stdout.strip()


def run_codex_query(prompt: str, timeout: int) -> str:
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        output_path = Path(tmp.name)

    try:
        subprocess.run(
            [
                "codex",
                "exec",
                "--skip-git-repo-check",
                "--sandbox",
                "read-only",
                "--color",
                "never",
                "--output-last-message",
                str(output_path),
                prompt,
            ],
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


def run_query(runner: str, prompt: str, timeout: int) -> str:
    if runner == "claude":
        return run_claude_query(prompt, timeout)
    if runner == "codex":
        return run_codex_query(prompt, timeout)
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


def estimated_token_count(text: str) -> int:
    # Approximate Claude-style token counts from plain text using a simple
    # word-to-token ratio. This is a benchmark proxy, not true tokenizer output.
    return max(1, int(math.ceil(word_count(text) * 1.33)))


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


def protocol_compliance(text: str) -> float:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return 0.0
    valid = sum(1 for line in lines if protocol_line_valid(line))
    return round(valid / len(lines) * 100, 1)


def repair_turns(condition: str, text: str) -> int:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if condition == "rcce_1":
        return sum(1 for line in lines if line.startswith("ASK:") or line.startswith("ESCALATE:"))
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
    parser.add_argument("--baseline", default="plain_english")
    return parser.parse_args()


def is_protocol_condition(condition_name: str) -> bool:
    return condition_name != "plain_english"


def display_condition(condition_name: str) -> str:
    return CONDITION_DISPLAY.get(condition_name, condition_name)


def main():
    args = parse_args()
    if args.repeats < 1:
        raise ValueError("--repeats must be at least 1")
    if args.baseline not in CONDITIONS:
        raise ValueError(f"--baseline must be one of: {', '.join(CONDITIONS)}")

    results = {}
    print(f"Runner: {args.runner}")
    print(f"Repeats: {args.repeats}")
    print(f"Baseline: {args.baseline}")

    for condition_name, condition_prompt in CONDITIONS.items():
        results[condition_name] = {}
        print(f"\nRunning: {condition_name}")
        for case in CASES:
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
                text = run_query(args.runner, prompt, args.timeout)
                internal_text, final_text = parse_output(text)
                raw_texts.append(text)
                parsed_internal.append(internal_text)
                parsed_finals.append(final_text)
                internal_token_runs.append(estimated_token_count(internal_text))
                line_runs.append(count_nonempty_lines(internal_text))
                compliance_runs.append(protocol_compliance(internal_text) if is_protocol_condition(condition_name) else 100.0)
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
    lines.append(f"Repeats per condition/case: `{args.repeats}`\n")
    lines.append(f"Baseline: `{args.baseline}`\n")
    lines.append(f"Conditions: {', '.join(f'`{display_condition(name)}`' for name in CONDITIONS)}\n")

    lines.append("## Per-Case Results\n")
    for case in CASES:
        label = case["label"]
        lines.append(f"### {label}\n")
        lines.append(f"Task: _{case['task']}_\n")
        baseline_cost = results[args.baseline][label]["internal_tokens"]
        for condition_name in CONDITIONS:
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

    totals = {name: {"internal_tokens": 0.0, "compliance": 0.0, "repair_turns": 0.0, "final_quality": 0.0} for name in CONDITIONS}
    for case in CASES:
        label = case["label"]
        for condition_name in CONDITIONS:
            result = results[condition_name][label]
            lines.append(
                f"| {label} | {display_condition(condition_name)} | {format_num(result['internal_tokens'])} | "
                f"{format_num(result['compliance'])}% | {format_num(result['repair_turns'])} | {format_num(result['final_quality'])} |"
            )
            for metric in totals[condition_name]:
                totals[condition_name][metric] += result[metric]

    for condition_name in CONDITIONS:
        lines.append("| **TOTAL / AVG** | "
                     f"{display_condition(condition_name)} | "
                     f"**{format_num(totals[condition_name]['internal_tokens'])}** | "
                     f"**{format_num(totals[condition_name]['compliance'] / len(CASES))}%** | "
                     f"**{format_num(totals[condition_name]['repair_turns'] / len(CASES))}** | "
                     f"**{format_num(totals[condition_name]['final_quality'] / len(CASES))}** |")

    lines.append("\n## Verdict\n")
    baseline_total = totals[args.baseline]["internal_tokens"]
    for condition_name in CONDITIONS:
        if condition_name == args.baseline:
            continue
        delta = percent_delta(baseline_total, totals[condition_name]["internal_tokens"])
        savings = baseline_total - totals[condition_name]["internal_tokens"]
        lines.append(
            f"`{display_condition(condition_name)}` reduced average internal coordination token cost by {delta:.1f}% vs `{display_condition(args.baseline)}`."
        )
        lines.append(
            f"Average compliance: {format_num(totals[condition_name]['compliance'] / len(CASES))}%; "
            f"average repair turns: {format_num(totals[condition_name]['repair_turns'] / len(CASES))}; "
            f"average final quality: {format_num(totals[condition_name]['final_quality'] / len(CASES))}."
        )
        lines.append(
            f"Average savings per {len(CASES)}-case suite: {format_num(savings)} internal tokens."
        )
        lines.append(
            f"Scale-up estimate: {format_num(scale_value(savings, 10))} tokens saved across 10 suites, "
            f"{format_num(scale_value(savings, 100))} across 100 suites, "
            f"{format_num(scale_value(savings, 1000))} across 1000 suites."
        )
        lines.append(
            f"Claude Sonnet 4 output-cost guideline: about ${savings * 15 / 1000000:.6f} saved per {len(CASES)}-case suite, "
            f"using $15 per million output tokens."
        )

    output = "\n".join(lines)
    with open(args.output, "w") as handle:
        handle.write(output)

    print(f"\nResults written to {args.output}")
    for condition_name in CONDITIONS:
        print(
            f"{condition_name}: total internal tokens {format_num(totals[condition_name]['internal_tokens'])}, "
            f"avg compliance {format_num(totals[condition_name]['compliance'] / len(CASES))}%, "
            f"avg repair {format_num(totals[condition_name]['repair_turns'] / len(CASES))}, "
            f"avg final quality {format_num(totals[condition_name]['final_quality'] / len(CASES))}"
        )


if __name__ == "__main__":
    main()
