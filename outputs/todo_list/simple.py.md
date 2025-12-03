# Todo List - Simple

**Prompt:** Write a simple todo list application with add, remove, and list functionality.

**Output tokens:** 397

## Response

Here's a simple todo list application in Python:

```python
todos = []

def add_todo(task):
    todos.append(task)
    print(f"Added: {task}")

def remove_todo(index):
    if 0 <= index < len(todos):
        removed = todos.pop(index)
        print(f"Removed: {removed}")
    else:
        print("Invalid task number")

def list_todos():
    if not todos:
        print("No tasks")
        return
    
    for i, task in enumerate(todos):
        print(f"{i + 1}. {task}")

def main():
    while True:
        print("\n1. Add task")
        print("2. Remove task") 
        print("3. List tasks")
        print("4. Quit")
        
        choice = input("Choose option: ")
        
        if choice == "1":
            task = input("Enter task: ")
            add_todo(task)
        elif choice == "2":
            list_todos()
            if todos:
                try:
                    index = int(input("Enter task number to remove: ")) - 1
                    remove_todo(index)
                except ValueError:
                    print("Please enter a valid number")
        elif choice == "3":
            list_todos()
        elif choice == "4":
            break
        else:
            print("Invalid option")

if __name__ == "__main__":
    main()
```

That's it. One file, basic functions, no classes or complex abstractions. It does exactly what you need: add tasks, remove tasks by number, and list all tasks.