# Conclusions: Agent-to-Agent Coordination Protocol Benchmark

## What was tested

Five coordination formats across 7–9 task types, repeated 3× each, measured on internal token cost, protocol compliance, repair turns, and final output quality.

- `plain_english` — baseline prose
- `RCCE-1` — typed key=value schema
- `ATRCE-2` — extended typed schema with interrupt/escalate
- `PCL-1` — compact English abbreviations (CLM, OBJ, EVD, REV…)
- `SDC-1` — pure symbolic operators (+c1, -c1, =c1…)

Runners: **Codex (gpt-5.2-codex)** and **Claude Sonnet 4.6**.

---

## Key findings

### PCL-1 is the best format across both runners

| Runner | Savings vs plain English | Compliance | Quality |
|---|---|---|---|
| Codex | 44.6% | 98.8% | 2.7 / 3 |
| Claude | ~76% | 100% | holds |

PCL-1 consistently compresses coordination exchanges without compliance failures or quality loss. It works better on Claude than Codex.

### SDC-1 is Codex-only

| Runner | Savings | Compliance |
|---|---|---|
| Codex | 57% | 100% |
| Claude | n/a | ~0% |

Claude completely ignores SDC-1 syntax and writes prose instead. Do not use SDC-1 with Claude-based agents.

**Why:** SDC-1 uses pure symbolic operators (`+c1`, `-c1`) with no English anchors. Claude's RLHF training biases it toward readable output — it treats the schema as noise. Codex is code-first and follows strict syntax precisely. PCL-1 works on both because its abbreviations (`CLM`, `OBJ`) are close enough to English that Claude latches onto them.

### RCCE-1 and ATRCE-2 are mostly not worth it

Both save only 5–28% on internal tokens while adding schema overhead and occasional compliance failures. The token savings don't justify the complexity for most tasks. Useful only if you specifically need typed, auditable message fields.

### The one recurring failure case

`missing_evidence_repair` is the hardest task for all compressed formats. It's the only case where PCL-1 dropped below 100% compliance on Codex (91.7%). Claude handled it fine. This case involves challenging an unsupported claim mid-thread — the most complex repair pattern tested.

---

## Caveats and limitations

### 1. The benchmark measures coordination tokens only
In a real multi-agent system, each agent also has a system prompt, tool definitions, and full conversation history. Coordination messages are a fraction of total token spend. If your coordination exchange is 50 tokens out of a 2,000-token context, saving 76% of those 50 tokens = 38 tokens saved per turn.

### 2. Protocol instruction overhead is not counted
To use PCL-1, every agent needs ~80–100 tokens of instructions in their system prompt. For short tasks this overhead cancels the savings. It only pays off at scale: many agents, many turns, long-running pipelines.

### 3. This is a simulated benchmark
One model generated all four "agents" in a single response. Real multi-agent systems have separate API calls, independent context windows, tool use, and failure modes that were not tested. Real-world compliance may be lower.

### 4. Token counts are not directly comparable across runners
Codex results used `openai_exact` (tiktoken). Claude results used a heuristic estimator. The relative savings within each runner are valid; absolute cross-runner token numbers are not.

### 5. Quality scoring is heuristic
Final quality was scored by keyword matching and word count. Real quality degradation may be worse than measured, especially for complex reasoning tasks.

---

## When to apply PCL-1

**Apply when:**
- Agents exchange many coordination messages (10+ turns in a session)
- Multiple agents run in parallel and need structured handoffs
- Token cost is a meaningful constraint (long-running pipelines, high volume)
- You need inspectable, repairable coordination logs

**Skip when:**
- Coordination is 3–5 turns — overhead cancels savings
- Agents are working independently with minimal coordination
- The task is complex enough that compressed format risks losing nuance (use `ESC` to fall back to plain English)
- You are using small/cheap models as subagents — compliance will likely be worse

## When to use SDC-1

Only with Codex-based agents. Never with Claude.

---

## Routing summary

| Agent runner | Recommended format | Notes |
|---|---|---|
| Claude | PCL-1 | 76% savings, 100% compliance |
| Codex | SDC-1 | 57% savings if quality acceptable |
| Codex | PCL-1 | fallback for quality-critical tasks |
| Mixed | PCL-1 | only format that works on both |

---

## Reusable infrastructure

`run_tests.py` is a working benchmark harness. Use it to:
- Test new formats against this baseline
- Test new models (add `--runner` and `--claude-model` / `--codex-model`)
- Run subsets with `--conditions` and `--cases`
- Results auto-save per condition so crashes don't lose progress
