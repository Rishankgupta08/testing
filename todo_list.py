import sys
import os

class TodoList:
    def __init__(self, filename):
        self.filename = filename
        self.tasks = self.load_tasks()

    def load_tasks(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                return [line.strip() for line in file.readlines()]
        else:
            return []

    def save_tasks(self):
        with open(self.filename, 'w') as file:
            for task in self.tasks:
                file.write(task + '\n')

    def add_task(self, task):
        self.tasks.append(task)
        self.save_tasks()

    def list_tasks(self):
        for i, task in enumerate(self.tasks, start=1):
            print(f'{i}. {task}')

    def delete_task(self, task_number):
        try:
            task_number = int(task_number)
            if task_number > 0 and task_number <= len(self.tasks):
                del self.tasks[task_number - 1]
                self.save_tasks()
            else:
                print('Invalid task number')
        except ValueError:
            print('Invalid task number')

def main():
    filename = 'todo.txt'
    todo_list = TodoList(filename)

    if len(sys.argv) == 1:
        print('Usage: python todo.py [add/list/delete] [task/task_number]')
    elif sys.argv[1] == 'add':
        if len(sys.argv) > 2:
            task = ' '.join(sys.argv[2:])
            todo_list.add_task(task)
        else:
            print('Please provide a task to add')
    elif sys.argv[1] == 'list':
        todo_list.list_tasks()
    elif sys.argv[1] == 'delete':
        if len(sys.argv) > 2:
            task_number = sys.argv[2]
            todo_list.delete_task(task_number)
        else:
            print('Please provide a task number to delete')
    else:
        print('Invalid command')

if __name__ == '__main__':
    main()