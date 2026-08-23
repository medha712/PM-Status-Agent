# 📊 Status Manager

An intelligent project management status agent that connects to Jira, Asana, and Notion to provide real-time sprint tracking, blocker identification, and week-over-week trend analysis.

## Features

✅ **Multi-Platform Integration**
- Jira: Sprint status, velocity, and blocking issues
- Asana: Project progress and at-risk tasks
- Notion: Strategic initiatives and status updates

✅ **Smart Blocker Detection**
- Identifies blocked dependencies
- Detects stuck-in-progress items
- Flags overdue and at-risk tasks
- Tracks external blockers

✅ **Trend Analysis & Memory**
- Week-over-week health score tracking
- Velocity trends across 8+ weeks
- Identifies items stuck 2+ sprints (chronic blockers)
- Historical snapshot storage (52-week rolling window)

✅ **Risk-Based Reporting**
- Health score with color-coded status
- Priority-based blocker flagging
- Trend indicators (improving/declining)
- Chronic issue alerts

✅ **Natural Language Queries**
- "What's been stuck for multiple sprints?"
- "Show me risk assessment"
- "What's our weekly status?"
- Ask custom questions about project status

## Installation

### Prerequisites
- Python 3.9+
- Groq API key (for LLM)
- Optional: Jira, Asana, Notion API keys

### Setup

1. **Clone/Create the project:**
```bash
cd PM-Status-Agent
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables:**
```bash
cp .env.example .env
# Edit .env with your API keys
```

4. **Run the agent:**
```bash
# Web interface
python app.py

# Or CLI
python pm_agent.py
```

## Configuration

### Groq LLM Setup
1. Get your API key from [console.groq.com](https://console.groq.com)
2. Add to `.env`:
```
GROQ_API_KEY=your_key_here
```

### Jira Integration
1. Create API token at [id.atlassian.com/manage-profile/security/api-tokens](https://id.atlassian.com/manage-profile/security/api-tokens)
2. Configure in `.env`:
```
JIRA_API_TOKEN=your_token_here
JIRA_BASE_URL=https://your-company.atlassian.net
```

### Asana Integration
1. Create API token in Asana Settings → Developer Apps
2. Add to `.env`:
```
ASANA_API_TOKEN=your_token_here
```

### Notion Integration
1. Create integration at [notion.so/my-integrations](https://www.notion.so/my-integrations)
2. Add to `.env`:
```
NOTION_API_TOKEN=your_token_here
```

## Usage

### Web Interface
```bash
python app.py
# Open http://localhost:5000
```

**Features:**
- Real-time health score and blocker count
- One-click report generation
- Natural language query box
- Memory summary with chronic blockers
- Trend visualization

### CLI Usage
```python
from pm_agent import run_pm_agent

# Get full weekly status
result = run_pm_agent("Generate weekly status report")
print(result["report"])

# Query specific questions
result = run_pm_agent("What's been stuck for multiple weeks?")
print(result["report"])

# Check memory trends
from memory_store import ProjectMemory
memory = ProjectMemory()
stuck = memory.find_chronic_blockers(min_weeks=2)
print(f"Found {len(stuck)} chronic issues")
```

### API Endpoints

**Get Current Status:**
```bash
curl http://localhost:5000/api/status
```

**Query the Agent:**
```bash
curl -X POST http://localhost:5000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is at risk?"}'
```

**Get Memory Summary:**
```bash
curl http://localhost:5000/api/memory
```

**Generate Reports:**
```bash
# Weekly report
curl http://localhost:5000/api/report/weekly

# Risk assessment
curl http://localhost:5000/api/report/risk

# Stuck items
curl http://localhost:5000/api/report/stuck
```

**Get Trend Data:**
```bash
curl http://localhost:5000/api/trends
```

**Find Stuck Items:**
```bash
curl http://localhost:5000/api/stuck-items?weeks=2
```

## Project Structure

```
PM-Status-Agent/
├── pm_agent.py              # Main LangGraph agent
├── pm_integrations.py       # Jira, Asana, Notion connectors
├── memory_store.py          # Trend tracking and memory
├── app.py                   # Flask web server
├── templates/
│   └── index.html          # Web interface
├── memory/                 # Persistent memory storage
│   ├── snapshots.json      # Weekly snapshots
│   ├── trends.json         # Calculated trends
│   └── stuck_items.json    # Chronic blocker tracking
├── requirements.txt        # Dependencies
├── .env                    # Configuration
└── README.md              # This file
```

## How It Works

### Agent Architecture
1. **Fetch Node:** Pulls data from all platforms
2. **Analyze Node:** Calculates metrics and identifies blockers
3. **Record Node:** Saves snapshot to memory
4. **Report Node:** Generates requested report format

### Memory System
- **Snapshots:** Weekly records of status (52-week rolling)
- **Trends:** Calculated from historical snapshots
- **Stuck Items:** Tracks items in blocker status week-over-week
- **Chronic Blockers:** Items stuck 2+ consecutive weeks

### Blocker Detection
- **Dependency Blocked:** Issues with blocking relationships
- **Stuck in Progress:** Items in progress 5+ days
- **Overdue:** Tasks past their due date
- **At Risk:** Flagged tasks in project tools
- **External Blocker:** Waiting on external resources

## Sample Reports

### Weekly Status Report
```
📊 Weekly Project Status Report
Generated: 2026-08-23 14:30:00

