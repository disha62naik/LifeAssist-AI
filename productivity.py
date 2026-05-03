"""
Productivity Module
Calculates a productivity score (0–100) from task completion and hours worked.
"""


def calculate_productivity(total: int, completed: int, hours: float) -> tuple:
    """
    Returns (score: float, label: str)
    Score formula:
      - Completion rate: 60% weight
      - Efficiency (tasks/hour): 40% weight (benchmarked at 3 tasks/hour = 100%)
    """
    if total == 0 or hours == 0:
        return 0, "No Data"

    completed = min(completed, total)
    completion_rate = completed / total  # 0–1

    tasks_per_hour = completed / hours
    efficiency = min(tasks_per_hour / 3.0, 1.0)  # benchmark: 3 tasks/hour = max

    raw_score = (completion_rate * 0.60 + efficiency * 0.40) * 100
    score = round(raw_score, 1)

    if score >= 85:
        label = "Excellent 🏆"
    elif score >= 70:
        label = "Good 👍"
    elif score >= 50:
        label = "Average 📊"
    elif score >= 30:
        label = "Needs Improvement 📈"
    else:
        label = "Low ⚠️"

    return score, label