# Import the Tkinter library, which is built-in with Python for GUI development.
import tkinter as tk
# Add time for tracking duration and datetime for formatting the time delta
import time 
from datetime import timedelta
# Import specific modules from Tkinter for dialog boxes (simple input/output) and ttk for scrollbar and Combobox.
from tkinter import simpledialog, messagebox, ttk 

# --- Global Theme Definitions ---
# Dictionary defining multiple themes with their corresponding color codes.
THEMES = {
    "Calm (Mint & Yellow)": {
        "main_bg": "#E6F7F2",    # Soft Mint Green
        "title_fg": "#003333",   # Dark teal text
        "list_bg": "#FFFACD",    # Baby Yellow
        "done_bg": "#F0F0F0",    # Pale Gray for completed tasks
        "add_btn_bg": "#CCDDDD", # Pale Mint/Teal
        "exit_btn_bg": "#FFCCCC",# Soft Red
        "exit_btn_fg": "#800000",
        "default_fg": "#000000",
        "done_fg": "#555555",
    },
    "Dark (Charcoal)": {
        "main_bg": "#1C1C1C",    # Charcoal Black
        "title_fg": "#E0E0E0",   # Light Gray text (used for titles/pop-up labels)
        "list_bg": "#333333",    # Darker Gray list background
        "done_bg": "#2A2A2A",    # Slightly lighter done task background
        "add_btn_bg": "#555555",
        "exit_btn_bg": "#8B0000", # Dark Red
        "exit_btn_fg": "#FFFFFF",
        "default_fg": "#FFFFFF", # White text
        "done_fg": "#A0A0A0",
    }
}
# Global variable to hold the currently selected theme's color dictionary.
current_theme = THEMES["Calm (Mint & Yellow)"] # Set initial theme
# Global reference to the main root window
root = None 
# Global references to key widgets for reconfiguration
list_title_var = None
canvas = None
task_frame = None
title_frame = None # Added for global access
add_control_frame = None # Added for global access
title_label = None # Added for global access
add_label = None # Added for global access
add_button = None # Added for global access
exit_button = None # Added for global access
theme_selector = None # Added for global access
stats_label = None # New label for displaying stats
# NEW: Global variable to track the maximum number of tasks ever added during the session
max_tasks_ever_added = 0 


# --- Data Structure and Backend Logic ---

# Initialize the core data structure: a global list to hold all tasks.
# Each task is now stored as a tuple: (desc, status, creation_time, completion_time).
todo_list = []

# Function to add a task to the global list.
def add_task_logic(task_desc):
    """Adds a task to the global list and triggers a GUI update."""
    global max_tasks_ever_added
    # Append a new tuple: (desc, status=False, creation_time=now, completion_time=None)
    todo_list.append((task_desc, False, time.time(), None))
    # NEW: Update max tasks ever added during the session
    max_tasks_ever_added = max(max_tasks_ever_added, len(todo_list)) 
    # Call the GUI function to refresh the task list display.
    update_task_list_display()
    # update_stats() is now managed by the root.after loop.

# Function called when a checkbox is toggled.
def toggle_task_status(index):
    """Flips the status of a task at a given index and updates its completion time."""
    # Check if the provided index is valid (within the bounds of the list).
    if 0 <= index < len(todo_list):
        # Unpack the existing tuple, including time stamps.
        task_desc, current_status, creation_time, completion_time = todo_list[index]
        
        new_status = not current_status
        new_completion_time = None
        
        if new_status:
            # Mark done: record current time as the completion time.
            new_completion_time = time.time()
        
        # Overwrite the old tuple with a new one, flipping the boolean status and updating the time.
        todo_list[index] = (task_desc, new_status, creation_time, new_completion_time)
        
        # Call the update function to re-render the list. Stats will update in the next 1-second cycle.
        update_task_list_display() 

# Function to delete a task based on its index.
def delete_task_logic(index):
    """Deletes a task at a given index and triggers a GUI update."""
    # Check if the provided index is valid.
    if 0 <= index < len(todo_list):
        # Use a custom colored confirmation dialog before deleting.
        message = f"Are you sure you want to delete task '{todo_list[index][0]}'?"
        # The custom dialog is called, returning True if 'Yes' is clicked.
        if custom_ask_yes_no(root, "Confirm Delete", message):
            # Use the pop() method to remove the item at the specific index.
            todo_list.pop(index)
            # Call the GUI function to refresh the task list display.
            update_task_list_display()

