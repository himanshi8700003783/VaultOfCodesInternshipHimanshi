import tkinter as tk
from tkinter import messagebox
import json
from tkinter import simpledialog, ttk

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal To-Do List")
        self.root.geometry("500x600")
        self.tasks_file = 'tasks.json'
        self.tasks = self.load_tasks()  # Load existing tasks

        # Create UI components
        self.create_widgets()

    def create_widgets(self):
        """Create the main UI components."""
        # Task List Frame
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=10)

        # Task Listbox
        self.task_listbox = tk.Listbox(self.frame, height=15, width=50, selectmode=tk.SINGLE)
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        
        # Scrollbar for the Listbox
        self.scrollbar = tk.Scrollbar(self.frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.task_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.task_listbox.yview)

        # Buttons Frame
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=20)

        # Add Task Button
        self.add_button = tk.Button(self.button_frame, text="Add Task", command=self.add_task)
        self.add_button.pack(side=tk.LEFT, padx=5)

        # Mark Completed Button
        self.complete_button = tk.Button(self.button_frame, text="Mark Completed", command=self.mark_task_completed)
        self.complete_button.pack(side=tk.LEFT, padx=5)

        # Delete Task Button
        self.delete_button = tk.Button(self.button_frame, text="Delete Task", command=self.delete_task)
        self.delete_button.pack(side=tk.LEFT, padx=5)

        # Summary Button
        self.summary_button = tk.Button(self.button_frame, text="View Summary", command=self.view_summary)
        self.summary_button.pack(side=tk.LEFT, padx=5)

        # Exit Button
        self.exit_button = tk.Button(self.button_frame, text="Exit", command=self.root.quit)
        self.exit_button.pack(side=tk.LEFT, padx=5)

        # Update the Listbox with loaded tasks
        self.update_task_listbox()

    def load_tasks(self):
        """Load tasks from the JSON file."""
        try:
            with open(self.tasks_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save_tasks(self):
        """Save the current tasks to the JSON file."""
        with open(self.tasks_file, 'w') as f:
            json.dump(self.tasks, f, indent=4)  # Pretty print the JSON for readability

    def update_task_listbox(self):
        """Update the Listbox with the current tasks."""
        self.task_listbox.delete(0, tk.END)  # Clear the current Listbox
        for task in self.tasks:
            status = "✓" if task['completed'] else "✗"
            self.task_listbox.insert(tk.END, f"{task['title']} - {status} ({task['category']})")

    def add_task(self):
        """Prompt the user to add a new task."""
        title = simpledialog.askstring("Input", "Enter the task title:")
        description = simpledialog.askstring("Input", "Enter the task description:")
        category = simpledialog.askstring("Input", "Enter the task category:")

        if title and description and category:
            task = {
                "title": title,
                "description": description,
                "category": category,
                "completed": False
            }
            self.tasks.append(task)  # Add new task
            self.save_tasks()  # Save the new task
            self.update_task_listbox()  # Refresh the task list
            messagebox.showinfo("Success", "Task added successfully!")
        else:
            messagebox.showwarning("Input Error", "All fields are required!")

    def mark_task_completed(self):
        """Mark the selected task as completed."""
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            task_index = selected_task_index[0]
            self.tasks[task_index]['completed'] = True  # Update the task's completion status
            self.save_tasks()  # Save the updated tasks
            self.update_task_listbox()  # Refresh the task list
            messagebox.showinfo("Success", "Task marked as completed!")
        else:
            messagebox.showwarning("Selection Error", "Please select a task to mark as completed.")

    def delete_task(self):
        """Delete the selected task from the list."""
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            task_index = selected_task_index[0]
            del self.tasks[task_index]  # Remove the task from the list
            self.save_tasks()  # Save the updated tasks
            self.update_task_listbox()  # Refresh the task list
            messagebox.showinfo("Success", "Task deleted successfully!")
        else:
            messagebox.showwarning("Selection Error", "Please select a task to delete.")

    def view_summary(self):
        """Display a summary of all tasks in a message box."""
        summary = ""
        for task in self.tasks:
            summary += f"Title: {task['title']}\nCategory: {task['category']}\nCompleted: {'Yes' if task['completed'] else 'No'}\n\n"
        if summary:
            messagebox.showinfo("Task Summary", summary)
        else:
            messagebox.showinfo("Task Summary", "No tasks available.")

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
