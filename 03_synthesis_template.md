# Synthesis Template

Use this template after each debate round to produce the round's candidate system prompt.

---

## Round metadata

**Round number:**
**Agents:**
**Date:**

---

## Step 1 — The candidate system prompt text

The actual prompt text. Ready to paste into a system prompt field. 2-6 sentences.

> [Candidate system prompt]

---

## Step 2 — Estimated token reduction vs. caveman

For each benchmark query type, simulate what Claude would output under this prompt and under caveman. Estimate the token count for each.

| Query type | Caveman output | Caveman tokens | Candidate output | Candidate tokens | Winner |
|------------|---------------|----------------|-----------------|-----------------|--------|
| Simple factual | | | | | |
| Process explanation | | | | | |
| Comparison | | | | | |
| Opinion/recommendation | | | | | |
| Multi-step | | | | | |
| Ambiguous | | | | | |

**Net assessment:** does the candidate beat caveman on average token count? Honest answer required.

---

## Step 3 — What the candidate drops vs. caveman

List specifically what this prompt instructs Claude to drop that caveman does not drop. These are the token savings mechanisms.

| Element dropped | Token savings estimate | Risk to coherence |
|----------------|----------------------|-------------------|
| | | |

---

## Step 4 — What the candidate keeps that caveman drops

List what this prompt keeps that caveman removes. These are the cases where the candidate produces longer output than caveman — and whether that longer output is justified.

| Element kept | Why kept | Extra tokens justified? |
|-------------|----------|------------------------|
| | | |

---

## Step 5 — Failure modes

Where does this candidate produce output that is too short to be usable? Where does it produce output that is longer than it needs to be?

**Too short (unusable):**

**Too long (beats caveman locally but not overall):**

---

## Step 6 — Honest comparison to caveman

**Where this prompt beats caveman on raw token count:**

**Where caveman produces shorter output:**

**Overall: does this candidate beat caveman?** (Yes / No / Depends on query type)
