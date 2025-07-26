from flask import Flask, render_template, request, redirect, url_for
import json
app = Flask(__name__)

# Existing data
tasks = []
completed_tasks = []

# Existing functions
def load_tasks():
    global tasks, completed_tasks
    try:
        with open("tasks.json", "r") as tasks_file:
            data = json.load(tasks_file)
            tasks.extend(data.get("tasks", []))
            completed_tasks.extend(data.get("completed_tasks", []))
    except FileNotFoundError:
        pass

def save_tasks():
    data = {"tasks": tasks, "completed_tasks": completed_tasks}
    with open("tasks.json", "w") as tasks_file:
        json.dump(data, tasks_file)

# Web routes
@app.route('/')
def home():
    load_tasks()
    return render_template('todo.html', tasks=tasks, completed_tasks=completed_tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task = request.form.get("task").strip()
    if task:
        tasks.append(task)
        save_tasks()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)