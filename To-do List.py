# Import the Tkinter library, which is built-in with Python for GUI development.
import tkinter as tk
# Import specific modules from Tkinter for dialog boxes (simple input/output).
from tkinter import simpledialog, messagebox

# --- Data Structure and Backend Logic ---

# Initialize the core data structure: a global list to hold all tasks.
# Each task is stored as a tuple: (description_string, status_string: "Pending" or "Done").
todo_list = []

# Function to add a task to the global list.
def add_task_logic(task_desc):
    """Adds a task to the global list and triggers a GUI update."""
    # Append a new tuple to the list with the task description and "Pending" status.
    todo_list.append((task_desc, "Pending"))
    # Call the GUI function to refresh the listbox display.
    update_listbox()

# Function to mark a task as Done based on its index in the list.
def mark_done_logic(index):
    """Marks a task at a given index as Done and triggers a GUI update."""
    # Check if the provided index is valid (within the bounds of the list).
    if 0 <= index < len(todo_list):
        # Unpack the existing tuple at the index to get the description (first element).
        task_desc, _ = todo_list[index]
        # Overwrite the old tuple with a new one, changing the status to "Done".
        # Tuples are immutable, so we must replace the whole item.
        todo_list[index] = (task_desc, "Done")
        # Call the GUI function to refresh the listbox display.
        update_listbox()

# Function to delete a task based on its index.
def delete_task_logic(index):
    """Deletes a task at a given index and triggers a GUI update."""
    # Check if the provided index is valid.
    if 0 <= index < len(todo_list):
        # Use the pop() method to remove the item at the specific index.
        todo_list.pop(index)
        # Call the GUI function to refresh the listbox display.
        update_listbox()

# --- GUI Functions (Frontend Interface) ---

# Function responsible for synchronizing the listbox display with the todo_list data.
def update_listbox():
    """Clears and re-populates the Listbox widget with current tasks."""
    # Clear all existing items in the listbox, from index 0 to the end (tk.END).
    listbox.delete(0, tk.END)
    # Loop through every task (which is a tuple of (task, status)) in the backend list.
    for task, status in todo_list:
        # Create a formatted string (f-string) for display in the listbox.
        display_text = f"[{status}] {task}"
        # Insert the formatted string at the end of the listbox.
        listbox.insert(tk.END, display_text)
    # Clear any selection highlighting after the update to avoid confusing the user.
    listbox.selection_clear(0, tk.END)

# Function called when the "Add Task" button is clicked.
def show_add_task_dialog():
    """Opens a dialog for task input and handles addition."""
    # Opens a simple Tkinter dialog to ask for a string input, storing the result in 'task'.
    task = simpledialog.askstring("Add Task", "Enter the new task:")
    # Check if the user entered any text (not empty) and didn't click Cancel (task is not None).
    if task:
        # Call the backend logic to add the task to the data list.
        add_task_logic(task)
        # Show a confirmation message box to the user.
        messagebox.showinfo("Success", f"Task '{task}' added!")

# Function called when the "Mark as Done" button is clicked.
def mark_done_gui():
    """Handles the GUI interaction for marking a task as done."""
    # Use a try-except block for robust error handling if no item is selected.
    try:
        # Get the index of the currently selected item in the listbox.
        # listbox.curselection() returns a tuple of indices; [0] gets the first one.
        selected_index = listbox.curselection()[0]
        # Call the backend logic with the found index.
        mark_done_logic(selected_index)
    # Catch the IndexError that occurs if listbox.curselection() returns an empty tuple (no item selected).
    except IndexError:
        # Display an error message box to prompt the user.
        messagebox.showerror("Error", "Please select a task to mark as done.")

# Function called when the "Delete Task" button is clicked.
def delete_task_gui():
    """Handles the GUI interaction for deleting a task."""
    # Use a try-except block for robust error handling.
    try:
        # Get the index of the currently selected item.
        selected_index = listbox.curselection()[0]
        # Call the backend logic with the found index.
        delete_task_logic(selected_index)
    # Catch the IndexError if no item is selected.
    except IndexError:
        # Display an error message box.
        messagebox.showerror("Error", "Please select a task to delete.")

# --- Main Application Setup ---

# 1. Initialize the main window (the root object).
root = tk.Tk()
# Set the title displayed in the window's title bar.
root.title("Python To-Do List GUI")
# Set the initial size of the window (Width x Height).
root.geometry("400x450")

# 2. Create the Listbox widget to display tasks.
# Arguments: parent (root), height (lines visible), width (characters), border style.
listbox = tk.Listbox(root, height=15, width=50, border=1)
# Place the listbox widget in the window using the pack geometry manager.
# pady=10 adds 10 pixels of padding above and below the widget.
listbox.pack(pady=10)

# 3. Create the buttons and associate them with functions using 'command'.

# Add Task Button setup.
# The 'command' argument links the button click event to the function to execute.
add_button = tk.Button(root, text="Add Task", command=show_add_task_dialog)
# Place the button, stretching it horizontally (fill='x'), with horizontal and vertical padding.
add_button.pack(fill='x', padx=20, pady=5)

# Mark Done Button setup.
done_button = tk.Button(root, text="Mark as Done", command=mark_done_gui)
# Place the button, maintaining consistent padding and filling the x-axis.
done_button.pack(fill='x', padx=20, pady=5)

# Delete Task Button setup.
delete_button = tk.Button(root, text="Delete Task", command=delete_task_gui)
# Place the button.
delete_button.pack(fill='x', padx=20, pady=5)

# 4. Start the Tkinter event loop.
# This block ensures the code runs only when executed directly, not imported.
if __name__ == "__main__":
    # Call the update function once to ensure the listbox is initialized (even if empty).
    update_listbox()
    # Start the event loop, which listens for user actions and keeps the window open.
    root.mainloop()