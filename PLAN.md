# Cognition AI Devin Take-Home: Execution Plan

**Goal**: Build event-driven automation using Devin API to autonomously remediate 2 code issues in Apache Superset, demonstrating end-to-end architecture where Devin is the decision-maker.

**Timeline**: 90 minutes total

---

## Differentiation Strategy

**Prior solutions** (devin-issues, devin-superset) built comprehensive dashboards and complex systems.

**Your approach**: Minimal orchestrator (150 lines Python) + 2 handpicked issues + simple observability API. Show depth in architecture, not breadth in features.

**Narrative**: "Devin autonomously picks up issues, figures out fixes, and pushes PRs. Orchestrator watches and reports."

---

## Phase 1: Issue Identification (10 min)

### What You'll Do
1. Clone Apache Superset to your local machine
2. Identify 2 easy-to-medium issues (maximum ROI, minimum complexity)
   - **Issue 1 (EASY)**: Dependency upgrade — e.g., pip-audit finding, simple version bump
   - **Issue 2 (MEDIUM)**: Configuration hardening — e.g., add security header, tighten default
3. Create 2 GitHub issues in your **private fork** with clear remediation guidance
4. Label both with `devin-eligible`

### Manual Actions Required
- [ ] Create private GitHub fork of Apache Superset
  - Go to https://github.com/apache/superset → Fork → Set to Private
  - Clone to local: `git clone https://github.com/YOUR_USERNAME/superset.git`
- [ ] Run diagnostics to find issues:
  - `pip install pip-audit && pip-audit` (check for dependency vulnerabilities)
  - `grep -r "security" . --include="*.py" | head -20` (look for security-related code)
  - Look at `superset/config.py` for hardening opportunities
