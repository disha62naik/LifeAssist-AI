"""
Suggestions Module
Rule-based smart suggestions based on productivity score and task data.
"""


def get_suggestions(score: float, completed: int, total: int) -> list:
    suggestions = []
    incomplete = total - completed

    if score >= 85:
        suggestions.append("🌟 Outstanding work! You're in the top performance zone. Keep it up!")
        suggestions.append("Consider mentoring others or taking on stretch goals.")
    elif score >= 70:
        suggestions.append("✅ Great job! You're performing well. Small refinements can push you higher.")
        if incomplete > 0:
            suggestions.append(f"You have {incomplete} task(s) remaining — try tackling them first thing tomorrow.")
    elif score >= 50:
        suggestions.append("📌 You're doing okay, but there's clear room to grow.")
        suggestions.append("Try the Pomodoro technique: 25 min focused work, 5 min break.")
        if incomplete > 2:
            suggestions.append("Break large tasks into smaller sub-tasks to reduce overwhelm.")
    elif score >= 30:
        suggestions.append("⚡ Your productivity is below average. Let's turn this around!")
        suggestions.append("Identify your top 3 priorities each morning and focus only on those.")
        suggestions.append("Minimize distractions: silence notifications during work blocks.")
    else:
        suggestions.append("🚨 Very low productivity detected. Don't be discouraged — start small!")
        suggestions.append("Set just ONE clear goal for tomorrow and achieve it.")
        suggestions.append("Check in with yourself: are you getting enough sleep and breaks?")
        suggestions.append("Consider speaking to a mentor or manager about workload balance.")

    # Universal tips
    if total > 0 and completed / total < 0.5:
        suggestions.append("💡 Tip: You completed less than 50% of tasks. Prioritize ruthlessly next session.")

    if total > 10:
        suggestions.append("📋 You're managing many tasks — consider delegating or deferring lower-priority ones.")

    return suggestions