"""Memory system to track week-over-week trends and historical data."""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any


class ProjectMemory:
    """Persistent memory for project status trends."""

    def __init__(self, memory_dir: str = "memory"):
        self.memory_dir = memory_dir
        os.makedirs(memory_dir, exist_ok=True)
        self.snapshots_file = os.path.join(memory_dir, "snapshots.json")
        self.trends_file = os.path.join(memory_dir, "trends.json")
        self.stuck_items_file = os.path.join(memory_dir, "stuck_items.json")
        self.load()

    def load(self):
        """Load all memory from disk."""
        self.snapshots = []
        self.trends = {
            "health_score_history": [],
            "velocity_history": [],
            "blocker_trends": [],
            "recurring_blockers": []
        }
        self.stuck_items = {}

        if os.path.exists(self.snapshots_file):
            try:
                with open(self.snapshots_file) as f:
                    self.snapshots = json.load(f)
            except (json.JSONDecodeError, IOError):
                pass

        if os.path.exists(self.trends_file):
            try:
                with open(self.trends_file) as f:
                    self.trends = json.load(f)
            except (json.JSONDecodeError, IOError):
                pass

        if os.path.exists(self.stuck_items_file):
            try:
                with open(self.stuck_items_file) as f:
                    self.stuck_items = json.load(f)
            except (json.JSONDecodeError, IOError):
                pass

    def save(self):
        """Save all memory to disk."""
        with open(self.snapshots_file, "w") as f:
            json.dump(self.snapshots, f, indent=2)

        with open(self.trends_file, "w") as f:
            json.dump(self.trends, f, indent=2)

        with open(self.stuck_items_file, "w") as f:
            json.dump(self.stuck_items, f, indent=2)

    def record_weekly_snapshot(self, statuses: Dict[str, Any], blockers: List[Dict[str, Any]]):
        """Record a snapshot of the week's status."""
        week_num = self._get_week_key()

        snapshot = {
            "week": week_num,
            "date": datetime.now().isoformat(),
            "blockers_count": len(blockers),
            "blocker_details": blockers,
            "jira_stats": statuses["sources"].get("jira", {}).get("stats", {}),
            "asana_stats": statuses["sources"].get("asana", {}).get("stats", {}),
            "notion_count": len(statuses["sources"].get("notion", {}).get("initiatives", []))
        }

        self.snapshots.append(snapshot)
        # Keep last 52 weeks (1 year of history)
        if len(self.snapshots) > 52:
            self.snapshots = self.snapshots[-52:]

        self._update_stuck_items(blockers)
        self._update_trends()
        self.save()

    def _get_week_key(self) -> str:
        """Get year-week key (e.g., '2026-W34')."""
        return datetime.now().strftime("%Y-W%V")

    def _update_stuck_items(self, current_blockers: List[Dict[str, Any]]):
        """Track items that have been blockers across multiple weeks."""
        week = self._get_week_key()

        for blocker in current_blockers:
            blocker_id = f"{blocker['source']}-{blocker['id']}"

            if blocker_id not in self.stuck_items:
                self.stuck_items[blocker_id] = {
                    "id": blocker_id,
                    "source": blocker["source"],
                    "title": blocker["title"],
                    "type": blocker.get("type"),
                    "first_seen_week": week,
                    "weeks_blocked": [],
                }

            if week not in self.stuck_items[blocker_id]["weeks_blocked"]:
                self.stuck_items[blocker_id]["weeks_blocked"].append(week)

    def _update_trends(self):
        """Update trend analysis from snapshots."""
        if not self.snapshots:
            return

        # Health score: ratio of completed to total
        self.trends["health_score_history"] = []
        for snapshot in self.snapshots[-12:]:  # Last 12 weeks
            jira = snapshot.get("jira_stats", {})
            asana = snapshot.get("asana_stats", {})

            total = jira.get("total", 0) + asana.get("total", 0)
            done = jira.get("done", 0) + asana.get("completed", 0)

            health = (done / total * 100) if total > 0 else 0
            self.trends["health_score_history"].append({
                "week": snapshot["week"],
                "health": round(health, 1),
                "total_items": total,
                "completed": done
            })

        # Velocity: items completed per week
        self.trends["velocity_history"] = []
        for snapshot in self.snapshots[-8:]:  # Last 8 weeks
            asana = snapshot.get("asana_stats", {})
            self.trends["velocity_history"].append({
                "week": snapshot["week"],
                "completed": asana.get("completed", 0)
            })

        # Blocker trends
        self.trends["blocker_trends"] = []
        for snapshot in self.snapshots[-4:]:  # Last 4 weeks
            self.trends["blocker_trends"].append({
                "week": snapshot["week"],
                "blocker_count": snapshot["blockers_count"]
            })

    def find_chronic_blockers(self, min_weeks: int = 2) -> List[Dict[str, Any]]:
        """Find items stuck for multiple weeks."""
        chronic = []
        for item_id, item_data in self.stuck_items.items():
            weeks_stuck = len(item_data["weeks_blocked"])
            if weeks_stuck >= min_weeks:
                chronic.append({
                    "id": item_data["id"],
                    "title": item_data["title"],
                    "source": item_data["source"],
                    "type": item_data["type"],
                    "weeks_stuck": weeks_stuck,
                    "first_seen": item_data["first_seen_week"],
                    "weeks": item_data["weeks_blocked"]
                })

        return sorted(chronic, key=lambda x: x["weeks_stuck"], reverse=True)

    def get_health_score(self) -> Dict[str, Any]:
        """Get current health score and trend."""
        if not self.trends["health_score_history"]:
            return {"score": 0, "trend": "unknown", "status": "insufficient_data"}

        recent = self.trends["health_score_history"][-1]
        score = recent["health"]

        if len(self.trends["health_score_history"]) > 1:
            previous = self.trends["health_score_history"][-2]
            if score > previous["health"]:
                trend = "📈 improving"
            elif score < previous["health"]:
                trend = "📉 declining"
            else:
                trend = "➡️ stable"
        else:
            trend = "➡️ stable"

        if score >= 75:
            status = "✅ excellent"
        elif score >= 60:
            status = "⚠️ at_risk"
        else:
            status = "🔴 critical"

        return {
            "score": round(score, 1),
            "trend": trend,
            "status": status,
            "total_items": recent["total_items"],
            "completed": recent["completed"]
        }

    def get_blocker_analysis(self) -> Dict[str, Any]:
        """Analyze blocker patterns."""
        if not self.trends["blocker_trends"]:
            return {"current": 0, "average": 0, "trend": "stable", "recommendation": "No data yet"}

        recent = self.trends["blocker_trends"][-1]["blocker_count"]
        average = sum(t["blocker_count"] for t in self.trends["blocker_trends"]) / len(
            self.trends["blocker_trends"]
        )

        if recent > average:
            trend = "increasing"
            recommendation = "⚠️ Investigate blockers urgently"
        elif recent < average:
            trend = "decreasing"
            recommendation = "✅ Good progress on blockers"
        else:
            trend = "stable"
            recommendation = "Monitor blocker resolution"

        return {
            "current_blockers": recent,
            "average": round(average, 1),
            "trend": trend,
            "recommendation": recommendation
        }

    def generate_memory_summary(self) -> str:
        """Generate a human-readable memory summary."""
        if not self.snapshots:
            return "📝 No memory records yet. Weekly snapshots will be recorded here."

        health = self.get_health_score()
        blockers = self.get_blocker_analysis()
        chronic = self.find_chronic_blockers(min_weeks=2)

        summary = f"""
## 📊 Project Memory Summary

**Current Status:**
- Health Score: {health['score']}% ({health['status']}) {health['trend']}
- Completed Items: {health['completed']}/{health['total_items']}

**Blockers:**
- Current: {blockers['current_blockers']} blockers
- Average (4-week): {blockers['average']}
- Trend: {blockers['trend']}
- Action: {blockers['recommendation']}

**Chronic Issues (2+ weeks):**
"""
        if chronic:
            for item in chronic[:5]:
                summary += f"\n- **{item['title']}** ({item['source']}) - stuck {item['weeks_stuck']} weeks"
        else:
            summary += "\n- ✅ No chronic blockers detected"

        summary += f"\n\n**Historical Data:** {len(self.snapshots)} weekly snapshots"

        return summary
