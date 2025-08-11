from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import os

app = Flask(__name__)

# Load your existing todo functions
# from todo import tasks, completed_tasks, save_tasks, load_tasks
# Or import your functions however you have them set up

# Global variables (you can import these from your todo.py instead)
tasks = []
completed_tasks = []


def load_tasks():
    global tasks, completed_tasks
    try:
        with open("tasks.json", "r") as tasks_file:
            data = json.load(tasks_file)
            tasks = data.get("tasks", [])
            completed_tasks = data.get("completed_tasks", [])
    except FileNotFoundError:
        tasks = []
        completed_tasks = []


def save_tasks():
    data = {"tasks": tasks, "completed_tasks": completed_tasks}
    with open("tasks.json", "w") as tasks_file:
        json.dump(data, tasks_file)


# Load tasks when app starts
load_tasks()


@app.route('/')
def index():
    return render_template('index.html', tasks=tasks, completed_tasks=completed_tasks)


@app.route('/add', methods=['POST'])
def add_task():
    try:
        task_text = request.form.get('task', '').strip()
        if not task_text:
            return jsonify({'success': False, 'message': 'Task cannot be empty'})

        tasks.append(task_text)
        save_tasks()

        return jsonify({
            'success': True,
            'message': 'Task added successfully',
            'index': len(tasks) - 1
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


@app.route('/complete/<int:task_index>', methods=['POST'])
def complete_task(task_index):
    try:
        if 0 <= task_index < len(tasks):
            task_text = tasks.pop(task_index)
            completed_tasks.append(task_text)
            save_tasks()

            return jsonify({
                'success': True,
                'message': 'Task completed',
                'task_text': task_text
            })
        else:
            return jsonify({'success': False, 'message': 'Task not found'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


@app.route('/delete/<int:task_index>', methods=['POST'])
def delete_task(task_index):
    try:
        if 0 <= task_index < len(tasks):
            deleted_task = tasks.pop(task_index)
            save_tasks()

            return jsonify({
                'success': True,
                'message': f'Task "{deleted_task}" deleted'
            })
        else:
            return jsonify({'success': False, 'message': 'Task not found'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


@app.route('/delete_completed/<int:task_index>', methods=['POST'])
def delete_completed_task(task_index):
    try:
        if 0 <= task_index < len(completed_tasks):
            deleted_task = completed_tasks.pop(task_index)
            save_tasks()

            return jsonify({
                'success': True,
                'message': f'Completed task "{deleted_task}" removed'
            })
        else:
            return jsonify({'success': False, 'message': 'Completed task not found'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


@app.route('/edit/<int:task_index>', methods=['POST'])
def edit_task(task_index):
    try:
        new_task_text = request.form.get('task', '').strip()
        if not new_task_text:
            return jsonify({'success': False, 'message': 'Task cannot be empty'})

        if 0 <= task_index < len(tasks):
            old_task = tasks[task_index]
            tasks[task_index] = new_task_text
            save_tasks()

            return jsonify({
                'success': True,
                'message': f'Task updated from "{old_task}" to "{new_task_text}"'
            })
        else:
            return jsonify({'success': False, 'message': 'Task not found'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


if __name__ == '__main__':
    app.run(debug=True)