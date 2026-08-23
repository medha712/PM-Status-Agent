# Status Manager - Project Overview

## What You've Got

A **production-ready** intelligent project management status agent that:

✅ **Connects to 3 PM Platforms**
- Jira (sprint tracking, blocking issues)
- Asana (project status, at-risk tasks)  
- Notion (strategic initiatives, status updates)

✅ **Automatically Detects Blockers**
- Dependency blocked items
- Tasks stuck in progress 5+ days
- Overdue tasks
- At-risk items flagged in tools
- External blockers (vendor delays, etc.)

✅ **Tracks Week-over-Week Trends**
- Health score history (52-week rolling)
- Completion velocity trends
- Blocker count patterns
- Identifies items stuck multiple sprints

✅ **Generates Risk-Based Reports**
- Weekly status reports
- Risk assessments with priority flags
- Chronic blocker reports
- Trend analysis

✅ **Natural Language Interface**
- Web chat for asking questions
- Specific query formats: "What's stuck?", "Show risks", etc.
- API for programmatic access
- Memory that remembers trends over time

---

## Project Structure

```
PM-Status-Agent/
├── Core Agent
│   ├── pm_agent.py              # LangGraph workflow (fetch→analyze→record→report)
│   ├── pm_integrations.py       # Jira, Asana, Notion connectors
│   └── memory_store.py          # Trend tracking & persistent memory
│
├── Web Interface
│   ├── app.py                   # Flask API server
│   ├── templates/index.html     # Interactive web UI
│   └── static/                  # (assets, if needed)
│
├── Configuration
│   ├── .env                     # API keys & settings
│   ├── requirements.txt         # Python dependencies
│   └── .gitignore              # (recommended)
│
├── Data Storage
│   └── memory/                  # Auto-created on first run
│       ├── snapshots.json       # Weekly snapshots
│       ├── trends.json          # Calculated trends
│       └── stuck_items.json     # Chronic blocker tracking
│
└── Documentation
    ├── README.md                # Full documentation
    ├── QUICKSTART.md            # 5-minute setup guide
    ├── SAMPLE_REPORT.md         # Example output
    └── PROJECT_OVERVIEW.md      # This file
```

---

## How It Works

### Agent Flow
```
START
  ↓
[Fetch] - Pulls data from Jira, Asana, Notion
  ↓
[Analyze] - Calculates metrics, identifies blockers
  ↓
[Record] - Saves snapshot for trend analysis
  ↓
[Report] - Generates requested report format
  ↓
END
```

### Memory System
```
Weekly Snapshots (52-week rolling window)
  ↓
Trend Analysis (health, velocity, blockers)
  ↓
Chronic Blocker Detection (stuck 2+ weeks)
  ↓
Available for queries ("What's been stuck?")
```

### Blocker Detection Pipeline
```
Raw Data from Platforms
  ↓
Extract Blocking Relationships
  ↓
Identify Long-Stuck Items
  ↓
Flag Overdue & At-Risk
  ↓
Score by Priority & Duration
  ↓
Ranked Blocker List
```

---

## Key Capabilities

### 1. Real-Time Status Dashboard
```
Health Score: 72% (At Risk) 📈 improving
Blockers: 5 (1 critical, 4 high)
Completion: 37/51 items done
Status: On Track overall
```

### 2. Smart Blocker Detection

**Automatically Finds:**
- Items blocked by dependencies (e.g., "Task A blocked by Task B")
- Stuck tasks (in progress 5+ days with no movement)
- Overdue tasks (past due date)
- At-risk items (flagged in Asana/Notion)
- External blockers (waiting on vendor, external team)

**Example:**
```
Blocker: "Set up payment webhooks" (Jira)
Type: Stuck in progress
Days Stuck: 7
Priority: High
Reason: Waiting for API documentation from vendor
```

### 3. Trend Analysis

**Tracks Over Time:**
- Health score: 80% → 60% → 72% (downtrend recovered)
- Velocity: 12 items → 8 items → 10 items (dip then recovery)
- Blocker count: 3 → 5 → 5 (elevated, stable)

**Identifies Patterns:**
- Which blockers recur?
- Are we improving or declining?
- Which weeks were problematic?
- What's trending in the right direction?

### 4. Chronic Issue Detection

**Finds Items Stuck Multiple Weeks:**
```
"Set up payment webhooks" stuck 2 weeks
  - First seen: Week 33
  - Still blocked: Week 34
  - Action: Escalate or replan
```

### 5. Risk Flagging

**Automatic Alerts:**
- 🔴 Health <60% = Critical
- 🟡 Health 60-75% = At Risk  
- 🟡 Blockers increasing = Trend alert
- 🟡 Item stuck 2+ weeks = Chronic issue
- 🔴 Critical path blocked = Timeline risk

---

## Usage Scenarios

### For Program Managers
**Use Case:** Weekly status update to leadership

```bash
# Generate comprehensive report
curl http://localhost:5000/api/report/weekly

# Get risk assessment
curl http://localhost:5000/api/report/risk

# Email the report
# (integrate with email service)
```

