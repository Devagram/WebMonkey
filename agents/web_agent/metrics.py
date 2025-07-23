import time
from typing import List, Dict

class ObjectiveMetrics:
    def __init__(self):
        self.records: List[Dict] = []

    def record(self, objective: str, status: str, start_time: float, end_time: float, error: str = None):
        self.records.append({
            "objective": objective,
            "status": status,
            "time_taken": end_time - start_time,
            "error": error
        })

    def analyze(self) -> Dict:
        total = len(self.records)
        successes = sum(1 for r in self.records if r["status"] == "success")
        avg_time = sum(r["time_taken"] for r in self.records) / total if total else 0
        error_count = sum(1 for r in self.records if r["status"] == "error")
        error_types = {}
        for r in self.records:
            if r["error"]:
                error_types[r["error"]] = error_types.get(r["error"], 0) + 1
        insights = {
            "success_rate": successes / total if total else 0,
            "average_time_taken": avg_time,
            "error_recovery_efficiency": (total - error_count) / total if total else 0,
            "common_errors": error_types
        }
        suggestions = []
        if insights["success_rate"] < 0.8:
            suggestions.append("Improve error handling and robustness.")
        if avg_time > 5:
            suggestions.append("Optimize performance to reduce time taken.")
        if error_types:
            suggestions.append(f"Address common errors: {list(error_types.keys())}")
        return {"insights": insights, "suggestions": suggestions}

metrics_tracker = ObjectiveMetrics()

