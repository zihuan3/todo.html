tasks = []
completed_tasks = []

# Adds a singular user-inputted task to the tasks list
def add_task():
    task_to_add = input("Enter a task to add: ")
    tasks.append(task_to_add)

# Prints every task in the tasks list
def view_tasks():
    if len(tasks) > 0:
        print("Tasks:")
        for task in tasks:
            print(task)
    else:
        print("No tasks")

def view_completed_tasks():
    if len(completed_tasks) > 0:
        print("Completed tasks:")
        for completed_task in completed_tasks:
            print(completed_task)
    else:
        print("No completed tasks")

# Remove a user-specified task
def remove_task():
    task_to_remove = input("Enter a task to remove: ")
    if task_to_remove in tasks:
        tasks.remove(task_to_remove)
        print(f"Removed: {task_to_remove}")
    else:
        print("Task not found! Please check your spelling and try again.")

# Check if task exists and mark completed if so
# Print error message if not
def mark_completed():
    task_to_mark = input("Enter a task to mark completed: ")
    if task_to_mark in tasks:
        tasks.remove(task_to_mark)
        completed_tasks.append(task_to_mark)
        print(f"Completed: {task_to_mark}")
    else:
        print("Task not found! Please check your spelling and try again.")


def main():
    while True:
        print("\n=== TO-DO LIST ===")
        print("1. Add task")
        print("2. View tasks")
        print("3. Remove task")
        print("4. Mark task complete")
        print("5. View completed tasks")
        print("6. Quit")

        choice = input("Choose an option(1-6)")

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
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()