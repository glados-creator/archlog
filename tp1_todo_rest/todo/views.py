from flask import jsonify, abort, make_response, request , url_for
from .app import app
from .models import tasks


def make_public_task(task):
    new_task = {}
    for field in task:
        if field =="id":
            new_task["uri"] = url_for("get_task", task_id=task["id"], _external=True)
        else:
            new_task[field] = task[field]
    return new_task


@app.route("/todo/api/v1.0/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks=[make_public_task(t) for t in tasks])

@app.route("/todo/api/v1.0/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    for t in tasks:
        if t["id"] == task_id:
            return jsonify(tasks=make_public_task(t))
    return make_response(jsonify({"error":"Not found"}), 404)

@app.route("/todo/api/v1.0/tasks", methods=["POST"])
def create_task():
    if not request.json or not"title" in request.json:
        abort(400)
    task = {
      "id": tasks[-1]["id"] + 1,
      "title": request.json["title"],
      "description": request.json.get("description",""),
      "done": False
    }
    tasks.append(task)
    return jsonify({"task": make_public_task(task)}), 201


@app.errorhandler (404)
def not_found ( error ):
    return make_response ( jsonify ( {"error":"Not found" } ), 404)

@app.errorhandler (418)
def not_found ( error ):
    return make_response ( jsonify ( {"error":"i am a teapot" } ), 418)

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({"error":"Not found"}), 400)


@app.route ("/todo/api/v1.0/tasks/<int:task_id>", methods = ["PUT"])
def update_task ( task_id ):
    task = [task for task in tasks if task["id"] == task_id ]
    if len (task) == 0:
        abort (404)
    if not request.json:
        abort (400)
    if"title" in request.json and type ( request.json["title"]) != str :
        abort (400)
    if"description" in request.json and type ( request.json["description"]) is not str :
        abort (400)
    if"done" in request .json and type ( request.json["done"]) is not bool :
        abort (400)
    task[0]["title"] = request.json.get("title", task[0]["title"])
    task[0]["description"] = request .json.get("description", task [0]["description"])
    task[0]["done"] = request.json.get("done", task [0]["done"])
    return jsonify ( {"task": make_public_task (task [0]) } )

@app.route ("/todo/api/v1.0/tasks/<int:task_id>", methods = ["DELETE"])
def delete_task ( task_id ):
    tmp = [index for index,task in enumerate(tasks) if task["id"] == task_id ]
    if len(tmp) == 0:
        abort(404)
    return jsonify(make_public_task(tasks.pop(tmp[0])))

## question


@app.route("/todo/api/v1.0/questionnaire", methods=["GET"])
def get_questionnaire():
    return jsonify(questionnaire=[make_public_question(t) for t in questionnaire])

@app.route("/todo/api/v1.0/questionnaire/<int:question_id>", methods=["GET"])
def get_question(question_id):
    for t in questionnaire:
        if t["id"] == question_id:
            return jsonify(questionnaire=make_public_question(t))
    return make_response(jsonify({"error":"Not found"}), 404)

@app.route("/todo/api/v1.0/questionnaire", methods=["POST"])
def create_question():
    if not request.json or not"title" in request.json:
        abort(400)
    question = {
      "id": questionnaire[-1]["id"] + 1,
      "title": request.json["title"],
      "description": request.json.get("description",""),
      "done": False
    }
    questionnaire.append(question)
    return jsonify({"question": make_public_question(question)}), 201


@app.route ("/todo/api/v1.0/questionnaire/<int:question_id>", methods = ["PUT"])
def update_question ( question_id ):
    question = [question for question in questionnaire if question["id"] == question_id ]
    if len (question) == 0:
        abort (404)
    if not request.json:
        abort (400)
    if"title" in request.json and type ( request.json["title"]) != str :
        abort (400)
    if"description" in request.json and type ( request.json["description"]) is not str :
        abort (400)
    if"done" in request .json and type ( request.json["done"]) is not bool :
        abort (400)
    question[0]["title"] = request.json.get("title", question[0]["title"])
    question[0]["description"] = request .json.get("description", question [0]["description"])
    question[0]["done"] = request.json.get("done", question [0]["done"])
    return jsonify ( {"question": make_public_question (question [0]) } )

@app.route ("/todo/api/v1.0/questionnaire/<int:question_id>", methods = ["DELETE"])
def delete_question ( question_id ):
    tmp = [index for index,question in enumerate(questionnaire) if question["id"] == question_id ]
    if len(tmp) == 0:
        abort(404)
    return jsonify(make_public_question(questionnaire.pop(tmp[0])))

#### question

@app.route("/todo/api/v1.0/questions", methods=["GET"])
def get_questions():
    return jsonify(questions=[make_public_question(t) for t in questions])

@app.route("/todo/api/v1.0/questions/<int:question_id>", methods=["GET"])
def get_question(question_id):
    for t in questions:
        if t["id"] == question_id:
            return jsonify(questions=make_public_question(t))
    return make_response(jsonify({"error":"Not found"}), 404)

@app.route("/todo/api/v1.0/questions", methods=["POST"])
def create_question():
    if not request.json or not"title" in request.json:
        abort(400)
    question = {
      "id": questions[-1]["id"] + 1,
      "title": request.json["title"],
      "description": request.json.get("description",""),
      "done": False
    }
    questions.append(question)
    return jsonify({"question": make_public_question(question)}), 201


@app.route ("/todo/api/v1.0/questions/<int:question_id>", methods = ["PUT"])
def update_question ( question_id ):
    question = [question for question in questions if question["id"] == question_id ]
    if len (question) == 0:
        abort (404)
    if not request.json:
        abort (400)
    if"title" in request.json and type ( request.json["title"]) != str :
        abort (400)
    if"description" in request.json and type ( request.json["description"]) is not str :
        abort (400)
    if"done" in request .json and type ( request.json["done"]) is not bool :
        abort (400)
    question[0]["title"] = request.json.get("title", question[0]["title"])
    question[0]["description"] = request .json.get("description", question [0]["description"])
    question[0]["done"] = request.json.get("done", question [0]["done"])
    return jsonify ( {"question": make_public_question (question [0]) } )

@app.route ("/todo/api/v1.0/questions/<int:question_id>", methods = ["DELETE"])
def delete_question ( question_id ):
    tmp = [index for index,question in enumerate(questions) if question["id"] == question_id ]
    if len(tmp) == 0:
        abort(404)
    return jsonify(make_public_question(questions.pop(tmp[0])))