### For Engineering Leads
**Use Case:** Sprint planning with blocker insight

```python
from pm_agent import run_pm_agent

# Find what's impacting the team
result = run_pm_agent("What's blocking the payment team?")
print(result["report"])

# Or check chronic issues
from memory_store import ProjectMemory
memory = ProjectMemory()
stuck = memory.find_chronic_blockers(min_weeks=2)
# Address in retrospective
```

### For Teams
**Use Case:** Daily standups with blocker visibility

```bash
# Quick status check
curl http://localhost:5000/api/status
# Returns: health score, blocker count, trend

# In standup
"We have 5 blockers, 1 critical. Health declining.
 Payment work stuck 7 days - needs escalation."
```

### For Consultants/Delivery Managers
**Use Case:** Client project tracking

```
Client sees: Health score 72%, 5 blockers, improving trend
PM can answer: "This has been stuck since week 33"
Report includes: Risk flags, team impact, recommendations
```

---

## Integration Points

### Add New Platform
```python
# In pm_integrations.py
class GitHubIntegration:
    def get_issues(self):
        # Fetch from GitHub Projects API
        return {"platform": "GitHub", "issues": [...]}

# Update fetch_all_statuses() to include GitHub
```

### Integrate with Slack
```python
# In app.py
from slack_sdk import WebClient

@app.route("/slack/command", methods=["POST"])
def slack_command():
    query = request.form.get("text")
    result = run_pm_agent(query)
    return result["report"]

# Slack: /status-agent "What's blocking?"
```

### Schedule with n8n (Low-Code)
```
[Cron: Every Monday 9am]
  → [HTTP: Call /api/report/weekly]
  → [Transform: Format for email]
  → [Email: Send to team]
  → [Slack: Post summary]
```

### Use with External Analytics
```python
# Log metrics for dashboards
for snapshot in memory.snapshots:
    log_metric("health_score", snapshot["summary"]["health"])
    log_metric("blocker_count", snapshot["summary"]["blockers"])

# Query in Grafana, DataDog, etc.
```

---

## What Makes This Production-Ready

✅ **Robust Data Handling**
- Graceful mock fallback if APIs unavailable
- Error handling and logging
- Persistent memory (JSON files)

✅ **Scalability**
- Stateless API (can run multiple instances)
- Configurable via environment variables
- Supports adding new platforms

✅ **User-Friendly**
- Web interface requires zero setup beyond running
- Natural language queries
- Mobile-responsive design

✅ **Team-Friendly**
- Detailed trend analysis
- Risk flagging
- Actionable insights

✅ **Maintainable Code**
- Clear separation of concerns
- Well-documented
- Easy to extend

---

## Quick Wins

Run this now to see value immediately:

1. **Use Mock Data**
```bash
python app.py
# No API keys needed - comes with sample data
```

2. **Ask a Question**
```
"What's been stuck for multiple weeks?"
→ Report on chronic blockers
```

3. **Check Health**
```
Click "Current Status" 
→ See health score, trend, risk level
```

4. **Generate Report**
```
Click "Weekly Report"
→ Full status for leadership
```

5. **Add Your Data**
```
Get API keys
Update .env
Update pm_integrations.py
→ Running against real projects
```

---

## Customization Ideas

**For Your Team:**
- Adjust health score thresholds
- Add custom blocker types
- Change report format/style
- Add team/project filtering
- Custom risk scoring

**For Your Process:**
- Weekly snapshots (already built in)
- Integration with your standup process
- Automated escalation for critical blockers
- Trend-based sprint planning

**For Your Metrics:**
- Add velocity targets
- Track blockers by root cause
- Measure blocker resolution time
- Compare across sprints/teams

---

## Files to Review

| File | What To Know |
|------|--------------|
| **pm_agent.py** | Main orchestration - shows the workflow |
| **pm_integrations.py** | Platform connectors - extend here for new tools |
| **memory_store.py** | Trend engine - core intelligence lives here |
| **app.py** | API endpoints - add new endpoints here |
| **templates/index.html** | Web UI - customize dashboard here |
| **SAMPLE_REPORT.md** | Example output - see what it generates |

---

## Next Steps

1. **Immediate:** Run `python app.py` and open http://localhost:5000
2. **This week:** Add real API keys and connect to your platforms
3. **Next week:** Schedule weekly agent runs for automated reporting
4. **Ongoing:** Customize reports and dashboards for your team

---

## Success Metrics

You'll know it's working when:
- ✅ Team asks "What's blocking X?" and you have the answer
- ✅ You catch chronic issues before they become major delays
- ✅ Health trends help predict sprint success
- ✅ Leaders trust the automated weekly report
- ✅ Fewer "surprise" blockers in standups

---

## Support & Customization

This is your foundation. Extend it for:
- Additional PM tools (Linear, Monday, etc.)
- Custom metrics for your org
- Advanced visualizations
- Integration with other systems
- Team-specific dashboards

Start with the code as-is, then build from there based on your needs!

---

**You're ready to build the agent every PM has always wanted.** 🚀
