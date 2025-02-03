from flask import jsonify, abort, make_response, request, url_for
from .app import app
from .models import *


from .app import app, login_manager
from .models import User
# from flask_wtf import FlaskForm
# from wtforms import StringField, HiddenField, PasswordField
# from wtforms.validators import DataRequired
# from hashlib import sha256
from flask_login import login_user, current_user, login_required

##################### TO DO #####################

def make_public_task(taskT : Tasks):
    task = mget_task(taskT.id).to_json()
    new_task = {}
    for field in task:
        if field =="id":
            new_task["uri"] = url_for("get_task", task_id=task["id"], _external=True)
        else:
            new_task[field] = task[field]
    return new_task

@app.route("/todo/api/v1.0/tasks", methods=["GET"])
def get_tasks():
    tasks = mget_tasks()
    return jsonify(tasks=[make_public_task(t) for t in tasks])

@app.route("/todo/api/v1.0/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = mget_task(task_id)
    return jsonify(task=make_public_task(task))

@app.route("/todo/api/v1.0/tasks", methods=["POST"])
def create_task():
    if not request.json or "title" not in request.json:
        abort(400, description="Missing title in request body")

    new_task = mcreate_task(title=request.json["title"],description=request.json.get("description", ""))

    return jsonify({"task": make_public_task(new_task)}), 201

@app.route("/todo/api/v1.0/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    task = mget_task(task_id)

    if not request.json:
        abort(400, description="Missing JSON request body")

    if "title" in request.json and not isinstance(request.json["title"], str):
        abort(400, description="Title must be a string")
    if "description" in request.json and not isinstance(request.json["description"], str):
        abort(400, description="Description must be a string")
    if "done" in request.json and not isinstance(request.json["done"], bool):
        abort(400, description="Done must be a boolean")

    task.title = request.json.get("title", task.title)
    task.description = request.json.get("description", task.description)
    task.done = request.json.get("done", task.done)

    db.session.commit()
    return jsonify({"task": make_public_task(task)})

@app.route("/todo/api/v1.0/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = mdelete_tasks(task_id)
    return jsonify({"message": "Task deleted successfully", "task": make_public_task(task)})


##################### QUIZZ #####################

# User loader function


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(0)
    # return User.query.get(user_id)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)


@app.errorhandler(418)
def not_found(error):
    return make_response(jsonify({"error": "i am a teapot"}), 418)


@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 400)

# question


@app.route("/quizz/api/v1.0/login", methods=["GET", "POST", "PUT", "DELETE"])
def login():
    login_user(load_user(0), remember=True)
    return make_response(jsonify({"status": "success", "userid": current_user.id}), 400)


@app.route("/quizz/api/v1.0/questionnaire", methods=["GET"])
def get_questionnaires():
    return make_response(jsonify(questionnaire=mget_questionnaires()), 400)


@app.route("/quizz/api/v1.0/questionnaire/<int:question_id>", methods=["GET"])
def get_questionnaire(question_id):
    return make_response(jsonify(questionnaire=mget_questionnaire(question_id)), 404)


@login_required
@app.route("/quizz/api/v1.0/questionnaire/<int:question_id>", methods=["POST"])
def create_questionnaire():
    if not request.json or not "title" in request.json:
        abort(400)
    return make_response(jsonify(questionnaire=madd_questionnaire(request.json["title"])), 400)


@login_required
@app.route("/quizz/api/v1.0/questionnaire/<int:question_id>", methods=["PUT"])
def update_questionnaire(question_id):
    abort(404)


@login_required
@app.route("/quizz/api/v1.0/questionnaire/<int:question_id>", methods=["DELETE"])
def delete_questionnaire(question_id):
    return make_response(jsonify(questionnaire=mdelete_questionnaire(mget_questionnaire(question_id))), 400)

# question


@app.route("/quizz/api/v1.0/question/<int:question_id>", methods=["GET"])
def get_question(question_id):
    return make_response(jsonify(question=mget_question(question_id)), 400)


@login_required
@app.route("/quizz/api/v1.0/question/<title>/<reponse>/<int:id_questionnaire>", methods=["POST"])
def create_question(title, reponse, id_questionnaire):
    abort(400)


@login_required
@app.route("/quizz/api/v1.0/questions/<int:question_id>", methods=["PUT"])
def update_question(question_id):
    abort(404)


@login_required
@app.route("/quizz/api/v1.0/questions/<int:question_id>", methods=["DELETE"])
def delete_question(question_id):
    return make_response(jsonify(question=mdelete_question(mget_question(question_id))), 400)


# reponse

@login_required
@app.route("/quizz/api/v1.0/questions/<int:question_id>/<reponse>", methods=["POST"])
def update_reponse(question_id, reponse):
    return make_response(jsonify(reponse=madd_reponse(mget_question(question_id), current_user, reponse)), 400)
