"""LangGraph-based Project Management Status Agent."""

from typing import TypedDict, Any, Dict
from datetime import datetime
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.tools import Tool
from langgraph.graph import StateGraph, END
import pm_integrations as integrations
from memory_store import ProjectMemory

load_dotenv()

# Agent state definition
class AgentState(TypedDict):
    query: str
    all_statuses: Dict[str, Any]
    blockers: list
    memory: ProjectMemory
    analysis: Dict[str, Any]
    report: str


# Initialize LLM
llm = ChatGroq(model="gemma2-9b-it", temperature=0.7)

# Initialize memory
memory = ProjectMemory("memory")


def fetch_statuses_node(state: AgentState) -> AgentState:
    """Fetch current status from all platforms."""
    state["all_statuses"] = integrations.fetch_all_statuses()
    state["blockers"] = integrations.extract_blockers(state["all_statuses"])
    state["memory"] = memory
    return state


def analyze_node(state: AgentState) -> AgentState:
    """Analyze the current state and trends."""
    statuses = state["all_statuses"]["sources"]
    blockers = state["blockers"]

    # Calculate metrics
    jira_stats = statuses.get("jira", {}).get("stats", {})
    asana_stats = statuses.get("asana", {}).get("stats", {})

    analysis = {
        "timestamp": datetime.now().isoformat(),
        "total_blockers": len(blockers),
        "blocker_summary": summarize_blockers(blockers),
        "jira_progress": {
            "done": jira_stats.get("done", 0),
            "total": jira_stats.get("total", 0),
            "percentage": (
                jira_stats.get("done", 0) / jira_stats.get("total", 1) * 100
                if jira_stats.get("total", 0) > 0
                else 0
            ),
        },
        "asana_progress": {
            "completed": asana_stats.get("completed", 0),
            "total": asana_stats.get("total", 0),
            "at_risk": asana_stats.get("at_risk", 0),
            "percentage": (
                asana_stats.get("completed", 0) / asana_stats.get("total", 1) * 100
                if asana_stats.get("total", 0) > 0
                else 0
            ),
        },
        "health_score": memory.get_health_score(),
        "blocker_analysis": memory.get_blocker_analysis(),
    }

    state["analysis"] = analysis
    return state


def record_memory_node(state: AgentState) -> AgentState:
    """Record snapshot in memory for trend analysis."""
    memory.record_weekly_snapshot(state["all_statuses"], state["blockers"])
    state["memory"] = memory
    return state


def generate_report_node(state: AgentState) -> AgentState:
    """Generate weekly status report."""
    analysis = state["analysis"]
    blockers = state["blockers"]
    query = state["query"]

    # Build report based on query
    if "stuck" in query.lower():
        report = generate_stuck_items_report(memory)
    elif "risk" in query.lower() or "flag" in query.lower():
        report = generate_risk_report(analysis, blockers)
    elif "trend" in query.lower() or "week" in query.lower():
        report = generate_trend_report(memory, analysis)
    else:
        report = generate_full_report(analysis, blockers, memory)

    state["report"] = report
    return state


# Helper functions
def summarize_blockers(blockers: list) -> Dict[str, Any]:
    """Summarize blockers by type and source."""
    by_type = {}
    by_source = {}

    for blocker in blockers:
        blocker_type = blocker.get("type", "unknown")
        source = blocker.get("source", "unknown")

        by_type[blocker_type] = by_type.get(blocker_type, 0) + 1
        by_source[source] = by_source.get(source, 0) + 1

    return {"by_type": by_type, "by_source": by_source, "total": len(blockers)}


def generate_full_report(analysis: Dict, blockers: list, mem: ProjectMemory) -> str:
    """Generate comprehensive weekly status report."""
    health = analysis["health_score"]
    jira_prog = analysis["jira_progress"]
    asana_prog = analysis["asana_progress"]
    blocker_analysis = analysis["blocker_analysis"]

    report = f"""
# Weekly Project Status Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Health Overview
- Overall Health: {health['score']}% ({health['status']}) {health['trend']}
- Completed Items: {health['completed']}/{health['total_items']}
- Total Blockers: {analysis['total_blockers']}

## Platform Progress

### Jira Sprint
- Completion: {jira_prog['percentage']:.1f}% ({jira_prog['done']}/{jira_prog['total']} done)
- Status: {'On Track' if jira_prog['percentage'] >= 70 else 'At Risk' if jira_prog['percentage'] >= 50 else 'Critical'}

### Asana Projects
- Completion: {asana_prog['percentage']:.1f}% ({asana_prog['completed']}/{asana_prog['total']} completed)
- At Risk: {asana_prog['at_risk']} tasks

## BLOCKERS ({len(blockers)} total)
{blocker_analysis['recommendation']}

### Top Blockers:
"""
    for i, blocker in enumerate(blockers[:5], 1):
        report += f"\n{i}. {blocker['title']} ({blocker['source']})\n"
        report += f"   Type: {blocker['type']}\n"
        report += f"   Days Blocked: {blocker.get('days_blocked', 0)}\n"
        report += f"   Assignee: {blocker.get('assignee', 'Unassigned')}\n"

    chronic = mem.find_chronic_blockers(min_weeks=2)
    if chronic:
        report += f"\n## CHRONIC ISSUES ({len(chronic)} items stuck 2+ weeks)\n"
        for item in chronic[:3]:
            report += f"\n- {item['title']} - {item['weeks_stuck']} weeks\n"
            report += f"  First seen: {item['first_seen']}\n"

    report += f"\n## Risk Flags\n"
    if health['score'] < 60:
        report += "[CRITICAL] Health score below 60%\n"
    if blocker_analysis['trend'] == 'increasing':
        report += "[WARNING] Blockers increasing\n"
    if chronic and len(chronic) > 3:
        report += f"[ALERT] {len(chronic)} items stuck multiple weeks\n"
    if jira_prog['percentage'] < 50:
        report += "[ALERT] Jira sprint significantly behind\n"

    return report


