from flask import Flask, render_template, request, redirect
import json
from datetime import date

app = Flask(__name__)

DATA_FILE = 'data.json'

def load_data():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {"cooldowns": {}, "last_used": {}}

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@app.route("/", methods=["GET", "POST"])
def index():
    data = load_data()
    message = ""

    if request.method == "POST":
        action = request.form.get("action")

        if action == "add":
            name = request.form.get("habit_name")
            cooldown = int(request.form.get("habit_cooldown"))
            data["cooldowns"][name] = cooldown
            data["last_used"][name] = None
            save_data(data)

        elif action == "mark_done":
            habit = request.form.get("habit_done")
            data["last_used"][habit] = str(date.today())
            save_data(data)

        return redirect("/")

    habits_info = []

    for habit, cooldown in data["cooldowns"].items():
        last_used = data["last_used"].get(habit)
        if last_used:
            days_since = (date.today() - date.fromisoformat(last_used)).days
            days_left = cooldown - days_since
        else:
            days_left = 0

        habits_info.append({
            "name": habit,
            "cooldown": cooldown,
            "last_used": last_used,
            "available": days_left <= 0,
            "days_left": max(days_left, 0)
        })

    return render_template("index.html", habits=habits_info)

if __name__ == "__main__":
    app.run(debug=True)
