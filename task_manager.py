import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox, StringVar, Toplevel
from firebase_config import *  # Import Firebase-related functions



class TaskManagerApp:
    def __init__(self, root):
        # Set style and theme
        self.style = ttk.Style(theme="cosmo")
        self.root = root
        self.root.title("Task Manager")
        self.root.state("zoomed")
        self.root.resizable(True, True)

        # Layout: Sidebar and Main Content
        self.create_sidebar()
        self.create_main_content()
        

        # Login Management
        self.current_user_uid = None
        self.login_window = self.create_login_window()
        self.root.withdraw()

    def create_sidebar(self):
        # Sidebar Layout
        self.sidebar = ttk.Frame(self.root, padding=10, bootstyle="light")
        self.sidebar.pack(side="left", fill="y")

        

        # Task Progress Section
        self.progress_label = ttk.Label(
            self.sidebar,
            text="Task Progress",
            bootstyle="primary",
            font=("Helvetica", 14, "bold"),
            anchor="center"
        )
        self.progress_label.pack(pady=5)

        self.progress_bar = ttk.Progressbar(
            self.sidebar, bootstyle="success-striped", mode="determinate", length=200
        )
        self.progress_bar.pack(fill="x", pady=10)

        ttk.Separator(self.sidebar).pack(fill="x", pady=5)

        # Logout Button (Bottom)
        self.logout_button = ttk.Button(
            self.sidebar,
            text="Logout",
            bootstyle="outline-danger",
            command=self.logout
        )
        self.logout_button.pack(side="bottom", fill="x", pady=20)
        

    def create_main_content(self):
        # Main Frame
        self.main_frame = ttk.Frame(self.root, padding=10)
        self.main_frame.pack(side="right", expand=True, fill="both")

        # Notebook for Tasks
        self.notebook = ttk.Notebook(self.main_frame, bootstyle="info")
        self.task_tab = ttk.Frame(self.notebook, padding=10)
        self.completed_tab = ttk.Frame(self.notebook, padding=10)

        self.notebook.add(self.task_tab, text=" Active Tasks")
        self.notebook.add(self.completed_tab, text=" Completed Tasks")
        self.notebook.pack(expand=True, fill="both")

        # Search Bar for Active Tasks
        search_frame = ttk.Frame(self.task_tab, padding=5)
        search_frame.pack(fill="x", pady=5)
    
        search_label = ttk.Label(search_frame, text="Search:", font=("Helvetica", 12))
        search_label.pack(side="left", padx=5)

        self.search_var = StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side="left", padx=5)
        search_entry.bind("<KeyRelease>", lambda e: self.filter_tasks())

        # Active Task List
        ttk.Label(self.task_tab, text="Active Tasks", font=("Helvetica", 14, "bold")).pack(anchor="w", pady=5)
        self.active_task_tree = ttk.Treeview(
            self.task_tab,
            columns=("Task", "Priority"),
            show="headings",
            bootstyle="info",
        )
        self.active_task_tree.heading("Task", text="Task Description")
        self.active_task_tree.heading("Priority", text="Priority")
        self.active_task_tree.pack(fill="both", expand=True, pady=5)

        self.add_task_button = ttk.Button(
            self.task_tab, text="Add Task", bootstyle="success", command=self.add_task
        )
        self.add_task_button.pack(side="left", padx=5, pady=10)

        self.mark_complete_button = ttk.Button(
            self.task_tab, text="Mark as Complete", bootstyle="info", command=self.mark_task_as_completed
        )
        self.mark_complete_button.pack(side="right", padx=5, pady=10)

        # Completed Task List
        ttk.Label(self.completed_tab, text="Completed Tasks", font=("Helvetica", 14, "bold")).pack(anchor="w", pady=5)
        self.completed_task_tree = ttk.Treeview(
            self.completed_tab,
            columns=("Task", "Priority"),
            show="headings",
            bootstyle="success",
        )
        self.completed_task_tree.heading("Task", text="Task Description")
        self.completed_task_tree.heading("Priority", text="Priority")
        self.completed_task_tree.pack(fill="both", expand=True, pady=10)

    def create_login_window(self):
        login_window = Toplevel(self.root)
        login_window.title("Login")
        self.center_window(login_window, 400, 300)

        # Login Frame
        login_frame = ttk.Frame(login_window, padding=20)
        login_frame.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(login_frame, text="Login to Task Manager", font=("Helvetica", 16, "bold")).pack(pady=10)

        # Username Input
        username_label = ttk.Label(login_frame, text="Username", font=("Helvetica", 12))
        username_label.pack(pady=5)
        username_entry = ttk.Entry(login_frame, width=30)
        username_entry.pack(pady=5)

        # Password Input
        password_label = ttk.Label(login_frame, text="Password", font=("Helvetica", 12))
        password_label.pack(pady=5)
        password_entry = ttk.Entry(login_frame, show="*", width=30)
        password_entry.pack(pady=5)

        # Login Button
        login_button = ttk.Button(
            login_frame, text="Login", bootstyle="success",
            command=lambda: self.login(username_entry, password_entry)
        )
        login_button.pack(pady=10)

        # Register Button
        register_button = ttk.Button(
            login_frame, text="Register", bootstyle="info",
            command=lambda: self.register(username_entry, password_entry)
        )
        register_button.pack()

        return login_window

    def add_task(self):
        task_window = Toplevel(self.root)
        task_window.title("Add Task")
        self.center_window(task_window, 400, 300)

        # Add Task Frame
        ttk.Label(task_window, text="Task Description", font=("Helvetica", 12)).pack(pady=10)
        task_entry = ttk.Entry(task_window, width=30)
        task_entry.pack(pady=5)

        ttk.Label(task_window, text="Priority", font=("Helvetica", 12)).pack(pady=10)
        priority_options = ["Low", "Medium", "High"]
        priority_var = StringVar(value="Medium")
        priority_menu = ttk.OptionMenu(task_window, priority_var, *priority_options)
        priority_menu.pack(pady=5)

        ttk.Button(
            task_window, text="Add Task", bootstyle="success",
            command=lambda: self.save_task(task_entry.get(), priority_var.get(), task_window)
        ).pack(pady=10)

    def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")

    def save_task(self, description, priority, task_window):
        if not description:
            messagebox.showerror("Error", "Task description cannot be empty.")
            return
        tasks = fetch_tasks_from_firebase(self.current_user_uid)
        tasks.append({"description": description, "priority": priority, "completed": False})
        save_tasks_to_firebase(self.current_user_uid, tasks)
        self.update_task_listbox()
        task_window.destroy()

    def mark_task_as_completed(self):
        selected_task = self.active_task_tree.selection()
        if not selected_task:
            messagebox.showerror("Error", "No task selected.")
            return
        task_index = int(self.active_task_tree.index(selected_task[0]))
        tasks = fetch_tasks_from_firebase(self.current_user_uid)
        active_tasks = [task for task in tasks if not task["completed"]]
        task_to_complete = active_tasks[task_index]
        task_to_complete["completed"] = True
        save_tasks_to_firebase(self.current_user_uid, tasks)
        self.update_task_listbox()

    def update_task_listbox(self):
        tasks = fetch_tasks_from_firebase(self.current_user_uid)

        # Update Active Tasks
        self.active_task_tree.delete(*self.active_task_tree.get_children())
        self.completed_task_tree.delete(*self.completed_task_tree.get_children())

        completed_tasks = 0
        for task in tasks:
            if task["completed"]:
                self.completed_task_tree.insert("", "end", values=(task["description"], task["priority"]))
                completed_tasks += 1
            else:
                self.active_task_tree.insert("", "end", values=(task["description"], task["priority"]))

        self.update_progress_bar(completed_tasks, len(tasks))

    def update_progress_bar(self, completed, total):
        self.progress_bar["value"] = (completed / total) * 100 if total > 0 else 0

    def logout(self):
        self.root.withdraw()
        self.login_window = self.create_login_window()

    def login(self, username_entry, password_entry):
        username = username_entry.get()
        password = password_entry.get()

        if validate_login_with_firebase(username, password):
            self.current_user_uid = auth.get_user_by_email(f"{username}@example.com").uid
            self.login_window.destroy()
            self.root.deiconify()
            self.root.state("zoomed")
            self.update_task_listbox()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def register(self, username_entry, password_entry):
        username = username_entry.get()
        password = password_entry.get()

        result = register_user_in_firebase(username, password)
        if result is True:
            self.login(username_entry, password_entry)
        else:
            messagebox.showerror("Registration Failed", result)
            
    def filter_tasks(self):
        search_term = self.search_var.get().lower()  # Get search term from the search bar
        tasks = fetch_tasks_from_firebase(self.current_user_uid)  # Fetch tasks from Firebase

    # Filter tasks based on the search term
        filtered_tasks = [
        task for task in tasks if search_term in task["description"].lower()
    ]

    # Clear the current task tree
        self.active_task_tree.delete(*self.active_task_tree.get_children())

    # Populate the task tree with filtered tasks
        for task in filtered_tasks:
         if not task["completed"]:
            self.active_task_tree.insert("", "end", values=(task["description"], task["priority"]))



if __name__ == "__main__":
    from tkinter import Tk
    root = Tk()
    app = TaskManagerApp(root)
    root.mainloop()