Health Overview
- Overall Health: 72% (⚠️ at_risk) 📈 improving
- Completed Items: 37/51
- Total Blockers: 5

Platform Progress
- Jira Sprint: 66.7% (16/24 done)
- Asana Projects: 65.6% (21/32 completed)

🚨 Blockers (5 total)
Top Blockers:
1. Set up payment webhooks (Jira)
2. Database optimization (Asana)
3. Customer feedback loop (Notion)
```

### Risk Assessment
```
🚨 Risk Assessment Report

🟡 MEDIUM RISK: Project health at 72%

⚠️ Blocker count increasing: 5 (avg: 4.2)

Critical Blockers: 2
- Implement Stripe payment integration
- PostgreSQL version migration
```

### Chronic Blockers Report
```
📌 Items Stuck Multiple Weeks

Found 3 items stuck in blockers for 2+ weeks:

Set up payment webhooks
- Source: Jira
- Type: stuck_in_progress
- Weeks Stuck: 2
- First Seen: 2026-W33
```

## Key Queries

Try these questions with the agent:

- "What's been stuck for more than one sprint?"
- "Show me critical blockers"
- "What's our health score trend?"
- "Which items are at risk?"
- "Generate risk assessment"
- "How's our velocity trending?"
- "What's blocking payment work?"
- "Show chronic issues"

## Integration with n8n (Low-Code)

For teams preferring low-code:

1. Create n8n workflow
2. Use HTTP nodes to fetch data from platforms
3. Connect to PM Status Agent API endpoints
4. Schedule weekly execution with n8n Cron
5. Send reports via email/Slack using n8n integrations

Example n8n workflow:
```
[Cron Trigger] → [Call /api/report/weekly] 
  → [Format for Email] → [Send via Gmail]
```

## Extending the Agent

### Add New Data Source
```python
class SlackIntegration:
    def get_status_updates(self):
        # Fetch from Slack channels
        return {"platform": "Slack", "updates": [...]}

# Update pm_integrations.fetch_all_statuses()
```

### Custom Report Type
```python
def generate_custom_report(analysis, blockers):
    # Your report logic
    return formatted_report

# Update pm_agent.py generate_report_node()
```

### Enhanced Memory
```python
# Add custom trend calculation
def calculate_custom_trend(snapshots):
    # Your trend logic
    return trend_data

# Update memory_store.py _update_trends()
```

## Performance

- **Data Fetch:** ~500ms (mocked) / ~2s (real APIs)
- **Memory Save:** ~100ms per snapshot
- **Report Generation:** ~1s
- **Memory Storage:** ~50KB per 52 weeks

## Deployment

### Docker
```dockerfile
FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "app.py"]
```

### Cloud Platforms
- **Heroku:** Add `Procfile` with `web: gunicorn app:app`
- **AWS/GCP:** Deploy as containerized service
- **Railway/Render:** Direct GitHub integration

### Scheduled Reports
Use n8n, cron, or Cloud Scheduler:
```bash
0 9 * * 1 curl http://localhost:5000/api/report/weekly
```

## Best Practices

1. **Weekly Snapshots:** Set up daily/weekly agent runs for consistent memory
2. **API Rate Limits:** Cache data locally between runs if needed
3. **Alert Thresholds:** Adjust health score and blocker thresholds for your team
4. **Team Sync:** Use reports in weekly standups
5. **Action Items:** Link blockers to resolution owners

## Troubleshooting

**No data appearing?**
- Check API keys in `.env`
- Verify network connectivity
- Check mock data in integrations

**Memory not updating?**
- Ensure snapshots are being recorded (check `memory/` directory)
- Run `memory.record_weekly_snapshot()` explicitly

**Blocker detection missing items?**
- Review blocker extraction logic in `pm_integrations.extract_blockers()`
- Add custom blocker types as needed

**LLM errors?**
- Check Groq API key validity
- Verify API rate limits not exceeded

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review API documentation for your platforms
3. Check memory files in `memory/` directory for debugging
4. Adjust log levels in the code for more detail

## License

Built for Gen Academy. Customize and extend as needed!

---

**Next Steps:**
1. Configure API keys in `.env`
2. Run `python app.py`
3. Open web interface at http://localhost:5000
4. Ask the agent your first question!
