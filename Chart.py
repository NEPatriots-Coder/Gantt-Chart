import tkinter as tk
from tkinter import ttk, messagebox
import requests

# Replace with your API endpoint from AWS Amplify
API_URL = "https://995xgiapz9.execute-api.us-east-1.amazonaws.com/Dev"


class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do App")
        self.create_widgets()
        self.load_tasks()

    def create_widgets(self):
        # --- Task List Section ---
        self.tree = ttk.Treeview(self.root, columns=("Task", "Status"), show="headings")
        self.tree.heading("Task", text="Task")
        self.tree.heading("Status", text="Status")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # --- New Task Input Section ---
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=5, padx=10, fill=tk.X)

        tk.Label(input_frame, text="New Task:").grid(row=0, column=0, sticky=tk.W)
        self.task_entry = tk.Entry(input_frame, width=40)
        self.task_entry.grid(row=0, column=1, padx=5)
        tk.Button(input_frame, text="Add Task", command=self.add_task).grid(row=0, column=2, padx=5)

        # --- Update Task Status Section ---
        update_frame = tk.Frame(self.root)
        update_frame.pack(pady=5, padx=10, fill=tk.X)

        tk.Label(update_frame, text="Update Selected Task Status:").grid(row=0, column=0, sticky=tk.W)
        self.status_var = tk.StringVar(value="Not Started")
        self.status_options = ["Not Started", "Started", "WIP", "Finished"]
        status_menu = tk.OptionMenu(update_frame, self.status_var, *self.status_options)
        status_menu.grid(row=0, column=1, padx=5)
        tk.Button(update_frame, text="Update Task", command=self.update_task_status).grid(row=0, column=2, padx=5)

    def load_tasks(self):
        """Load tasks from the backend API and populate the tree view."""
        try:
            response = requests.get(API_URL)
            if response.status_code == 200:
                tasks = response.json()
                print("API Response:", tasks)  # Inspect the API response
                # Clear the tree view first (if reloading)
                for item in self.tree.get_children():
                    self.tree.delete(item)
                # Insert each task; assuming each task has an 'id', 'task', and 'status' field.
                if isinstance(tasks, dict) and 'tasks' in tasks:
                    for task in tasks['tasks']:
                        self.tree.insert("", tk.END, iid=task["id"], values=(task["task"], task["status"]))
                else:
                    messagebox.showerror("Error", "Unexpected data structure from API. Consult print statement in terminal.")
            else:
                messagebox.showerror("Error", f"Failed to retrieve tasks. HTTP Status Code: {response.status_code}")
        except Exception as e:
            messagebox.showerror("Error", f"Error loading tasks: {e}")

    def add_task(self):
        """Add a new task using the REST API and update the UI."""
        task_text = self.task_entry.get().strip()
        if not task_text:
            messagebox.showwarning("Warning", "Task field cannot be empty.")
            return
        payload = {"task": task_text, "status": "Not Started"}
        try:
            response = requests.post(API_URL, json=payload)
            if response.status_code == 201:
                # Assumes the new task is returned with an 'id'
                task = response.json()
                self.tree.insert("", tk.END, iid=task["id"], values=(task["task"], task["status"]))
                self.task_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", f"Failed to add task. HTTP Status Code: {response.status_code}")
        except Exception as e:
            messagebox.showerror("Error", f"Error adding task: {e}")

    def update_task_status(self):
        """Update the selected task status via the REST API."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "No task selected for update.")
            return
        task_id = selected_item[0]
        new_status = self.status_var.get()
        payload = {"status": new_status}
        try:
            # Update the task using its unique ID
            url = f"{API_URL}/{task_id}"
            response = requests.put(url, json=payload)
            if response.status_code == 200:
                # Update succeeded: update the UI Treeview.
                current_values = self.tree.item(task_id, "values")
                self.tree.item(task_id, values=(current_values[0], new_status))
            else:
                messagebox.showerror("Error", f"Failed to update task. HTTP Status Code: {response.status_code}")
        except Exception as e:
            messagebox.showerror("Error", f"Error updating task: {e}")


if __name__ == '__main__':
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
