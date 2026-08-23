# Quick Start Guide

Get Status Manager running in 5 minutes!

## 1️⃣ Install & Setup

```bash
# Navigate to project
cd PM-Status-Agent

# Install dependencies
pip install -r requirements.txt

# Create/configure .env
# (Already provided with defaults - add your API keys for real data)
```

## 2️⃣ Run the Web Interface

```bash
python app.py
```

Then open your browser to: **http://localhost:5000**

You'll see:
- Real-time health score
- Active blocker count
- Quick action buttons
- Query interface for asking questions

## 3️⃣ Try These Queries

In the agent interface, try asking:

**Status Questions:**
- "Generate weekly status report"
- "What's our current health?"

**Blocker Questions:**
- "What's blocked?"
- "What items are stuck?"
- "What's been stuck for multiple weeks?"

**Risk Questions:**
- "Show me risks"
- "What's at critical risk?"
- "Which tasks are overdue?"

**Trend Questions:**
- "How's our velocity?"
- "Show week-over-week trends"
- "Is health improving?"

## 4️⃣ Use the API (Programmatic Access)

```python
from pm_agent import run_pm_agent

# Get a status report
result = run_pm_agent("Generate weekly status report")
print(result["report"])

# Get memory summary
from memory_store import ProjectMemory
memory = ProjectMemory()
stuck = memory.find_chronic_blockers(min_weeks=2)
print(f"Items stuck 2+ weeks: {len(stuck)}")
```

## 5️⃣ Integrate Real Data

To connect real project management tools:

### Jira
1. Get API token from [id.atlassian.com](https://id.atlassian.com/manage-profile/security/api-tokens)
2. Update `.env`:
```
JIRA_API_TOKEN=your_token
JIRA_BASE_URL=https://your-company.atlassian.net
```
3. In `pm_integrations.py`, replace mock data with real API calls

### Asana
1. Create API token in Asana Settings
2. Update `.env`:
```
ASANA_API_TOKEN=your_token
```
3. Implement real API calls in `pm_integrations.py`

### Notion
1. Create integration at [notion.so/my-integrations](https://www.notion.so/my-integrations)
2. Update `.env`:
```
NOTION_API_TOKEN=your_token
```
3. Implement database queries in `pm_integrations.py`

## Key Features Explained

### Health Score
- **Green (80%+):** Project on track ✅
- **Yellow (60-79%):** Some risks to address ⚠️
- **Red (<60%):** Critical issues need attention 🔴

### Blockers
Automatically detected:
- **Dependency Blocked:** Task blocked by another task
- **Stuck in Progress:** Item in progress 5+ days
- **Overdue:** Task past due date
- **At Risk:** Flagged as at-risk in PM tool
- **External Blocker:** Waiting on something outside the team

### Memory
Records snapshots weekly to track:
- Health score trends
- Completion velocity
- Recurring blocker patterns
- Items stuck multiple weeks (chronic issues)

## Sample Data

The agent comes with sample mock data so you can:
- See all features in action
- Understand the report formats
- Test without API keys

To see it in action:
1. Run `python app.py`
2. Click "Weekly Report" button
3. Review the generated status report

## Architecture Overview

```
┌─────────────────────────────────────────┐
│     Web Interface (Browser)              │
│  - Real-time metrics                    │
│  - Query chat                           │
│  - Report buttons                       │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│     Flask API Server (app.py)           │
│  - /api/status (metrics)                │
│  - /api/query (chat)                    │
│  - /api/report/* (reports)              │
│  - /api/memory (trends)                 │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│     PM Agent (pm_agent.py)              │
│  - LangGraph workflow                   │
│  - Fetch → Analyze → Record → Report    │
└──────────────────┬──────────────────────┘
    ┌──────────────┼──────────────┐
    ▼              ▼              ▼
┌─────────┐  ┌───────────┐  ┌──────────┐
│  Jira   │  │  Asana    │  │  Notion  │
│ Sprint  │  │ Projects  │  │  Pages   │
└─────────┘  └───────────┘  └──────────┘
    ▼              ▼              ▼
┌──────────────────────────────────────┐
│      Data Integration Layer           │
│  (pm_integrations.py)                 │
│  - Fetch platform data                │
│  - Extract blockers                   │
│  - Aggregate status                   │
└──────────────────┬───────────────────┘
                   │
┌──────────────────▼───────────────────┐
│      Memory System (memory_store.py)  │
│  - Weekly snapshots                   │
│  - Trend calculation                  │
│  - Chronic blocker tracking           │
│  - Persistent JSON storage            │
└───────────────────────────────────────┘
```

## Troubleshooting

**No data showing?**
- Check Flask console for errors
- Verify .env has GROQ_API_KEY
- The agent uses mock data by default

**Want real platform data?**
- Add API tokens to .env
- Update pm_integrations.py to call real APIs
- Test with individual platform first

**Memory not updating?**
- Snapshots save to `memory/` directory
- Check that directory exists and is writable
- Try running the agent twice (once to record, once to query)

**Port already in use?**
```bash
# Change port
export PORT=5001
python app.py
```

## Next Steps

1. **Try the web interface** - Click around, test queries
2. **Review SAMPLE_REPORT.md** - See what output looks like
3. **Add real API keys** - Connect to your actual tools
4. **Schedule weekly runs** - Set up cron/n8n for automation
5. **Customize for your team** - Adjust thresholds and report types

## Files You'll Care About

| File | Purpose |
|------|---------|
| `app.py` | Flask server + API endpoints |
| `pm_agent.py` | Main LangGraph agent logic |
| `pm_integrations.py` | Platform data fetching |
| `memory_store.py` | Trend tracking |
| `templates/index.html` | Web UI |
| `.env` | Configuration (add your API keys) |
| `memory/` | Persistent storage (auto-created) |

## Tips

**For Program Managers:**
- Use weekly reports for status updates to leadership
- Reference risk flags in planning discussions
- Track chronic blockers as team improvements

**For Engineers:**
- Query specific blockers affecting your work
- Use trend data for sprint planning
- Identify bottlenecks and dependencies

**For Team Leads:**
- Monitor health score weekly
- Act on chronic blockers
- Use reports in retrospectives

---

Need help? Check README.md for detailed docs!
