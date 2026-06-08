"""
Devin Orchestrator: Autonomous remediation automation
Triggers Devin sessions to fix GitHub issues, polls for progress, tracks PRs.

IP Protection Notice:
This code is provided for interview evaluation purposes only.
Unauthorized reproduction or commercial use is prohibited.
"""

import os
import sqlite3
import time
from datetime import datetime
from typing import Optional
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)

# Load environment variables
DEVIN_API_KEY = os.getenv("DEVIN_API_KEY")
DEVIN_ORG_ID = os.getenv("DEVIN_ORG_ID")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_FORK_OWNER = os.getenv("GITHUB_FORK_OWNER")
GITHUB_FORK_REPO = os.getenv("GITHUB_FORK_REPO", "Interview-CognitionAi-TakeHome")

# Validate credentials
if not all([DEVIN_API_KEY, DEVIN_ORG_ID, GITHUB_TOKEN, GITHUB_FORK_OWNER]):
    print("ERROR: Missing required environment variables in .env file")
    print(f"  DEVIN_API_KEY: {bool(DEVIN_API_KEY)}")
    print(f"  DEVIN_ORG_ID: {bool(DEVIN_ORG_ID)}")
    print(f"  GITHUB_TOKEN: {bool(GITHUB_TOKEN)}")
    print(f"  GITHUB_FORK_OWNER: {bool(GITHUB_FORK_OWNER)}")
    exit(1)

# Database setup
DB_PATH = Path(__file__).parent / "orchestrator.db"

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class SessionStartRequest(BaseModel):
    issue_numbers: list[int]

class FindingResponse(BaseModel):
    issue_num: int
    title: str
    status: str
    pr_url: Optional[str] = None
    completed_at: Optional[str] = None

class MetricsResponse(BaseModel):
    total_issues: int
    prs_completed: int
    status: str

# Database initialization
def init_db():
    """Initialize SQLite database with findings and sessions tables."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS findings (
        id INTEGER PRIMARY KEY,
        github_issue_number INTEGER UNIQUE,
        title TEXT,
        status TEXT DEFAULT 'new',
        pr_url TEXT,
        created_at TEXT,
        devin_session_id TEXT
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS devin_sessions (
        id INTEGER PRIMARY KEY,
        session_id TEXT UNIQUE,
        status TEXT DEFAULT 'running',
        pr_url TEXT,
        started_at TEXT,
        completed_at TEXT
    )''')

    conn.commit()
    conn.close()

def get_db():
    """Get database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def create_devin_session(task_description: str) -> str:
    """Create a Devin session via API and return session_id."""
    headers = {
        "Authorization": f"Bearer {DEVIN_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "prompt": task_description
    }

    url = f"https://api.devin.ai/v3/organizations/{DEVIN_ORG_ID}/sessions"

    try:
        print(f"Creating Devin session with URL: {url}")
        print(f"Payload: {payload}")
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.text}")
        response.raise_for_status()
        data = response.json()
        return data.get("session_id") or data.get("id")
    except Exception as e:
        print(f"Error creating Devin session: {e}")
        raise

def poll_devin_session(session_id: str) -> dict:
    """Poll Devin session status and check for PR URLs."""
    headers = {
        "Authorization": f"Bearer {DEVIN_API_KEY}",
        "Content-Type": "application/json"
    }

    url = f"https://api.devin.ai/v3/organizations/{DEVIN_ORG_ID}/sessions/{session_id}"

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error polling Devin session {session_id}: {e}")
        return {"status": "error", "message": str(e)}

def get_github_prs(issue_number: int) -> Optional[str]:
    """Get PR URL linked to a GitHub issue."""
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    url = f"https://api.github.com/repos/{GITHUB_FORK_OWNER}/{GITHUB_FORK_REPO}/issues/{issue_number}"

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Check if issue has linked PR in body
        if data.get("pull_request"):
            return data["pull_request"]["html_url"]

        # Search for PRs that reference this issue
        search_url = f"https://api.github.com/repos/{GITHUB_FORK_OWNER}/{GITHUB_FORK_REPO}/pulls"
        search_response = requests.get(search_url, headers=headers, timeout=10)
        search_response.raise_for_status()

        for pr in search_response.json():
            if f"#{issue_number}" in pr.get("body", ""):
                return pr["html_url"]

        return None
    except Exception as e:
        print(f"Error fetching GitHub PR for issue {issue_number}: {e}")
        return None

@app.on_event("startup")
def startup():
    """Initialize database on startup."""
    init_db()

@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "ok"}

