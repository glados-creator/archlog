from flask import jsonify, abort, make_response, request, url_for
from .app import app
from .models import *

from .app import app, db, login_manager
from .models import User
# from flask_wtf import FlaskForm
# from wtforms import StringField, HiddenField, PasswordField
# from wtforms.validators import DataRequired
# from hashlib import sha256
from flask_login import login_user, current_user, logout_user, login_required

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


@app.route("/quizz/api/v1.0/login", methods=["GET","POST","PUT","DELETE"])
def login():
    login_user(load_user(0), remember=True)
    return make_response(jsonify({"status": "success","userid":current_user.id}), 400)


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
