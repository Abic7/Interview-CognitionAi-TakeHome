# Approach: Devin as Autonomous Decision-Maker

## Problem Statement
Apache Superset has real security vulnerabilities. Manual remediation is time-consuming and error-prone. How do we automate it using an autonomous coding agent?

## Strategic Differentiation

**Known Solutions:**
- **devin-issues** (Jan 2026): Full-stack TypeScript app with React UI, database, human-in-the-loop scoping
- **devin-superset** (May 2026): Python orchestrator + Next.js dashboard with ROI metrics

**Our Approach:**
Instead of building a complex system for humans to orchestrate Devin, we treat **Devin as the autonomous decision-maker** — it picks issues, figures out fixes, and pushes PRs with minimal orchestration overhead.

### Key Design Principles

1. **Devin Drives the System** — Not a tool called by humans; Devin is the agent that acts
2. **Minimal Orchestration** — Lightweight FastAPI service (~150 lines) that:
   - Triggers Devin with a task
   - Polls for progress
   - Records results
3. **Simple Observability** — REST API endpoints return JSON; no dashboard complexity
4. **Ruthless Scope** — 2 carefully selected issues, not 5-8; guarantees completion

## Why This Matters

**Narrative for evaluators:**
- Detection (finding vulnerabilities) is commodity — scanners do this
- Remediation is still mostly manual — this is where value is
- Autonomous agents like Devin can close that loop without human bottlenecks
- This system proves Devin can work independently: pick issue → understand context → implement fix → validate → PR

## Architecture Overview

```
GitHub Issues (pyjwt, requests vulnerabilities)
    ↓
Orchestrator triggers Devin session
    ↓
Devin autonomously:
  - Reads issue
  - Finds affected files
  - Writes code
  - Runs tests
  - Opens PR
    ↓
Orchestrator detects PR
    ↓
REST API returns: { issues: 2, prs_opened: 2, status: "complete" }
```

**Why no UI?** — Devin's autonomy is the story. A dashboard adds complexity without adding signal.

## Issue Selection Rationale

**Issue #1: pyjwt 2.12.1 → 2.13.0**
- **Complexity**: Easy (single dependency bump)
- **Risk**: Low (well-tested library, straightforward upgrade)
- **Signal**: Proves Devin can find and update vulnerable packages
- **Effort**: ~10-15 min for Devin

**Issue #2: requests 2.31.0 → 2.32.4+**
- **Complexity**: Medium (multiple requirements files, may need version pinning adjustments)
- **Risk**: Medium (slightly more touch points than pyjwt)
- **Signal**: Shows Devin can handle multi-file updates, dependency coordination
- **Effort**: ~15-20 min for Devin

**Why 2, not 5-8?**
- Clear proof of autonomy (both issues → both PRs)
- Fast execution (30-40 min Devin compute time)
- No scrambling on time budget
- Stronger narrative (quality over quantity)

## Success Criteria

1. ✓ Orchestrator successfully triggers Devin
2. ✓ Both PRs open on GitHub (automated, no human approval)
3. ✓ API endpoints return correct JSON metrics
4. ✓ Loom video clearly shows end-to-end flow
5. ✓ Code is tight (no scope creep, no unnecessary features)

## What This Demonstrates

| Evaluation Criterion | How We Address It |
|---|---|
| **Translate ambiguous problems into working systems** | Issues defined; Devin receives task; PRs appear as proof |
| **Leverage Devin as core primitive** | Devin is the decision-maker; orchestrator just watches |
| **Communicate technical execution + business impact** | Loom + API metrics show both |
| **Problem-solving ability** | Scoped ruthlessly, identified real CVEs, build minimal system |

---

## Next Steps (Once Working)

This foundation enables:
- Multi-repo queue (same pattern, multiple Superset-like projects)
- Auto-merge on CI pass (orchestrator detects green checks, merges PR)
- Slack notifications (each issue completion → team alert)
- Devin-driven audit loop (Devin runs security scanner *and* fixes; closes full loop)