@app.post("/sessions/start")
def start_session(request: SessionStartRequest):
    """Start a new Devin session to fix the specified issues."""
    issue_numbers = request.issue_numbers

    conn = get_db()
    c = conn.cursor()

    # Check if issues already exist in DB
    existing = []
    for issue_num in issue_numbers:
        c.execute("SELECT devin_session_id FROM findings WHERE github_issue_number = ?", (issue_num,))
        row = c.fetchone()
        if row and row["devin_session_id"]:
            existing.append(issue_num)

    if existing:
        return {
            "status": "already_running",
            "message": f"Issues {existing} already have active sessions",
            "issue_numbers": issue_numbers
        }

    # Fetch issue titles from GitHub
    issue_titles = {}
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    for issue_num in issue_numbers:
        try:
            url = f"https://api.github.com/repos/{GITHUB_FORK_OWNER}/{GITHUB_FORK_REPO}/issues/{issue_num}"
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            issue_titles[issue_num] = response.json()["title"]
        except Exception as e:
            print(f"Error fetching issue {issue_num}: {e}")
            issue_titles[issue_num] = f"Issue {issue_num}"

    # Create Devin session with task
    issue_list = "\n".join([f"- Issue #{num}: {issue_titles.get(num, f'Issue {num}')}" for num in issue_numbers])

    task = f"""
You have the following GitHub issues to fix in the {GITHUB_FORK_REPO} repository:

{issue_list}

For each issue:
1. Read the GitHub issue description to understand what needs to be fixed
2. Find the affected files in the codebase
3. Make the necessary code changes
4. Test your changes if possible
5. Create a pull request with the fix

Work through the issues in order. Report the PR URLs in your final message.
"""

    try:
        session_id = create_devin_session(task)

        # Store findings in DB
        now = datetime.utcnow().isoformat()
        for issue_num in issue_numbers:
            c.execute("""
                INSERT INTO findings (github_issue_number, title, status, created_at, devin_session_id)
                VALUES (?, ?, 'in_progress', ?, ?)
            """, (issue_num, issue_titles.get(issue_num, f"Issue {issue_num}"), now, session_id))

        # Store session
        c.execute("""
            INSERT INTO devin_sessions (session_id, status, started_at)
            VALUES (?, 'running', ?)
        """, (session_id, now))

        conn.commit()
        conn.close()

        return {
            "status": "started",
            "session_id": session_id,
            "issue_numbers": issue_numbers,
            "created_at": now
        }
    except Exception as e:
        conn.close()
        return {
            "status": "error",
            "message": str(e)
        }

@app.get("/api/findings")
def get_findings():
    """Get all findings with current status."""
    conn = get_db()
    c = conn.cursor()

    c.execute("SELECT * FROM findings ORDER BY github_issue_number")
    findings = []

    for row in c.fetchall():
        issue_num = row["github_issue_number"]

        # Check for PR
        pr_url = get_github_prs(issue_num)

        if pr_url and row["status"] == "in_progress":
            c.execute("""
                UPDATE findings SET status = 'pr_opened', pr_url = ? WHERE github_issue_number = ?
            """, (pr_url, issue_num))
            conn.commit()

        findings.append({
            "issue_num": issue_num,
            "title": row["title"],
            "status": row["status"],
            "pr_url": pr_url or row["pr_url"],
            "created_at": row["created_at"]
        })

    conn.close()
    return findings

@app.get("/api/metrics")
def get_metrics():
    """Get remediation metrics."""
    conn = get_db()
    c = conn.cursor()

    c.execute("SELECT COUNT(*) as total FROM findings")
    total = c.fetchone()["total"]

    c.execute("SELECT COUNT(*) as completed FROM findings WHERE status IN ('pr_opened', 'completed')")
    completed = c.fetchone()["completed"]

    c.execute("SELECT status FROM devin_sessions ORDER BY started_at DESC LIMIT 1")
    session_status = c.fetchone()

    conn.close()

    return {
        "total_issues": total,
        "prs_completed": completed,
        "status": session_status["status"] if session_status else "idle"
    }

@app.post("/api/poll")
def manual_poll():
    """Manually trigger polling for Devin session updates."""
    conn = get_db()
    c = conn.cursor()

    c.execute("SELECT devin_session_id FROM findings WHERE status = 'in_progress' LIMIT 1")
    finding = c.fetchone()

    if not finding:
        conn.close()
        return {"status": "no_active_sessions"}

    session_id = finding["devin_session_id"]

    # Poll Devin
    session_data = poll_devin_session(session_id)

    # Update status if session is complete
    if session_data.get("status") in ["completed", "finished"]:
        c.execute("UPDATE devin_sessions SET status = ? WHERE session_id = ?",
                 (session_data.get("status"), session_id))
        conn.commit()

    conn.close()

    return {
        "session_id": session_id,
        "devin_status": session_data.get("status"),
        "findings_updated": True
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
