tasks = []

def add_task(task):
    tasks.append(task)

def view_tasks():
    for task in tasks:
        print(task)

def main():
    print("Add 3 tasks")
    counter = 0
    while counter < 3:
        input_task = input("Enter a task: ")
        add_task(input_task)
        counter += 1
    view_tasks()

if __name__ == '__main__':
    main()