def generate_risk_report(analysis: Dict, blockers: list) -> str:
    """Generate risk-focused report."""
    report = "# Risk Assessment Report\n\n"

    health = analysis["health_score"]
    if health['score'] < 60:
        report += f"[CRITICAL RISK] Project health at {health['score']}%\n\n"
    elif health['score'] < 75:
        report += f"[MEDIUM RISK] Project health at {health['score']}%\n\n"

    blocker_analysis = analysis["blocker_analysis"]
    if blocker_analysis['trend'] == 'increasing':
        report += f"Blocker count increasing: {blocker_analysis['current_blockers']} (avg: {blocker_analysis['average']})\n"

    # Risk by priority
    critical_blockers = [b for b in blockers if b.get("priority") == "Critical"]
    high_blockers = [b for b in blockers if b.get("priority") == "High"]

    report += f"\nCritical Blockers: {len(critical_blockers)}\n"
    for b in critical_blockers[:3]:
        report += f"- {b['title']} ({b['source']})\n"

    report += f"\nHigh Priority Blockers: {len(high_blockers)}\n"

    return report


def generate_stuck_items_report(mem: ProjectMemory) -> str:
    """Report on items stuck multiple weeks."""
    chronic = mem.find_chronic_blockers(min_weeks=2)

    report = "# Items Stuck Multiple Weeks\n\n"

    if not chronic:
        report += "No items stuck for 2+ weeks. Great progress!\n"
        return report

    report += f"Found {len(chronic)} items stuck in blockers for 2+ weeks:\n\n"

    for item in chronic:
        report += f"{item['title']}\n"
        report += f"- Source: {item['source']}\n"
        report += f"- Type: {item['type']}\n"
        report += f"- Weeks Stuck: {item['weeks_stuck']}\n"
        report += f"- First Seen: {item['first_seen']}\n"
        report += f"- Timeline: {', '.join(item['weeks'][:4])}{'...' if len(item['weeks']) > 4 else ''}\n\n"

    return report


def generate_trend_report(mem: ProjectMemory, analysis: Dict) -> str:
    """Generate week-over-week trend report."""
    report = "# Week-over-Week Trends\n\n"

    health_history = mem.trends.get("health_score_history", [])
    if health_history:
        report += "Health Score Trend\n"
        for entry in health_history[-4:]:
            bar = "[" + ("=" * int(entry["health"] / 10)) + (" " * (10 - int(entry["health"] / 10))) + "]"
            report += f"{entry['week']}: {bar} {entry['health']:.1f}%\n"

    blocker_trend = mem.trends.get("blocker_trends", [])
    if blocker_trend:
        report += "\nBlocker Count Trend\n"
        for entry in blocker_trend[-4:]:
            report += f"{entry['week']}: {entry['blocker_count']} blockers\n"

    velocity = mem.trends.get("velocity_history", [])
    if velocity:
        report += "\nCompletion Velocity\n"
        for entry in velocity[-4:]:
            report += f"{entry['week']}: {entry['completed']} items completed\n"

    return report


# Build the LangGraph
def create_pm_agent():
    """Create the PM status agent graph."""
    graph = StateGraph(AgentState)

    graph.add_node("fetch_statuses", fetch_statuses_node)
    graph.add_node("analyze", analyze_node)
    graph.add_node("record_memory", record_memory_node)
    graph.add_node("generate_report", generate_report_node)

    graph.add_edge("fetch_statuses", "analyze")
    graph.add_edge("analyze", "record_memory")
    graph.add_edge("record_memory", "generate_report")
    graph.add_edge("generate_report", END)

    graph.set_entry_point("fetch_statuses")

    return graph.compile()


def run_pm_agent(query: str = "Generate weekly status report") -> Dict[str, Any]:
    """Run the PM agent."""
    agent = create_pm_agent()

    initial_state = AgentState(
        query=query,
        all_statuses={},
        blockers=[],
        memory=memory,
        analysis={},
        report=""
    )

    result = agent.invoke(initial_state)

    return {
        "query": result["query"],
        "timestamp": datetime.now().isoformat(),
        "blockers": result["blockers"],
        "analysis": result["analysis"],
        "report": result["report"],
        "memory_summary": memory.generate_memory_summary()
    }


if __name__ == "__main__":
    # Test the agent
    import json

    result = run_pm_agent("Generate weekly status report")
    print(result["report"])
    print("\n---\n")
    print(result["memory_summary"])
