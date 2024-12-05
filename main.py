from task_manager import TaskManagerApp
from firebase_config import initialize_firebase
import ttkbootstrap as ttk

if __name__ == "__main__":
    initialize_firebase()  # Initialize Firebase
    root = ttk.Window(themename="darkly")
    app = TaskManagerApp(root)
    root.mainloop()
