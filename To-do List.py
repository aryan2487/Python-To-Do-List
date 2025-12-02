# Import the Tkinter library, which is built-in with Python for GUI development.
import tkinter as tk
# Import specific modules from Tkinter for dialog boxes (simple input/output) and ttk for scrollbar.
from tkinter import simpledialog, messagebox, ttk 

# --- Data Structure and Backend Logic ---

# Initialize the core data structure: a global list to hold all tasks.
# Each task is stored as a tuple: (description_string, status_boolean: True for Done, False for Pending).
todo_list = []

# Function to add a task to the global list.
def add_task_logic(task_desc):
    """Adds a task to the global list and triggers a GUI update."""
    # Append a new tuple to the list with the task description and False (Pending) status.
    todo_list.append((task_desc, False))
    # Call the GUI function to refresh the task list display.
    update_task_list_display()

# Function called when a checkbox is toggled.
def toggle_task_status(index):
    """Flips the status of a task at a given index."""
    # Check if the provided index is valid (within the bounds of the list).
    if 0 <= index < len(todo_list):
        # Unpack the existing tuple at the index.
        task_desc, current_status = todo_list[index]
        # Overwrite the old tuple with a new one, flipping the boolean status (True becomes False, and vice-versa).
        todo_list[index] = (task_desc, not current_status)
        # Call the update function to re-render the list and apply any styling based on status (e.g., strikethrough).
        # We call it here to refresh the look of the list after the state is toggled.
        update_task_list_display() 

# Function to delete a task based on its index.
def delete_task_logic(index):
    """Deletes a task at a given index and triggers a GUI update."""
    # Check if the provided index is valid.
    if 0 <= index < len(todo_list):
        # Use a custom colored confirmation dialog before deleting.
        message = f"Are you sure you want to delete task '{todo_list[index][0]}'?"
        if custom_ask_yes_no(root, "Confirm Delete", message):
            # Use the pop() method to remove the item at the specific index.
            todo_list.pop(index)
            # Call the GUI function to refresh the task list display.
            update_task_list_display()

# --- GUI Functions (Frontend Interface) ---

# Function called when the user wants to set a new name for the list.
def set_list_name_gui():
    """Opens a dialog to get the list name and updates the title variable."""
    # Opens a simple Tkinter dialog to ask for the new list name.
    new_name = simpledialog.askstring("Set List Name", "Enter the new title for your To-Do List:")
    # Check if the user entered a name (not empty and not cancelled).
    if new_name:
        # Update the Tkinter StringVar, which automatically updates the Label widget.
        list_title_var.set(new_name)

# Function called when the inner frame changes size (e.g., tasks are added/removed).
def on_frame_configure(event):
    """Adjusts the scroll region of the canvas to match the size of the inner frame."""
    # Set the scroll region of the canvas to enclose the entire frame.
    canvas.configure(scrollregion=canvas.bbox("all"))

# Function responsible for synchronizing the display with the todo_list data using Checkbuttons.
def update_task_list_display():
    """Destroys and recreates Checkbutton widgets for all tasks inside the scrollable frame."""
    # Destroy all existing widgets inside the task_frame (the inner container).
    for widget in task_frame.winfo_children():
        widget.destroy()

    # Loop through every task in the backend list to create its corresponding widgets.
    for index, (task, status) in enumerate(todo_list):
        # Create a variable to hold the state of the Checkbutton for the current task.
        var = tk.BooleanVar(value=status)
        
        # Determine the text decoration (strikethrough) and colors based on the status.
        font_config = ("Arial", 12)
        
        # --- NEW VISUAL EFFECTS LOGIC ---
        if status:
            # If done, apply strikethrough, set text to dark gray, and set row background to pale gray.
            font_config = ("Arial", 12, "overstrike") 
            fg_color = "#555555" # Darker gray for completed tasks
            row_bg_color = "#F0F0F0" # Pale Gray for completed task background (Visual Effect)
        else:
            # If pending, use normal font, black text, and baby yellow background.
            fg_color = "#000000" 
            row_bg_color = task_frame.cget('bg') # Baby yellow (#FFFACD)

        # Create the Checkbutton widget.
        chk = tk.Checkbutton(
            task_frame,
            text=task,
            variable=var, # Link the Checkbutton state to the BooleanVar.
            # Use a lambda function to call the toggle_task_status with the task's index when clicked.
            command=lambda i=index: toggle_task_status(i),
            anchor='w', # Align the text to the west (left).
            bg=row_bg_color, # Apply calculated background color
            font=font_config,
            fg=fg_color,
            selectcolor=row_bg_color # Makes the checkbox background transparent (matches row color)
        )
        # Place the checkbutton in the grid. Column 0, Row index. Span 2 columns.
        chk.grid(row=index, column=0, sticky='ew', padx=10, pady=5)

        # Create the Delete Button widget next to the task.
        del_btn = tk.Button(
            task_frame,
            text="X", # Use 'X' for a compact delete button.
            fg='#800000', # Darker red/maroon for a softer delete look
            bg=row_bg_color, # Apply calculated background color to delete button
            activebackground='#FFCCCC',
            relief=tk.FLAT, # Flat look for calmness
            # Use a lambda function to call the delete_task_logic with the task's index.
            command=lambda i=index: delete_task_logic(i)
        )
        # Place the delete button in the grid. Column 1, Row index.
        del_btn.grid(row=index, column=1, padx=5, pady=5)

        # Configure the grid to ensure the Checkbutton expands to fill the space.
        task_frame.grid_columnconfigure(0, weight=1)

    # After adding all widgets, update the scroll region of the canvas.
    task_frame.update_idletasks() # Ensure the frame size is calculated.
    canvas.config(scrollregion=canvas.bbox("all")) # Set the scrollable area.

