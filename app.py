"""Flask web app for PM Status Agent."""

from flask import Flask, render_template, request, jsonify
from pm_agent import run_pm_agent
from memory_store import ProjectMemory
import json
import os

app = Flask(__name__)
memory = ProjectMemory("memory")


@app.route("/")
def home():
    """Render home page."""
    return render_template("index.html")


@app.route("/api/status", methods=["GET"])
def get_status():
    """Get current project status."""
    try:
        result = run_pm_agent("Generate weekly status report")
        return jsonify({
            "success": True,
            "report": result["report"],
            "blockers": result["blockers"],
            "blockers_count": len(result["blockers"]),
            "health": result["analysis"].get("health_score", {}),
            "timestamp": result["timestamp"]
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/query", methods=["POST"])
def query_agent():
    """Query the agent with a custom question."""
    data = request.json
    query = data.get("query", "Generate weekly status report")

    try:
        result = run_pm_agent(query)
        return jsonify({
            "success": True,
            "report": result["report"],
            "blockers_count": len(result["blockers"]),
            "timestamp": result["timestamp"]
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/memory", methods=["GET"])
def get_memory():
    """Get memory summary."""
    try:
        chronic = memory.find_chronic_blockers(min_weeks=2)
        health = memory.get_health_score()
        blockers = memory.get_blocker_analysis()

        return jsonify({
            "success": True,
            "health_score": health,
            "blocker_analysis": blockers,
            "chronic_blockers": chronic[:10],
            "snapshots": len(memory.snapshots),
            "summary": memory.generate_memory_summary()
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/stuck-items", methods=["GET"])
def get_stuck_items():
    """Get items stuck for multiple weeks."""
    try:
        min_weeks = request.args.get("weeks", 2, type=int)
        stuck = memory.find_chronic_blockers(min_weeks=min_weeks)

        return jsonify({
            "success": True,
            "min_weeks": min_weeks,
            "items": stuck,
            "count": len(stuck)
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/trends", methods=["GET"])
def get_trends():
    """Get trend data."""
    try:
        return jsonify({
            "success": True,
            "health_history": memory.trends.get("health_score_history", []),
            "blocker_trends": memory.trends.get("blocker_trends", []),
            "velocity_history": memory.trends.get("velocity_history", [])
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/report/weekly", methods=["GET"])
def get_weekly_report():
    """Get formatted weekly report."""
    try:
        result = run_pm_agent("Generate weekly status report")
        return jsonify({
            "success": True,
            "report": result["report"],
            "analysis": result["analysis"],
            "timestamp": result["timestamp"]
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/report/risk", methods=["GET"])
def get_risk_report():
    """Get risk-focused report."""
    try:
        result = run_pm_agent("Generate risk assessment report")
        return jsonify({
            "success": True,
            "report": result["report"],
            "timestamp": result["timestamp"]
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/report/stuck", methods=["GET"])
def get_stuck_report():
    """Get report on stuck items."""
    try:
        result = run_pm_agent("What items are stuck for multiple sprints?")
        return jsonify({
            "success": True,
            "report": result["report"],
            "timestamp": result["timestamp"]
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print("🚀 PM Status Agent starting...")
    print(f"📍 Open your browser at: http://localhost:{port}")
    app.run(debug=True, port=port, host="0.0.0.0")
