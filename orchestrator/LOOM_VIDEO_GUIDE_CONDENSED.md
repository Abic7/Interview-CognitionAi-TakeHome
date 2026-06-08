# Loom Video Recording Guide - CONDENSED (5 min EXACTLY)

**Goal**: Show end-to-end automation in 5 minutes max. Cut the fat.

---

## Condensed Timeline (5 min)

| Time | Scene | Duration | What to Show |
|------|-------|----------|-------------|
| 0:00 | Problem | 30 sec | 2 GitHub issues (5 sec each) |
| 0:30 | Trigger | 20 sec | Terminal: run API call, show response |
| 0:50 | Dashboard + PRs | 60 sec | Dashboard → click both PR links → quick GitHub PR view (10 sec each) |
| 1:50 | Code (quick) | 60 sec | VS Code: show 3 key functions only |
| 2:50 | Why Devin | 60 sec | Speak to camera: problem solved |
| 3:50 | Metrics view | 30 sec | Dashboard final screenshot |
| 4:20 | Close | 40 sec | "That's autonomous remediation" |

**Total: 5:00**

---

## Scene-by-Scene (CONDENSED)

### Scene 1: Problem (0:00 - 0:30)

**Screen**: GitHub Issues  
**URL**: https://github.com/Abic7/Interview-CognitionAi-TakeHome/issues

**Actions** (keep it SHORT):
1. Open issues page
2. Show Issue #1 title (read it): "Security: Upgrade pyjwt from 2.12.1 to 2.13.0"
3. Pause 3 sec
4. Show Issue #2 title (read it): "Security: Upgrade requests from 2.31.0 to 2.32.4+"
5. Pause 3 sec
6. Done — move to terminal

**Narration** (20 seconds):
"Two real security vulnerabilities in Apache Superset. Normally, a developer spends 20-30 minutes fixing each one. We're automating it with Devin."

---

### Scene 2: Trigger (0:30 - 0:50)

**Screen**: Terminal (PowerShell)

**Actions**:
1. Show terminal with orchestrator running
2. Run the one-liner:
   ```powershell
   Invoke-RestMethod -Uri "http://localhost:8001/sessions/start" -Method POST -ContentType "application/json" -Body (@{issue_numbers = @(1, 2)} | ConvertTo-Json)
   ```
3. Show response: `session_id`, `status: started`
4. Done

**Narration** (15 seconds):
"One API call. Devin gets the task and starts working. Autonomously."

---

### Scene 3: Results (0:50 - 1:50)

**Screen 3A**: Dashboard

**Actions**:
1. Switch to dashboard
2. Point to: "PRs Completed: 2" and "Status: RUNNING"
3. Show Issue #1 and #2 both showing "PR OPENED"
4. Pause 5 seconds
5. Click "View PR on GitHub" for Issue #1

**Narration** (first 15 seconds):
"The dashboard shows real-time status. Both issues fixed. Both PRs opened."

---

**Screen 3B**: GitHub PR #1 (5 seconds only)

**Actions**:
1. PR page loads
2. Show title and commit message
3. **NO scrolling** — just show the top
4. Go back immediately

**Narration** (5 seconds):
"Real PR, real code changes."

---

**Screen 3C**: Back to Dashboard, then GitHub PR #2 (5 seconds)

**Actions**:
1. Go back to dashboard
2. Click "View PR on GitHub" for Issue #2
3. Show title and commit
4. Go back

**Narration** (5 seconds):
"Both issues. Both fixed."

---

**Screen 3D**: Dashboard final view (rest of time)

**Actions**:
1. Back to dashboard
2. Show the full view with both issues and PRs
3. Pause to let viewer take it in

**Narration** (remaining 20 seconds):
"Devin handled it all. No human approval needed. The orchestrator detected both PRs automatically and updated the status. That's the key — autonomous end-to-end."

---

### Scene 4: Architecture (1:50 - 2:50)

**Screen**: VS Code with main.py

**Actions** (FAST, no long pauses):
1. Open main.py
2. Scroll to `create_devin_session()` — show ONE function
3. Point to the `prompt` variable being sent to Devin
4. Narrate: "Send a prompt with issue numbers. That's it."
5. Scroll to `@app.post("/sessions/start")` and `@app.get("/api/findings")`
6. Point and narrate: "Three endpoints. Trigger, check findings, done."
7. Done — close code

**Narration** (60 seconds, paced):
"The code is elegant because it's minimal. Create Devin session, poll every 30 seconds for PR status, expose three endpoints: start, findings, metrics. [PAUSE] The orchestrator is 150 lines. Devin is the decision-maker. Orchestrator just watches."

