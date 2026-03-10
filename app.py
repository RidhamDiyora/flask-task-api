from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Task Model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)


with app.app_context():
    db.create_all()


# Health check route
@app.route("/")
def home():
    return jsonify({"message": "Task API is running"})


# Get all tasks
@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()

    result = [
        {
            "id": task.id,
            "title": task.title,
            "completed": task.completed
        }
        for task in tasks
    ]

    return jsonify(result), 200


# Create new task
@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()

    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    task = Task(title=data["title"])

    db.session.add(task)
    db.session.commit()

    return jsonify({
        "message": "Task created",
        "task_id": task.id
    }), 201


# Update task
@app.route("/tasks/<int:id>", methods=["PUT"])
def update_task(id):

    task = Task.query.get(id)

    if not task:
        return jsonify({"error": "Task not found"}), 404

    data = request.get_json()

    task.completed = data.get("completed", task.completed)

    db.session.commit()

    return jsonify({"message": "Task updated"}), 200


# Delete task
@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):

    task = Task.query.get(id)

    if not task:
        return jsonify({"error": "Task not found"}), 404

    db.session.delete(task)
    db.session.commit()

    return jsonify({"message": "Task deleted"}), 200


if __name__ == "__main__":
    app.run(debug=True)