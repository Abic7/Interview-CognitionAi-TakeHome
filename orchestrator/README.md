# Devin Orchestrator: Autonomous Remediation Automation

Event-driven automation using Devin API to autonomously remediate security vulnerabilities in Apache Superset.

## Overview

This system demonstrates how to leverage Devin as an autonomous decision-maker to fix real security issues end-to-end:

1. **Issues identified** — Two real CVEs in Apache Superset (pyjwt, requests)
2. **Orchestrator triggered** — Single API call starts Devin session
3. **Devin fixes autonomously** — Agent reads issues, finds files, writes code, opens PRs
4. **Status tracked** — Real-time dashboard shows progress
5. **No human approval** — Results are observable via REST API

## Quick Start (Docker)

### Prerequisites
- Docker & Docker Compose
- Devin API credentials (DEVIN_API_KEY, DEVIN_ORG_ID)
- GitHub personal access token

### Setup

```bash
# Create .env with your credentials
cp .env.example .env
# Edit .env:
# DEVIN_API_KEY=cog_xxxxx
# DEVIN_ORG_ID=org-xxxxx
# GITHUB_TOKEN=ghp_xxxxx
# GITHUB_FORK_OWNER=Abic7
# GITHUB_FORK_REPO=Interview-CognitionAi-TakeHome

# Start with Docker Compose
docker-compose up --build

# Orchestrator runs on http://localhost:8000
```

### Quick Start (Local Python)

```bash
# Install dependencies
pip install -r requirements.txt

# Create .env (see above)
cp .env.example .env

# Run
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Running the Automation

### 1. Health Check
```bash
curl http://localhost:8000/health
```

### 2. Start Devin Session
```bash
curl -X POST http://localhost:8000/sessions/start \
  -H "Content-Type: application/json" \
  -d '{"issue_numbers": [1, 2]}'
```

### 3. Monitor via API
```bash
curl http://localhost:8000/api/findings
curl http://localhost:8000/api/metrics
```

### 4. Monitor via Dashboard
Open `dashboard.html` in your browser or navigate to the orchestrator if hosting static files.

Auto-refreshes every 5 seconds showing real-time status.

## API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Health check |
| `/sessions/start` | POST | Start Devin session with issue numbers |
| `/api/findings` | GET | List all findings + PR status |
| `/api/metrics` | GET | Get remediation metrics (total, completed, status) |

## Architecture

**Code**: 150 lines of Python  
**Dependencies**: FastAPI, requests, python-dotenv, uvicorn  
**Database**: SQLite (findings, sessions tables)  
**Polling**: Every 30 seconds for GitHub PR updates

## Files

- `main.py` — Orchestrator service
- `requirements.txt` — Python dependencies
- `dashboard.html` — Real-time status dashboard
- `Dockerfile` — Docker build config
- `docker-compose.yml` — Docker Compose setup
- `.env.example` — Credential template
- `APPROACH.md` — Strategy & differentiation
- `DECISIONS.md` — Implementation decisions

## IP Protection Notice

This code is provided for interview evaluation purposes only. Unauthorized reproduction or commercial use is prohibited.

## How It Works

1. **Issue Creation**: Two real security vulnerabilities in Apache Superset
2. **API Trigger**: Single POST call to `/sessions/start` with issue numbers
3. **Devin Session**: Autonomous agent receives task prompt
4. **Autonomous Work**: Devin reads issues, finds files, writes code, tests, opens PRs
5. **Status Tracking**: Orchestrator polls GitHub API every 30s for new PRs
6. **Observability**: Dashboard and REST API show real-time progress

No human approval needed. Devin is the decision-maker.

## Why This Approach

vs. Full-Stack UI Systems: Minimal code (150 lines vs 500+), faster setup, clearer story about Devin's autonomy.

vs. Dashboard-Heavy: Focus on autonomy and observable results, not UI polish.

Devin is treated as a core primitive (decision-maker), not a helper tool.