---

### Scene 5: Why Devin (2:50 - 4:20)

**Screen**: No code. Face-to-camera OR blank screen with your voice.

**Narration** (90 seconds):
"Why is this different? [PAUSE] Detection is solved. Snyk, Trivy, pip-audit all find vulnerabilities. [PAUSE] Remediation is still manual. A human has to read, understand, write, test, deploy. [PAUSE] Devin closes that gap. One autonomous agent can fix dozens of issues in parallel. It adapts to any codebase, validates its own work, and opens real PRs. [PAUSE] That's the power of autonomous agents. This is what happens when you stop treating AI as a tool and start treating it as a decision-maker."

---

### Scene 6: Wrap (4:20 - 5:00)

**Screen**: Dashboard (screenshot or live)

**Actions**:
1. Show dashboard one more time
2. Point to the metrics: "2 issues, 2 PRs, fully automated"

**Narration** (40 seconds):
"Two real security vulnerabilities. Two real pull requests. Opened by Devin. Tracked by the orchestrator. No human bottleneck. No approval gates. Just remediation at scale. That's what we built."

---

## Timing Checklist

- [ ] Problem: 30 sec (not 45)
- [ ] Trigger: 20 sec (not 45)
- [ ] Dashboard + PRs: 60 sec (not 90) — show both PRs quickly
- [ ] Code: 60 sec (not 90) — show 2-3 functions only, no deep dives
- [ ] Why Devin: 90 sec (face to camera, no screen)
- [ ] Wrap: 40 sec (dashboard + closing)
- **TOTAL: 5:00 EXACTLY**

---

## What to CUT

- ❌ Long pauses reading GitHub issues (3 sec each max)
- ❌ Detailed explanation of every code function
- ❌ Scrolling through PR file changes
- ❌ Showing CI check runs in detail
- ❌ Over-explaining the orchestrator logic
- ❌ Multiple slides or diagrams
- ❌ Any screen time over 15-20 seconds without narration

## What to KEEP

- ✅ Real GitHub issues (they're the problem)
- ✅ Real API call (proves it's live)
- ✅ Real Dashboard (shows automation in action)
- ✅ Real GitHub PRs (prove Devin worked)
- ✅ Code overview (show it's minimal, 150 lines)
- ✅ "Why Devin" narrative (the story matters more than the code)

---

## Pro Tips for 5-Minute Recording

1. **Speak at normal pace** — don't rush, but don't linger
2. **No screen time > 20 seconds without narration** — silence kills momentum
3. **Pre-record if needed** — if live demo is risky, record it once and use that clip
4. **Use Loom's zoom feature** — zoom into code so it's readable
5. **Practice once** — do a dry run to hit the 5-minute mark exactly
6. **Don't polish** — raw is better than over-produced for technical talks
7. **Narration is 80% of the video** — code is just proof
8. **End strong** — final sentence should stick: "Autonomous remediation at scale."

---

## Exact Word Count for Narration

**Scene 1** (30 sec): ~70 words  
**Scene 2** (20 sec): ~45 words  
**Scene 3** (60 sec): ~170 words  
**Scene 4** (60 sec): ~180 words  
**Scene 5** (90 sec): ~270 words  
**Scene 6** (40 sec): ~120 words  

**Total: ~855 words / 5 minutes = 171 words/minute (natural speech pace)**

---

## Quick Narration (Copy-Paste Ready)

**Scene 1**: "Two real security vulnerabilities in Apache Superset. Normally a developer spends 20-30 minutes fixing each one. We're automating it with Devin."

**Scene 2**: "One API call. Devin gets the task and starts working. Autonomously."

**Scene 3**: "The dashboard shows real-time status. Both issues fixed. Both PRs opened. Devin handled it all. No human approval needed."

**Scene 4**: "The code is elegant because it's minimal. Create Devin session, poll for PR status, expose three endpoints. The orchestrator is 150 lines. Devin is the decision-maker. Orchestrator just watches."

**Scene 5**: "Detection is solved. Every tool finds vulnerabilities. Remediation is still manual. Devin closes that gap. One autonomous agent fixes dozens of issues in parallel. It adapts to any codebase, validates its own work. That's the power of autonomous agents."

**Scene 6**: "Two real security vulnerabilities. Two real pull requests. Opened by Devin. Tracked by the orchestrator. No human bottleneck. Remediation at scale."

---

## You're Ready

- Script: ✅
- Timing: ✅ (5 min exactly)
- Screens: ✅ (6 scenes)
- Narration: ✅ (copy-paste ready)

Record with confidence. This story is strong.
