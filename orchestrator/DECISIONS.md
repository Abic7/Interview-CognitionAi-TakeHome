# Decisions Log

## Phase 1: Issue Identification

### Decision 1.1: Repository Setup
**Date**: 2026-06-05  
**Decision**: Create private GitHub repo `Interview-CognitionAi-TakeHome` as working copy of Apache Superset  
**Why**: Need private repo for IP protection; easier to add access to Cognition reviewer by email than forking  
**Alternative Considered**: Fork as public → add Cognition email as collaborator later (more cumbersome)  
**Outcome**: ✓ Private repo created, Superset code cloned, ready for issues

---

### Decision 1.2: Issue Selection Strategy
**Date**: 2026-06-05  
**Decision**: Pick 2 simple issues (easy + medium) from pip-audit output instead of 3-5 complex ones  
**Why**: 
- Guarantees completion within 90-min timeline
- Cleaner narrative (2 issues → 2 PRs = full proof of concept)
- Reduces risk of partial work
- Shows quality over quantity
**Alternative Considered**: 
- 5-8 issues: More ambitious, higher risk of timeout, 1-2 PRs might fail
- 1 issue: Not enough signal
**Outcome**: ✓ Selected pyjwt and requests; both real CVEs from pip-audit

---

### Decision 1.3: Issue #1 — pyjwt 2.12.1 → 2.13.0
**Date**: 2026-06-05  
**Decision**: Upgrade pyjwt (JWT library) as the EASY issue  
**Why**:
- 5 published CVEs (PYSEC-2026-175 through 179)
- Single dependency, straightforward bump
- Superset uses it; impact is real
- ~10-15 min fix for Devin
**Why Not**:
- pip: CVE-2026-6357 (too meta, pip upgrading itself)
- uv: GHSA-4gg8-gxpx-9rph (build tool, not core dependency)
**Outcome**: ✓ Issue created as GitHub #1 with label `devin-eligible`

---

### Decision 1.4: Issue #2 — requests 2.31.0 → 2.32.4+
**Date**: 2026-06-05  
**Decision**: Upgrade requests library as the MEDIUM issue  
**Why**:
- 3 CVEs across multiple severities (CVE-2024-35195, CVE-2024-47081, CVE-2026-25645)
- More complex than pyjwt (likely multiple requirements files, possible version coordination)
- Widely used, higher impact fix
- ~15-20 min fix for Devin
**Why Not**:
- starlette: PYSEC-2026-161 (framework, riskier dependency to bump)
- urllib3: 2 CVEs but lower severity, less critical than requests
**Outcome**: ✓ Issue created as GitHub #2 with label `devin-eligible`

---

## Phase 2: Orchestrator Design (In Progress)

### Decision 2.1: Language + Framework
**Date**: 2026-06-05 (planning)  
**Decision**: Python FastAPI for orchestrator  
**Why**:
- Quick to write (~150 lines)
- Native async/await for polling
- Built-in JSON responses
- SQLite integration simple
**Alternative Considered**: Node.js/Express (would take longer to write)  
**Outcome**: Pending implementation

---

### Decision 2.2: Architecture Pattern
**Date**: 2026-06-05 (planning)  
**Decision**: Simple request-response with background polling, no webhooks  
**Why**:
- Devin v3 API doesn't expose webhooks
- Polling every 30s is sufficient for 2 issues
- Simpler code, fewer failure modes
**Alternative Considered**: Long-polling, server-sent events (overengineering for 2 issues)  
**Outcome**: Pending implementation

---

## Timeline So Far

| Phase | Start | Duration | Status |
|-------|-------|----------|--------|
| Phase 1 | 06-05 | 10 min | ✓ Complete |
| Phase 2 | 06-05 | 30 min | → Starting now |
| Phase 3 | TBD | 20 min | Pending |
| Phase 4 | TBD | 20 min | Pending |
| Phase 5 | TBD | 10 min | Pending |

---

## Blockers / Learnings

- **Git merge unrelated histories**: Resolved with `--allow-unrelated-histories` flag
- **No private fork option**: Worked around by creating private repo + mirror clone
- **GitHub issue templates**: Had to use "Blank issue" to create custom security issues

---

**Next**: Build orchestrator (Phase 2, 30 min)