- [ ] Create 2 GitHub issues in your fork:
  - Issue 1: "Upgrade [package-name] from X.Y.Z to A.B.C" (with pip-audit output)
  - Issue 2: "Harden default configuration: add security header [or config change]" (with recommendation)
  - Label both: `devin-eligible`
  - Note the issue numbers (e.g., #1, #2)

### Deliverable
- 2 GitHub issues in your private fork, labeled `devin-eligible`
- You have issue numbers documented

---

## Phase 2: Orchestrator Build (30 min)

### What Will Happen
I will write a Python FastAPI orchestrator (~150 lines) that:
- Triggers a Devin session with your 2 issues
- Polls the Devin API every 30s to track progress
- Detects new PRs on GitHub
- Exposes `/api/findings` and `/api/metrics` endpoints
- Stores data in SQLite

### Manual Actions Required
- [ ] Have your Devin API credentials ready (from earlier screenshot):
  - API Key (starts with `cog_...`)
  - Organization ID (starts with `org-...`)
  - GitHub Personal Access Token (with `repo` scope)
- [ ] Create project directory structure:
  ```
  E:\LEARNING\Interview - CognitionAi - Take Home\
  ├── orchestrator/
  │   ├── main.py           (I'll write this)
  │   ├── requirements.txt   (I'll write this)
  │   └── .env              (you create: DEVIN_API_KEY, ORG_ID, GITHUB_TOKEN)
  ├── docs/
  │   ├── APPROACH.md       (I'll write this)
  │   └── DECISIONS.md      (we'll update as we go)
  └── PLAN.md               (this file)
  ```

### Deliverable
- Working FastAPI orchestrator with `/sessions/start`, `/api/findings`, `/api/metrics` endpoints

---

## Phase 3: Trigger + Validate (20 min)

### What Will Happen
You'll run the orchestrator locally and trigger the Devin session.

### Manual Actions Required
- [ ] Install Python dependencies:
  ```bash
  cd E:\LEARNING\Interview - CognitionAi - Take Home\orchestrator
  pip install -r requirements.txt
  ```
- [ ] Create `.env` file in `orchestrator/` directory with:
  ```
  DEVIN_API_KEY=cog_xxxxx
  DEVIN_ORG_ID=org-xxxxx
  GITHUB_TOKEN=ghp_xxxxx
  GITHUB_FORK_OWNER=YOUR_USERNAME
  GITHUB_FORK_REPO=superset
  ```
- [ ] Start the orchestrator:
  ```bash
  python main.py
  ```
- [ ] In another terminal, trigger the session:
  ```bash
  curl -X POST http://localhost:8000/sessions/start \
    -H "Content-Type: application/json" \
    -d '{"issue_numbers": [1, 2]}'
  ```
- [ ] Monitor progress:
  ```bash
  # Keep running this every 10-15 seconds
  curl http://localhost:8000/api/findings
  curl http://localhost:8000/api/metrics
  ```
- [ ] Watch Devin IDE window — you'll see the agent working on your issues
- [ ] After 20-40 minutes, check your GitHub fork for 2 new PRs

### Deliverable
- 2 open PRs on your private Superset fork (auto-opened by Devin)
- API endpoints responding with JSON showing both issues as "completed"

---

## Phase 4: Loom Video (20 min)

### What You'll Record
A 5-minute Loom video showing the full end-to-end flow.

### Manual Actions Required
- [ ] Open Loom (https://www.loom.com) and start recording
- [ ] Screen sequence:
  1. **Setup (0:00-0:45)**: Show your private fork with 2 labeled issues
  2. **Trigger (0:45-1:15)**: Terminal window, run `curl POST /sessions/start`, show response
  3. **Devin Working (1:15-2:15)**: Devin IDE window showing agent working (speed up video 2-3x)
  4. **PRs Appearing (2:15-2:45)**: GitHub fork, show 2 new PRs opening
  5. **Observability (2:45-3:15)**: Terminal, run `curl /api/findings` and `curl /api/metrics`, show JSON
  6. **Architecture Walkthrough (3:15-4:30)**: Show orchestrator code (~150 lines), explain:
     - How Devin gets triggered
     - How orchestrator polls and tracks progress
     - Why this design (no UI, no dashboard complexity)
  7. **Close (4:30-5:00)**: "Two real issues, fixed autonomously, end-to-end. No human bottleneck."
- [ ] Save video, upload to Loom, get shareable link

### Deliverable
- 5-minute Loom video, uploaded and shareable

---

## Phase 5: Docs + Submit (10 min)

### What We'll Do
Add IP protection notice, finalize README, submit via Ashby.

### Manual Actions Required
- [ ] Create `README.md` in project root (I'll provide template)
- [ ] Add IP protection notice (boilerplate)
- [ ] Document the 2 issues you chose and why in `docs/DECISIONS.md`
- [ ] Submit via: https://you.ashbyhq.com/cognition/assignment/a850c981-32b3-48d7-9b8c-153b33eacdd8
  - Attach: GitHub repo link (private fork), GitHub repo link (orchestrator), Loom video

---

## Next Step: Phase 1 Starts Now

**Your immediate action items:**

1. **Create private GitHub fork** of Apache Superset
   - Go to https://github.com/apache/superset
   - Click "Fork"
   - Select your personal account
   - Check "Private"
   - Click "Create fork"

2. **Clone it locally**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/superset.git
   cd superset
   ```

3. **Find 2 issues** (run these commands in the cloned repo):
   ```bash
   # Look for dependencies to upgrade
   pip install pip-audit
   pip-audit
   
   # Or look at config hardening needs
   cat superset/config.py | head -50
   ```

4. **Create 2 GitHub issues** in your fork:
   - Example Issue 1: "Upgrade pip package X from Y to Z"
   - Example Issue 2: "Add security headers to default config"
   - Label both: `devin-eligible`

**Once you've done these 4 steps, message me back with the issue numbers and repo URL, and we'll move to Phase 2.**

---

## Timeline at a Glance

| Phase | Time | Status |
|-------|------|--------|
| 1. Identify 2 issues | 10 min | Starting now |
| 2. Build orchestrator | 30 min | Pending Phase 1 |
| 3. Trigger + validate | 20 min | Pending Phase 2 |
| 4. Loom video | 20 min | Pending Phase 3 |
| 5. Docs + submit | 10 min | Pending Phase 4 |
| Buffer | 10 min | Contingency |
| **TOTAL** | **90 min** | |

---

## Critical Success Factors

✓ 2 real, simple issues (not complex OWASP vulnerabilities)  
✓ Clear remediation guidance in each GitHub issue  
✓ Orchestrator successfully triggers Devin  
✓ Both PRs actually open (proof Devin worked)  
✓ API endpoints return correct JSON  
✓ Loom shows the full flow clearly  

---

**Status**: Waiting for you to complete Phase 1. Ping me when you have 2 issues created.
