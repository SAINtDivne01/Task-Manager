from flask import Flask, render_template, request, redirect, url_for # type: ignore

app = Flask(__name__)

# In-memory task storage
tasks = []


@app.route("/")
def index():
    return render_template("index.html", tasks=tasks)


@app.route("/add", methods=["POST"])
def add_task():
    task_title = request.form.get("title")
    task_description = request.form.get("description")
    if task_title:
        tasks.append({"title": task_title, "description": task_description, "completed": False})
    return redirect(url_for("index"))


@app.route("/complete/<int:task_id>")
def complete_task(task_id):
    if 0 <= task_id < len(tasks):
        tasks[task_id]["completed"] = True
    return redirect(url_for("index"))


@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