# Helper function to calculate session duration
def calculate_session_duration_str():
    """Calculates the total elapsed time since the first task was created."""
    current_time = time.time()
    if not todo_list:
        total_duration_seconds = 0
    else:
        # Find the creation time of the very first task added (index 2 in the tuple)
        earliest_creation_time = min(task[2] for task in todo_list) 
        total_duration_seconds = current_time - earliest_creation_time
        
    return str(timedelta(seconds=int(total_duration_seconds)))
            
# Function to handle mouse wheel scrolling
def on_mousewheel(event):
    """Handles mouse wheel scrolling for the canvas."""
    global canvas
    # Check if the event uses the standard 'delta' (Windows/macOS)
    if event.delta:
        # Scroll based on the delta value (typically -120 or 120), adjusting by a factor.
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    # Handle Linux buttons (Button-4 = scroll up, Button-5 = scroll down)
    elif event.num == 4:
        canvas.yview_scroll(-1, "units")
    elif event.num == 5:
        canvas.yview_scroll(1, "units")

def update_stats():
    """Calculates completed task count and total elapsed session time, updating the stats label in real-time."""
    global stats_label, root
    
    completed_count = 0
    
    # Find the count of completed tasks
    for _, status, _, _ in todo_list:
        if status:
            completed_count += 1
    
    # --- Calculate Elapsed Session Time using helper ---
    total_duration_str = calculate_session_duration_str()
    
    stats_text = (
        f"Completed: {completed_count} / {len(todo_list)} | "
        f"Elapsed Session Time: {total_duration_str}" # Renamed label for clarity
    )
    
    # Update the label if it has been created
    if stats_label:
        stats_label.config(text=stats_text)
        
    # Re-schedule this function to run again in 1000 milliseconds (1 second)
    if root:
        root.after(1000, update_stats) # Creates the real-time update loop


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
    global current_theme
    
    # Destroy all existing widgets inside the task_frame (the inner container).
    for widget in task_frame.winfo_children():
        widget.destroy()

    # Loop through every task in the backend list to create its corresponding widgets.
    for index, (task, status, _, _) in enumerate(todo_list): # Unpack data structure including time (unused here)
        # Create a variable to hold the state of the Checkbutton for the current task.
        var = tk.BooleanVar(value=status)
        
        # Determine the text decoration (strikethrough) and colors based on the status.
        font_config = ("Arial", 12)
        
        # --- VISUAL EFFECTS LOGIC ---
        if status:
            # If done, apply strikethrough, set text to dark gray, and set row background to pale gray.
            font_config = ("Arial", 12, "overstrike") 
            fg_color = current_theme['done_fg'] # Completed task text color
            row_bg_color = current_theme['done_bg'] # Completed task background color
        else:
            # If pending, use normal font, default text color, and list background color.
            fg_color = current_theme['default_fg'] 
            row_bg_color = current_theme['list_bg'] 

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

# --- Theme Switching Logic ---

def apply_theme_colors():
    """Applies the colors from the global current_theme dictionary to all main widgets."""
    
    # Apply colors to the root and main structures
    root.config(bg=current_theme['main_bg'])
    title_frame.config(bg=current_theme['main_bg'])
    add_control_frame.config(bg=current_theme['main_bg'])
    
    # Apply colors to title and labels
    title_label.config(bg=current_theme['main_bg'], fg=current_theme['title_fg'])
    stats_label.config(bg=current_theme['main_bg'], fg=current_theme['title_fg']) # New: Stats label color
    add_label.config(bg=current_theme['main_bg'], fg=current_theme['title_fg'])
    
    # Apply colors to buttons
    add_button.config(bg=current_theme['add_btn_bg'], fg=current_theme['title_fg'])
    exit_button.config(bg=current_theme['exit_btn_bg'], fg=current_theme['exit_btn_fg'])
    
    # Apply colors to the canvas and inner task frame
    canvas.config(background=current_theme['list_bg'])
    task_frame.config(background=current_theme['list_bg'])
    
    # Re-render the task list to apply new colors to individual Checkbuttons/Delete buttons
    update_task_list_display()

