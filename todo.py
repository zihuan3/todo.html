tasks = []

# Adds a singular user-inputted task to the tasks list
def add_task():
    task_to_add = input("Enter a task to add: ")
    tasks.append(task_to_add)

# Prints every task in the tasks list
def view_tasks():
    for task in tasks:
        print(task)

# Remove a user-specified task
def remove_task():
    task_to_remove = input("Enter a task to remove: ")
    tasks.remove(task_to_remove)

def main():
    print("Add 3 tasks")
    counter = 0
    while counter < 3:
        add_task()
        counter += 1
    view_tasks()
    remove_task()
    view_tasks()

if __name__ == '__main__':
    main()