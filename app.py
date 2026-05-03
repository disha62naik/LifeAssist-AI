from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json
import os
from modules.decision import evaluate_decision
from modules.planner import generate_plan
from modules.productivity import calculate_productivity
from modules.suggestions import get_suggestions

app = Flask(__name__)
app.secret_key = "lifeassist_secret_2026"

DATA_FILE = "data/users.json"


def load_users():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_users(users):
    with open(DATA_FILE, "w") as f:
        json.dump(users, f, indent=2)


# ──────────────────────── AUTH ────────────────────────

@app.route("/")
def index():
    if "user" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        users = load_users()
        if username in users and users[username]["password"] == password:
            session["user"] = username
            return redirect(url_for("dashboard"))
        error = "Invalid username or password."
    return render_template("login.html", error=error)


@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        users = load_users()
        if username in users:
            error = "Username already exists."
        elif not username or not password:
            error = "All fields are required."
        else:
            users[username] = {
                "password": password,
                "tasks": [],
                "productivity_history": []
            }
            save_users(users)
            session["user"] = username
            return redirect(url_for("dashboard"))
    return render_template("register.html", error=error)


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


# ──────────────────────── DASHBOARD ────────────────────────

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    users = load_users()
    user_data = users.get(session["user"], {})
    tasks = user_data.get("tasks", [])
    history = user_data.get("productivity_history", [])
    avg_score = round(sum(h["score"] for h in history) / len(history), 1) if history else 0
    return render_template("dashboard.html",
                           username=session["user"],
                           tasks=tasks,
                           history=history[-5:],
                           avg_score=avg_score)


# ──────────────────────── DECISION ────────────────────────

@app.route("/decision", methods=["GET", "POST"])
def decision():
    if "user" not in session:
        return redirect(url_for("login"))
    result = None
    if request.method == "POST":
        options_raw = request.form.get("options", "")
        options = [o.strip() for o in options_raw.split(",") if o.strip()]
        criteria = {
            "urgency": int(request.form.get("urgency", 5)),
            "importance": int(request.form.get("importance", 5)),
            "effort": int(request.form.get("effort", 5)),
        }
        result = evaluate_decision(options, criteria)
    return render_template("decision.html", result=result, username=session["user"])


# ──────────────────────── PLANNER ────────────────────────

@app.route("/planner", methods=["GET", "POST"])
def planner():
    if "user" not in session:
        return redirect(url_for("login"))
    schedule = None
    if request.method == "POST":
        tasks_raw = request.form.get("tasks", "")
        tasks = [t.strip() for t in tasks_raw.split(",") if t.strip()]
        start_time = request.form.get("start_time", "09:00")
        available_hours = float(request.form.get("available_hours", 8))
        schedule = generate_plan(tasks, start_time, available_hours)
    return render_template("planner.html", schedule=schedule, username=session["user"])


# ──────────────────────── PRODUCTIVITY ────────────────────────

@app.route("/productivity", methods=["GET", "POST"])
def productivity():
    if "user" not in session:
        return redirect(url_for("login"))
    result = None
    if request.method == "POST":
        total = int(request.form.get("total_tasks", 0))
        completed = int(request.form.get("completed_tasks", 0))
        hours = float(request.form.get("hours_worked", 0))
        score, label = calculate_productivity(total, completed, hours)
        suggestions = get_suggestions(score, completed, total)
        result = {
            "score": score,
            "label": label,
            "suggestions": suggestions,
            "completed": completed,
            "total": total,
            "hours": hours
        }
        # Save to history
        users = load_users()
        users[session["user"]]["productivity_history"].append({
            "score": score,
            "label": label,
            "completed": completed,
            "total": total
        })
        save_users(users)
    return render_template("productivity.html", result=result, username=session["user"])


# ──────────────────────── TASK MANAGER ────────────────────────

@app.route("/tasks", methods=["GET", "POST"])
def tasks():
    if "user" not in session:
        return redirect(url_for("login"))
    users = load_users()
    user_tasks = users[session["user"]].get("tasks", [])
    if request.method == "POST":
        action = request.form.get("action")
        if action == "add":
            task_name = request.form.get("task_name", "").strip()
            priority = request.form.get("priority", "Medium")
            if task_name:
                user_tasks.append({"name": task_name, "priority": priority, "done": False})
        elif action == "toggle":
            idx = int(request.form.get("index", -1))
            if 0 <= idx < len(user_tasks):
                user_tasks[idx]["done"] = not user_tasks[idx]["done"]
        elif action == "delete":
            idx = int(request.form.get("index", -1))
            if 0 <= idx < len(user_tasks):
                user_tasks.pop(idx)
        users[session["user"]]["tasks"] = user_tasks
        save_users(users)
        return redirect(url_for("tasks"))
    return render_template("tasks.html", tasks=user_tasks, username=session["user"])


if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    app.run(debug=True, port=5000)