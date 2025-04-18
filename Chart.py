import tkinter as tk
from tkinter import ttk, messagebox

class GanttChartApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To do Task List for Lamar")
        self.tasks = []  # Local in-memory storage for tasks
        self.create_widgets()
        self.draw_chart()  # Draw an initial empty chart

    def create_widgets(self):
        # --- Input Section for Adding a New Task ---
        input_frame = tk.Frame(self.root)
        input_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        # Task Name
        tk.Label(input_frame, text="Task:").grid(row=0, column=0, padx=5, pady=2)
        self.task_entry = tk.Entry(input_frame)
        self.task_entry.grid(row=0, column=1, padx=5, pady=2)

        # Task Start (day, time unit)
        tk.Label(input_frame, text="Start (day):").grid(row=0, column=2, padx=5, pady=2)
        self.start_entry = tk.Entry(input_frame, width=5)
        self.start_entry.grid(row=0, column=3, padx=5, pady=2)

        # Task Duration (in days)
        tk.Label(input_frame, text="Duration (days):").grid(row=0, column=4, padx=5, pady=2)
        self.duration_entry = tk.Entry(input_frame, width=5)
        self.duration_entry.grid(row=0, column=5, padx=5, pady=2)

        # Task Status
        tk.Label(input_frame, text="Status:").grid(row=0, column=6, padx=5, pady=2)
        self.status_var = tk.StringVar(value="Not Started")
        status_options = ["Not Started", "Started", "WIP", "Finished"]
        self.status_menu = tk.OptionMenu(input_frame, self.status_var, *status_options)
        self.status_menu.grid(row=0, column=7, padx=5, pady=2)

        # Add Task Button
        tk.Button(input_frame, text="Add Task", command=self.add_task).grid(row=0, column=8, padx=5, pady=2)

        # --- Canvas Section to Draw the Gantt Chart ---
        self.canvas = tk.Canvas(self.root, bg="white", height=400, width=800)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def add_task(self):
        """Read input fields, add the task to the list, and redraw the chart."""
        task_name = self.task_entry.get().strip()
        if not task_name:
            messagebox.showwarning("Warning", "Task name cannot be empty.")
            return

        try:
            start_day = float(self.start_entry.get())
            duration = float(self.duration_entry.get())
        except ValueError:
            messagebox.showwarning("Warning", "Start and Duration must be numbers.")
            return

        status = self.status_var.get()
        # Create a simple task dictionary. An 'id' is generated by incrementing the task count.
        new_task = {
            "id": len(self.tasks) + 1,
            "task": task_name,
            "start": start_day,
            "duration": duration,
            "status": status
        }
        self.tasks.append(new_task)
        self.clear_entries()
        self.draw_chart()

    def clear_entries(self):
        """Clear input fields after adding a task."""
        self.task_entry.delete(0, tk.END)
        self.start_entry.delete(0, tk.END)
        self.duration_entry.delete(0, tk.END)

    def draw_chart(self):
        """Redraw the Gantt chart on the canvas using local task data."""
        self.canvas.delete("all")  # Clear the canvas first

        # Set up drawing parameters.
        left_margin = 100  # Reserve space for task labels
        day_width = 50     # Pixels per time unit (day)
        row_height = 30    # Height of each task row
        top_margin = 40    # Space at the top for the timeline

        # Determine the end of the timeline (max end time among tasks or a default if none)
        if self.tasks:
            max_day = max(task["start"] + task["duration"] for task in self.tasks)
        else:
            max_day = 10
        timeline_end = int(max_day) + 1

        # --- Draw the Time Axis at the Top ---
        for day in range(0, timeline_end + 1):
            x = left_margin + day * day_width
            self.canvas.create_line(x, top_margin - 20, x, 400, fill="lightgray")
            self.canvas.create_text(x + day_width/2, top_margin - 30, text=str(day))

        # Define color mapping based on task status.
        status_colors = {
            "Not Started": "gray",
            "Started": "blue",
            "WIP": "orange",
            "Finished": "green"
        }

        # --- Draw Each Task as a Bar on the Chart ---
        for idx, task in enumerate(self.tasks):
            y = top_margin + idx * row_height + 10  # Calculate vertical position for this task row
            x_start = left_margin + task["start"] * day_width
            x_end = x_start + task["duration"] * day_width
            color = status_colors.get(task["status"], "black")

            # Draw the rectangle (bar) for the task.
            self.canvas.create_rectangle(x_start, y, x_end, y + row_height - 10, fill=color, outline="black")
            # Draw the task name on the left margin.
            self.canvas.create_text(10, y + (row_height / 2) - 5, text=task["task"], anchor="w")

if __name__ == '__main__':
    root = tk.Tk()
    app = GanttChartApp(root)
    root.mainloop()