def change_theme_selection(event):
    """Callback function for the Combobox to switch the theme."""
    global current_theme
    
    # Get the selected theme name from the Combobox (event.widget is the Combobox)
    selected_theme_name = theme_selector.get()
    
    # Update the global theme dictionary
    current_theme = THEMES[selected_theme_name]
    
    # Update the main window title
    root.title(f"Python To-Do List GUI ({selected_theme_name} Theme)")
    
    # Update the list name to reflect the new theme
    list_title_var.set(f"{selected_theme_name} To-Do List")
    
    # Apply the new colors to the entire application
    apply_theme_colors()


# --- Custom Dialogs for Colored Input and Confirmation ---

class CustomAskStringDialog(tk.Toplevel):
    """Custom input dialog to allow background color customization."""
    # ADD fg_color to constructor
    def __init__(self, parent, title, prompt, bg_color, fg_color):
        super().__init__(parent)
        self.transient(parent)
        self.title(title)
        self.result = None
        self.parent = parent
        self.bg_color = bg_color
        self.fg_color = fg_color # Store fg_color
        self.config(bg=self.bg_color)
        
        self.parent.update_idletasks()
        w = self.winfo_reqwidth()
        h = self.winfo_reqheight()
        x = (self.parent.winfo_width() // 2) - (w // 2)
        y = (self.parent.winfo_height() // 2) - (h // 2)
        self.geometry('+%d+%d' % (x, y))

        self.create_widgets(prompt)
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.grab_set()
        self.wait_visibility() 

    def create_widgets(self, prompt):
        body = tk.Frame(self, bg=self.bg_color, padx=10, pady=10)
        body.pack(padx=5, pady=5)

        # USE self.fg_color for the prompt label
        tk.Label(body, text=prompt, bg=self.bg_color, font=("Arial", 12), fg=self.fg_color).pack(pady=5)

        self.entry = tk.Entry(body, width=30, font=("Arial", 12))
        self.entry.pack(pady=5)
        self.entry.bind("<Return>", lambda event: self.ok())
        self.entry.focus_set()

        button_frame = tk.Frame(self, bg=self.bg_color)
        button_frame.pack(pady=5, padx=10)

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
        self.result = self.entry.get()
        self.destroy()

    def cancel(self):
        self.result = None 
        self.destroy()

def custom_ask_string(parent, title, prompt):
    """Utility function to create and run the custom dialog, passing the current theme color."""
    # PASSES CURRENT THEME BG AND FG COLOR
    dialog = CustomAskStringDialog(parent, title, prompt, 
                                   bg_color=current_theme['main_bg'], 
                                   fg_color=current_theme['title_fg']) 
    parent.wait_window(dialog)
    return dialog.result

class CustomAskYesNoDialog(tk.Toplevel):
    """Custom Yes/No confirmation dialog with colored background."""
    # ADD fg_color to constructor
    def __init__(self, parent, title, message, bg_color, fg_color, button_texts=("Yes, Exit", "Cancel")):
        super().__init__(parent)
        self.transient(parent)
        self.title(title)
        self.result = False
        self.parent = parent
        self.bg_color = bg_color
        self.fg_color = fg_color # Store fg_color
        self.button_texts = button_texts # Store custom button texts
        self.config(bg=self.bg_color)
        
        self.parent.update_idletasks()
        w = 400
        h = 200
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

        # USE self.fg_color for the message label
        tk.Label(body, text=message, bg=self.bg_color, font=("Arial", 12), fg=self.fg_color, justify=tk.LEFT).pack(pady=10, fill='x')

        button_frame = tk.Frame(self, bg=self.bg_color)
        button_frame.pack(pady=5, padx=10)

        yes_button = tk.Button(
            button_frame, 
            text=self.button_texts[0], # Use custom text for YES button
            width=15, 
            command=self.yes_action,
            bg='#FFCCCC', 
            activebackground='#FF9999',
            fg='#800000',
            relief=tk.GROOVE
        )
        yes_button.pack(side=tk.LEFT, padx=5)

        no_button = tk.Button(
            button_frame, 
            text=self.button_texts[1], # Use custom text for NO button
            width=15, 
            command=self.no_action,
            bg='#CCDDDD', 
            activebackground='#DDFFFF',
            fg='#003333',
            relief=tk.GROOVE
        )
        no_button.pack(side=tk.LEFT, padx=5)
        
    def yes_action(self):
        self.result = True
        self.destroy()

    def no_action(self):
        self.result = False
        self.destroy()

def custom_ask_yes_no(parent, title, message, button_texts=("Yes, Delete", "No, Keep It")):
    """Utility function to create and run the custom yes/no dialog, passing the current theme color."""
    # PASSES CURRENT THEME BG AND FG COLOR
    dialog = CustomAskYesNoDialog(parent, title, message, 
                                  bg_color=current_theme['main_bg'], 
                                  fg_color=current_theme['title_fg'],
                                  button_texts=button_texts) 
    return dialog.result

def show_add_task_dialog():
    """Opens a custom colored dialog for task input and handles addition."""
    # Use the custom function which returns the entered string or None if cancelled.
    task = custom_ask_string(root, "Add Task", "Enter the new task:")
    # Check if the user entered any text (not empty) and didn't click Cancel.
    if task:
        # Call the backend logic to add the task.
        add_task_logic(task)
        # REMOVED confirmation message box for cleaner workflow
        # messagebox.showinfo("Success", f"Task '{task}' added!")

def show_exit_summary():
    """Calculates final session metrics, displays a summary, and exits if confirmed."""
    global root, max_tasks_ever_added

    # 1. Calculate metrics
    final_elapsed_time = calculate_session_duration_str()
    
    # 2. Build summary message
    summary_message = (
        f"Session Summary:\n\n"
        f"Tasks added (Max): {max_tasks_ever_added}\n"
        f"Total session duration: {final_elapsed_time}\n\n"
        f"Are you sure you want to end the session?"
    )

    # 3. Open custom confirmation dialog (repurposing custom_ask_yes_no)
    if custom_ask_yes_no(
        root, 
        "Session Complete & Exit", 
        summary_message,
        button_texts=("Yes, End Session", "Cancel")
    ):
        # If the user clicks 'Yes, End Session', destroy the main window
        root.destroy()


# --- Main Application Setup ---

# Rename initialize_main_app to main and remove selected_theme_name argument for simplicity
def main():
    """Initializes and runs the main To-Do List GUI."""
    global root, list_title_var, canvas, task_frame, title_frame, add_control_frame, title_label, add_label, add_button, exit_button, theme_selector, stats_label
    
    # 1. Initialize the main window (the root object).
    root = tk.Tk()
    
    # Set the title displayed in the window's title bar.
    root.title(f"Python To-Do List GUI (Calm Theme)")

    # FIX: Initialize the Tkinter string variable AFTER the root window is created.
    # Initialize a Tkinter string variable to hold the dynamic title of the list.
    list_title_var = tk.StringVar(value="Calm (Mint & Yellow) To-Do List")

    # Set the window to fullscreen mode.
    root.attributes('-fullscreen', True) 

    # --- UI LAYOUT CREATION ---

    # 2. Setup the Title Bar (Row 0).

    # Create a frame for the title and the "Set Name" button.
    title_frame = tk.Frame(root) 
    # Place the title frame at the top (Row 0), spanning both columns.
    title_frame.grid(row=0, column=0, columnspan=2, sticky='ew', padx=50, pady=(50, 20))
    # Configure the title frame grid so the title label expands.
    title_frame.grid_columnconfigure(0, weight=1)

    # Create the main Title Label, linked to the StringVar.
    title_label = tk.Label(
        title_frame,
        textvariable=list_title_var, # Uses the dynamic string variable
        font=("Arial", 28, "bold"),
    )
    # Place the title label on the left of the title frame, spanning two rows to make space for buttons.
    title_label.grid(row=0, column=0, rowspan=1, sticky='w')
    
    # NEW: Stats Label (Row 1, below the main title)
    stats_label = tk.Label(
        title_frame,
        text="", # Will be set by update_stats
        font=("Arial", 12),
        anchor='w'
    )
    # Place the stats label below the title in the title frame
    stats_label.grid(row=1, column=0, sticky='w', pady=(5, 0))


    # Create the "Set Name" button.
    set_name_button = tk.Button(
        title_frame,
        text="Set Name",
        command=set_list_name_gui, # New function call
        bg='#CCCCE6', # Soft Lavender (Fixed color for controls)
        activebackground='#DDDDFF',
        fg='#333366',
        relief=tk.FLAT
    )
    # Place the button in the top right corner of the title area (Row 0, Column 1).
    set_name_button.grid(row=0, column=1, sticky='e', padx=10)

    # NEW: Theme Selector Dropdown
    theme_selector = ttk.Combobox(
        title_frame,
        values=list(THEMES.keys()), # List of all defined theme names
        state="readonly", # User can only select from the list
        font=("Arial", 12)
    )
    theme_selector.set(list(THEMES.keys())[0]) # Set default theme as selected
    theme_selector.bind("<<ComboboxSelected>>", change_theme_selection) # Bind selection change to function
    # Place the theme selector next to the set name button (Row 0, Column 2)
    theme_selector.grid(row=0, column=2, sticky='e', padx=10)


    # 2.1 Setup the Add Task Control (New Row 1).
    # Create a frame for the Add Task button and label
    add_control_frame = tk.Frame(root)
    # Place the control frame immediately below the title bar (Row 1).
    add_control_frame.grid(row=1, column=0, columnspan=2, sticky='ew', padx=50, pady=(0, 10))
    # Configure the grid to push controls to the right.
    add_control_frame.grid_columnconfigure(0, weight=1) 

    # Add Task Label
    add_label = tk.Label(
        add_control_frame,
        text="Add Task:",
        font=("Arial", 12),
    )
    # Place the label to the right of the expanding space (Column 1).
    add_label.grid(row=0, column=1, sticky='e') 

    # NEW: Add Task Button setup (the "+" sign)
    add_button = tk.Button(
        add_control_frame, 
        text="+", 
        command=show_add_task_dialog,
        font=("Arial", 16, "bold"), 
        relief=tk.GROOVE # Slightly raised look
    )
    # Place the + button next to the label (Column 2).
    add_button.grid(row=0, column=2, sticky='e', padx=(5, 0)) 


    # 3. Setup the Canvas and Scrollbar for the task list (Now Row 2).

    # Create the Canvas widget.
    canvas = tk.Canvas(root, borderwidth=0) 
    # Create the vertical scrollbar.
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
    # Place the inner frame (task_frame) inside the canvas view.
    task_frame = tk.Frame(canvas) 

    # Configure the canvas to use the scrollbar for the y-axis.
    canvas.configure(yscrollcommand=scrollbar.set)

    # Place the scrollbar and canvas in the main window using grid.
    scrollbar.grid(row=2, column=1, sticky='ns') 
    canvas.grid(row=2, column=0, sticky='nsew', padx=50) 

    # Configure the grid to allow the canvas to expand when the window is resized.
    root.grid_rowconfigure(2, weight=1) 
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=0) 


    # Create a window inside the canvas to hold the task_frame.
    canvas.create_window((0, 0), window=task_frame, anchor="nw")
    # Bind the frame configuration event to adjust the canvas scroll region when the frame size changes.
    task_frame.bind("<Configure>", on_frame_configure)
    
    # Bind mouse wheel events to the canvas
    canvas.bind_all("<MouseWheel>", on_mousewheel)  # Windows/macOS
    canvas.bind_all("<Button-4>", on_mousewheel)    # Linux scroll up
    canvas.bind_all("<Button-5>", on_mousewheel)    # Linux scroll down


    # 4. Create the control buttons at the bottom (Now Rows 3).

    # Exit Button for fullscreen mode.
    exit_button = tk.Button(
        root,
        text="Done with all the tasks", 
        command=show_exit_summary, # NEW: Calls the summary function instead of destroying immediately
        relief=tk.GROOVE
    )
    # The button is placed in Row 3.
    exit_button.grid(row=3, column=0, columnspan=2, sticky='ew', padx=50, pady=(10, 50))

    # Optional: Bind the F11 key to toggle fullscreen/exit
    root.bind("<F11>", lambda event: root.attributes("-fullscreen", not root.attributes("-fullscreen")))

    # --- INITIAL SETUP & RUN ---
    
    # Apply the initial default theme colors to all widgets
    apply_theme_colors() 
    
    # Call the update function once to populate the list upon startup.
    update_task_list_display()
    update_stats() # New: Call update_stats initially, which starts the root.after loop
    
    # Start the event loop, which listens for user actions.
    root.mainloop()

if __name__ == "__main__":
    main()