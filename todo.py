import json

tasks = []
completed_tasks = []

# Adds single user-inputted task to tasks list
def add_task():
    task_to_add = input("Enter a task to add: ").strip()
    if task_to_add:
        tasks.append(task_to_add)
        print(f"Added: {task_to_add}")
    else:
        print("Task cannot be empty")

# Prints every task in tasks list
def view_tasks():
    if tasks:
        print("Tasks:")
        for i, task in enumerate(tasks, 1):
            print(f"{i}. {task}")
    else:
        print("No tasks")

def view_completed_tasks():
    if completed_tasks:
        print("Completed tasks:")
        for i, task in enumerate(completed_tasks, 1):
            print(f"{i}. {task}")
    else:
        print("No completed tasks")

# Remove user-specified task
def remove_task():
    if not tasks:
        print("No tasks to remove")
        return
    else:
        task_to_remove = input("Enter a task to remove: ")
        if task_to_remove in tasks:
            tasks.remove(task_to_remove)
            print(f"Removed: {task_to_remove}")
        else:
            print("Task not found! Please check your spelling and try again.")

# Check if task exists and mark completed if so
# Print error message if not
def mark_completed():
    if not tasks:
        print("No tasks to mark completed")
        return
    else:
        task_to_mark = input("Enter a task to mark completed: ")
        if task_to_mark in tasks:
            tasks.remove(task_to_mark)
            completed_tasks.append(task_to_mark)
            print(f"Completed: {task_to_mark}")
        else:
            print("Task not found! Please check your spelling and try again.")

def save_tasks():
    data = {"tasks": tasks, "completed_tasks": completed_tasks}
    with open("tasks.json", "w") as tasks_file:
        json.dump(data, tasks_file)

def load_tasks():
    try:
        with open("tasks.json", "r") as tasks_file:
            data = json.load(tasks_file)
            tasks.extend(data.get("tasks", []))
            completed_tasks.extend(data.get("completed_tasks", []))
    except FileNotFoundError:
        print("New list. No tasks yet.")


def main():
    load_tasks()
    while True:
        print("\n=== TO-DO LIST ===")
        print("1. Add task")
        print("2. View tasks")
        print("3. Remove task")
        print("4. Mark task complete")
        print("5. View completed tasks")
        print("6. Quit")

        choice = input("Choose an option(1-6): ")

        if choice == "1":
            add_task()
        elif choice == "2":
            view_tasks()
        elif choice == "3":
            remove_task()
        elif choice == "4":
            mark_completed()
        elif choice == "5":
            view_completed_tasks()
        elif choice == "6":
            save_tasks()
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
