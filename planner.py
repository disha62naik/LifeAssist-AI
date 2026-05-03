"""
Planner Module
Generates a structured daily schedule with breaks.
"""
from datetime import datetime, timedelta
import math


def generate_plan(tasks: list, start_time: str, available_hours: float) -> dict:
    """
    Distributes tasks evenly within available_hours starting at start_time.
    Inserts a 15-min break every 2 tasks and a 30-min lunch if > 4 hours.
    """
    if not tasks:
        return {"error": "No tasks provided."}

    try:
        current = datetime.strptime(start_time, "%H:%M")
    except ValueError:
        current = datetime.strptime("09:00", "%H:%M")

    end_time = current + timedelta(hours=available_hours)
    total_minutes = available_hours * 60

    # Calculate break time
    short_breaks = math.floor(len(tasks) / 2)
    long_break = 1 if available_hours > 4 else 0
    break_minutes = short_breaks * 15 + long_break * 30

    work_minutes = max(total_minutes - break_minutes, 30)
    minutes_per_task = round(work_minutes / len(tasks))

    schedule = []
    task_count = 0

    for task in tasks:
        task_start = current.strftime("%I:%M %p")
        current += timedelta(minutes=minutes_per_task)
        task_end = current.strftime("%I:%M %p")

        schedule.append({
            "type": "task",
            "label": task,
            "start": task_start,
            "end": task_end,
            "duration": minutes_per_task
        })
        task_count += 1

        # Insert break after every 2 tasks
        if task_count % 2 == 0 and task_count < len(tasks):
            if long_break and task_count == len(tasks) // 2:
                break_duration = 30
                break_label = "Lunch Break"
            else:
                break_duration = 15
                break_label = "Short Break ☕"

            break_start = current.strftime("%I:%M %p")
            current += timedelta(minutes=break_duration)
            break_end = current.strftime("%I:%M %p")
            schedule.append({
                "type": "break",
                "label": break_label,
                "start": break_start,
                "end": break_end,
                "duration": break_duration
            })

    return {
        "schedule": schedule,
        "start": datetime.strptime(start_time, "%H:%M").strftime("%I:%M %p"),
        "end": end_time.strftime("%I:%M %p"),
        "total_tasks": len(tasks),
        "task_duration": minutes_per_task
    }