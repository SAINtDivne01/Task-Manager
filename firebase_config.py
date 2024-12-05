import firebase_admin
from firebase_admin import credentials, auth, db
import requests
import threading
import random

# Firebase configuration
def initialize_firebase():
    cred = credentials.Certificate('C:/Users/ADMIN/Downloads/task-manager-c168c-firebase-adminsdk-2nn1y-23e88466f2.json')  # Update with your Firebase credentials file path
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://task-manager-c168c-default-rtdb.firebaseio.com/'  # Update with your database URL
    })

def register_user_in_firebase(username, password):
    try:
        user = auth.create_user(
            email=f"{username}@example.com",
            password=password
        )
        db.reference(f'users/{user.uid}').set({
            'username': username,
            'tasks': []
        })
        return True
    except Exception as e:
        return str(e)

def validate_login_with_firebase(username, password):
    try:
        auth.get_user_by_email(f"{username}@example.com")
        return True
    except Exception:
        return False

def save_tasks_to_firebase(user_uid, tasks):
    tasks_ref = db.reference(f'users/{user_uid}/tasks')
    tasks_ref.set(tasks)

def fetch_tasks_from_firebase(user_uid):
    tasks_ref = db.reference(f'users/{user_uid}/tasks')
    tasks = tasks_ref.get()
    return tasks if tasks else []


