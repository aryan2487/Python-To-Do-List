def display_menu():
    """Displays the main menu options to the user."""
    print("\n--- To-Do List Manager ---")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Mark Task as Done")
    print("4. Delete Task")
    print("5. Exit")

def add_task(todo_list):
    """Prompts user for a task and adds it to the list."""
    task = input("Enter the task description: ")
    # Tasks are stored as a tuple: (description, status)
    todo_list.append((task, "Pending"))
    print(f"Task '{task}' added.")

def view_tasks(todo_list):
    """Displays all tasks with their index and status."""
    if not todo_list:
        print("Your To-Do list is empty!")
        return

    print("\n--- Your Tasks ---")
    for index, (task, status) in enumerate(todo_list):
        # The index is 0-based, so we add 1 for user readability
        print(f"{index + 1}. [{status}] {task}")

def mark_done(todo_list):
    """Allows the user to mark a task as 'Done'."""
    view_tasks(todo_list)
    if not todo_list:
        return

    try:
        task_num = int(input("Enter the number of the task to mark as Done: "))
        # Convert user's 1-based input to 0-based index
        index = task_num - 1

        if 0 <= index < len(todo_list):
            # Retrieve the task description
            task_desc, _ = todo_list[index]
            # Replace the old tuple with a new one having the 'Done' status
            todo_list[index] = (task_desc, "Done")
            print(f"Task {task_num} marked as Done.")
        else:
            print("Invalid task number.")

    except ValueError:
        print("Invalid input. Please enter a number.")

def delete_task(todo_list):
    """Allows the user to delete a task."""
    view_tasks(todo_list)
    if not todo_list:
        return

    try:
        task_num = int(input("Enter the number of the task to delete: "))
        # Convert user's 1-based input to 0-based index
        index = task_num - 1

        if 0 <= index < len(todo_list):
            # Delete the task using its index
            deleted_task, _ = todo_list.pop(index)
            print(f"Task '{deleted_task}' deleted.")
        else:
            print("Invalid task number.")

    except ValueError:
        print("Invalid input. Please enter a number.")

def main():
    """The main function to run the To-Do List program."""
    # The core data structure: a list to hold all tasks.
    # Each task is a tuple (task_description, status)
    todo_list = []

    # The main loop keeps the program running until the user chooses to exit
    while True:
        display_menu()
        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            add_task(todo_list)
        elif choice == '2':
            view_tasks(todo_list)
        elif choice == '3':
            mark_done(todo_list)
        elif choice == '4':
            delete_task(todo_list)
        elif choice == '5':
            print("Exiting To-Do List Manager. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

# This is the standard way to run the main function when the script is executed
if __name__ == "__main__":
    main()