# --- Custom Dialogs for Colored Input and Confirmation ---

class CustomAskStringDialog(tk.Toplevel):
    """Custom input dialog to allow background color customization."""
    def __init__(self, parent, title, prompt, bg_color="#E6F7F2"):
        # Initialize the top-level window (the dialog itself)
        super().__init__(parent)
        self.transient(parent) # Set dialog as transient for the parent window (stays on top)
        self.title(title)
        self.result = None
        self.parent = parent
        self.bg_color = bg_color
        
        # Set the custom background color for the dialog window
        self.config(bg=self.bg_color)
        
        # Center the dialog on the screen (based on the parent window size)
        self.parent.update_idletasks()
        w = self.winfo_reqwidth()
        h = self.winfo_reqheight()
        x = (self.parent.winfo_width() // 2) - (w // 2)
        y = (self.parent.winfo_height() // 2) - (h // 2)
        self.geometry('+%d+%d' % (x, y))

        self.create_widgets(prompt)

        # Define behavior for closing the window via the window manager (X button)
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.grab_set() # Make the dialog modal (forces interaction)
        self.parent.wait_window(self) # Pause the main app until the dialog is closed

    def create_widgets(self, prompt):
        # Frame for padding and color consistency within the dialog body
        body = tk.Frame(self, bg=self.bg_color, padx=10, pady=10)
        body.pack(padx=5, pady=5)

        # Label displaying the input prompt
        tk.Label(body, text=prompt, bg=self.bg_color, font=("Arial", 12)).pack(pady=5)

        # Entry widget for user input
        self.entry = tk.Entry(body, width=30, font=("Arial", 12))
        self.entry.pack(pady=5)
        self.entry.bind("<Return>", lambda event: self.ok()) # Bind Enter key to 'OK'
        self.entry.focus_set() # Focus the cursor on the input field

        # Frame for placing the OK and Cancel buttons
        button_frame = tk.Frame(self, bg=self.bg_color)
        button_frame.pack(pady=5, padx=10)

        # OK Button (Add)
        ok_button = tk.Button(
            button_frame, 
            text="Add", 
            width=10, 
            command=self.ok,
            bg='#CCCCE6', # Soft Lavender
            activebackground='#DDDDFF',
            fg='#333366',
            relief=tk.GROOVE
        )
        ok_button.pack(side=tk.LEFT, padx=5)

        # Cancel Button
        cancel_button = tk.Button(
            button_frame, 
            text="Cancel", 
            width=10, 
            command=self.cancel,
            bg='#FFCCCC', # Soft Red
            activebackground='#FF9999',
            fg='#800000',
            relief=tk.GROOVE
        )
        cancel_button.pack(side=tk.LEFT, padx=5)

    def ok(self):
        """Sets the result to the entry text and closes the dialog."""
        self.result = self.entry.get()
        self.destroy()

    def cancel(self):
        """Sets the result to None and closes the dialog."""
        self.result = None 
        self.destroy()

def custom_ask_string(parent, title, prompt):
    """Utility function to create and run the custom dialog."""
    dialog = CustomAskStringDialog(parent, title, prompt)
    return dialog.result

class CustomAskYesNoDialog(tk.Toplevel):
    """Custom Yes/No confirmation dialog with colored background."""
    def __init__(self, parent, title, message, bg_color="#E6F7F2"):
        super().__init__(parent)
        self.transient(parent)
        self.title(title)
        self.result = False
        self.parent = parent
        self.bg_color = bg_color
        self.config(bg=self.bg_color)
        
        # Centering logic (fixed dimensions for simplicity)
        self.parent.update_idletasks()
        w = 350 # Fixed width for dialog
        h = 150 # Fixed height
        x = (self.parent.winfo_width() // 2) - (w // 2)
        y = (self.parent.winfo_height() // 2) - (h // 2)
        self.geometry(f'{w}x{h}+{x}+{y}')

        self.create_widgets(message)

        self.protocol("WM_DELETE_WINDOW", self.no_action)
        self.grab_set()
        self.parent.wait_window(self)

    def create_widgets(self, message):
        body = tk.Frame(self, bg=self.bg_color, padx=10, pady=15)
        body.pack(padx=5, pady=5, fill='both', expand=True)

        tk.Label(body, text=message, bg=self.bg_color, font=("Arial", 12)).pack(pady=10)

        button_frame = tk.Frame(self, bg=self.bg_color)
        button_frame.pack(pady=5, padx=10)

        # Yes Button (Confirm Delete - Soft Red/Maroon)
        yes_button = tk.Button(
            button_frame, 
            text="Yes, Delete", 
            width=12, 
            command=self.yes_action,
            bg='#FFCCCC', 
            activebackground='#FF9999',
            fg='#800000',
            relief=tk.GROOVE
        )
        yes_button.pack(side=tk.LEFT, padx=5)

        # No Button (Cancel - Soft Mint/Teal)
        no_button = tk.Button(
            button_frame, 
            text="No, Keep It", 
            width=12, 
            command=self.no_action,
            bg='#CCDDDD', 
            activebackground='#DDFFFF',
            fg='#003333',
            relief=tk.GROOVE
        )
        no_button.pack(side=tk.LEFT, padx=5)
        
    def yes_action(self):
        """Sets result to True and destroys the dialog."""
        self.result = True
        self.destroy()

    def no_action(self):
        """Sets result to False and destroys the dialog."""
        self.result = False
        self.destroy()

def custom_ask_yes_no(parent, title, message):
    """Utility function to create and run the custom yes/no dialog."""
    dialog = CustomAskYesNoDialog(parent, title, message)
    return dialog.result

def show_add_task_dialog():
    """Opens a custom colored dialog for task input and handles addition."""
    # Use the custom function which returns the entered string or None if cancelled.
    task = custom_ask_string(root, "Add Task", "Enter the new task:")
    # Check if the user entered any text (not empty) and didn't click Cancel.
    if task:
        # Call the backend logic to add the task.
        add_task_logic(task)
        # Show a confirmation message box.
        messagebox.showinfo("Success", f"Task '{task}' added!")

# --- Main Application Setup ---

# 1. Initialize the main window (the root object).
root = tk.Tk()
# Set the title displayed in the window's title bar.
root.title("Python To-Do List GUI (Calm Fullscreen)")

# FIX: Initialize the Tkinter string variable AFTER the root window is created.
# Initialize a Tkinter string variable to hold the dynamic title of the list.
list_title_var = tk.StringVar(value="My Daily To-Do List")

# Set the window to fullscreen mode.
root.attributes('-fullscreen', True) 
# Set the calming background color for the main window.
root.config(bg="#E6F7F2") # Soft Mint Green

# 2. Setup the Title Bar (Row 0).

# Create a frame for the title and the "Set Name" button.
title_frame = tk.Frame(root, bg=root.cget('bg')) 
# Place the title frame at the top (Row 0), spanning both columns.
title_frame.grid(row=0, column=0, columnspan=2, sticky='ew', padx=50, pady=(50, 20))
# Configure the title frame grid so the title label expands.
title_frame.grid_columnconfigure(0, weight=1)

# Create the main Title Label, linked to the StringVar.
title_label = tk.Label(
    title_frame,
    textvariable=list_title_var, # Uses the dynamic string variable
    font=("Arial", 28, "bold"),
    bg=root.cget('bg'),
    fg="#003333" # Dark teal text color
)
# Place the title label on the left of the title frame, spanning two rows to make space for buttons.
title_label.grid(row=0, column=0, rowspan=1, sticky='w') # Reduced rowspan from 2 to 1 as the + button is no longer here

# Create the "Set Name" button.
set_name_button = tk.Button(
    title_frame,
    text="Set Name",
    command=set_list_name_gui, # New function call
    bg='#CCCCE6', # Soft Lavender
    activebackground='#DDDDFF',
    fg='#333366',
    relief=tk.FLAT
)
# Place the button in the top right corner of the title area (Row 0, Column 1).
set_name_button.grid(row=0, column=1, sticky='e', padx=10)


# 2.1 Setup the Add Task Control (New Row 1).
# Create a frame for the Add Task button and label
add_control_frame = tk.Frame(root, bg=root.cget('bg'))
# Place the control frame immediately below the title bar (Row 1).
add_control_frame.grid(row=1, column=0, columnspan=2, sticky='ew', padx=50, pady=(0, 10))
# Configure the grid to push controls to the right.
add_control_frame.grid_columnconfigure(0, weight=1) 

# Add Task Label
add_label = tk.Label(
    add_control_frame,
    text="Add Task:",
    font=("Arial", 12),
    bg=root.cget('bg'),
    fg="#003333"
)
# Place the label to the right of the expanding space (Column 1).
add_label.grid(row=0, column=1, sticky='e') 

# NEW: Add Task Button setup (the "+" sign)
add_button = tk.Button(
    add_control_frame, 
    text="+", 
    command=show_add_task_dialog,
    font=("Arial", 16, "bold"), 
    bg='#CCDDDD', # Pale Mint/Teal (Easy on the eyes)
    activebackground='#DDFFFF',
    fg='#003333',
    relief=tk.GROOVE # Slightly raised look
)
# Place the + button next to the label (Column 2).
add_button.grid(row=0, column=2, sticky='e', padx=(5, 0)) 


# 3. Setup the Canvas and Scrollbar for the task list (Now Row 2).

# Create the Canvas widget.
canvas = tk.Canvas(root, borderwidth=0, background="#FFFACD") # Baby yellow background for the list area
# Create the vertical scrollbar.
scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
# Place the inner frame (task_frame) inside the canvas view.
task_frame = tk.Frame(canvas, background="#FFFACD") # Baby yellow background for the task container

# Configure the canvas to use the scrollbar for the y-axis.
canvas.configure(yscrollcommand=scrollbar.set)

# Place the scrollbar and canvas in the main window using grid.
# The grid system manages the layout for the entire fullscreen app.
scrollbar.grid(row=2, column=1, sticky='ns') # SHIFTED TO ROW 2
canvas.grid(row=2, column=0, sticky='nsew', padx=50) # SHIFTED TO ROW 2

# Configure the grid to allow the canvas to expand when the window is resized.
root.grid_rowconfigure(2, weight=1) # SHIFTED TO ROW 2
root.grid_columnconfigure(0, weight=1)
# Column 1 (for the scrollbar) should not expand.
root.grid_columnconfigure(1, weight=0) 


# Create a window inside the canvas to hold the task_frame.
canvas.create_window((0, 0), window=task_frame, anchor="nw")
# Bind the frame configuration event to adjust the canvas scroll region when the frame size changes.
task_frame.bind("<Configure>", on_frame_configure)

# 4. Create the control buttons at the bottom (Now Rows 3).

# Exit Button for fullscreen mode.
exit_button = tk.Button(
    root,
    # CHANGED TEXT: from "Exit App (F11)" to a more friendly phrase.
    text="Done with all the tasks (Press F11 to Exit Fullscreen)", 
    command=root.destroy, # The built-in command to close the window
    bg='#FFCCCC', # Soft Red background
    activebackground='#FF9999',
    fg='#800000',
    relief=tk.GROOVE
)
# The button is placed in Row 3 now.
exit_button.grid(row=3, column=0, columnspan=2, sticky='ew', padx=50, pady=(10, 50)) # Extra padding at bottom

# Optional: Bind the F11 key to toggle fullscreen/exit
root.bind("<F11>", lambda event: root.attributes("-fullscreen", not root.attributes("-fullscreen")))

# 5. Start the Tkinter event loop.
if __name__ == "__main__":
    # Call the update function once to populate the list upon startup.
    update_task_list_display()
    # Start the event loop, which listens for user actions.
    root.mainloop()