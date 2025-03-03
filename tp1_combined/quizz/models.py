from sqlalchemy import Column, Float, Integer, Text, Date, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy import func
from .app import db, app, login_manager
from flask_login import UserMixin
from typing import List, Optional
# quizz

class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(100))
    done = db.Column(db.Boolean())

    def to_json(self):
        return {
            "id" : self.id,
            "title" : self.title,
            "description" : self.description,
            "done" : self.done
        }


def mget_tasks():
    tasks = Tasks.query.all()  # Fetch all tasks
    return [task.to_json() for task in tasks]  # Use existing to_json method

def mget_task(task_id):
    return Tasks.query.get_or_404(task_id)

def mcreate_task(title, description=""):
    new_task = Tasks(title=title, description=description, done=False)
    db.session.add(new_task)
    db.session.commit()
    return new_task

def mdelete_tasks(task_id):
    task = Tasks.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return task


from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from .app import db  # Assuming db is imported from your app module

# (Many-to-Many tables)
asso_questionnaires = db.Table(
    'asso_questionnaires',
    db.Column('user_id', db.String(50), db.ForeignKey('user.U_username')),
    db.Column('questionnaire_id', db.Integer, db.ForeignKey('questionnaire.id'))
)

asso_questions = db.Table(
    'asso_questions',
    db.Column('user_id', db.String(50), db.ForeignKey('user.U_username')),
    db.Column('question_id', db.Integer, db.ForeignKey('question.id'))
)

class Questionnaire(db.Model):
    __tablename__ = "questionnaire"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    questions = db.relationship("Question", backref="questionnaire", lazy="dynamic")

    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return str(self.to_json())

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "questions": [q.to_json() for q in self.questions]  # Full question objects
        }

    def to_json_short(self) -> dict:
        return {
            "id": self.id,
            "name": self.name
        }

class Question(db.Model):
    __tablename__ = "question"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    reponse = db.Column(db.String(120))
    questionnaire_id = db.Column(db.Integer, db.ForeignKey("questionnaire.id"))

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "reponse": self.reponse,
            "questionnaire_id": self.questionnaire_id,
            "reponses": [r.to_json_short() for r in self.reponses]  # Shortened responses
        }

    def to_json_short(self) -> dict:
        return {
            "id": self.id,
            "title": self.title
        }

class Reponse(db.Model):
    __tablename__ = "reponse"
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"), nullable=False)
    user_id = db.Column(db.String(50), db.ForeignKey("user.U_username"), nullable=False)
    reponse = db.Column(db.String(120))

    question = db.relationship("Question", backref=db.backref("reponses", lazy="dynamic"))

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "question_id": self.question_id,
            "user_id": self.user_id,
            "reponse": self.reponse,
            "question": self.question.to_json_short() if self.question else None  # Shortened question
        }

    def to_json_short(self) -> dict:
        return {
            "id": self.id,
            "reponse": self.reponse  # Using reponse as the "title-like" field
        }

class User(db.Model, UserMixin):
    __tablename__ = "user"
    U_username = db.Column(db.String(50), primary_key=True)
    U_password = db.Column(db.String(64))

    questionnaires = db.relationship('Questionnaire',
                                     secondary=asso_questionnaires,
                                     lazy='subquery',
                                     backref=db.backref('answered_by', lazy=True))
    questions = db.relationship('Question',
                                secondary=asso_questions,
                                lazy='subquery',
                                backref=db.backref('answered_by', lazy=True))
    reponses = db.relationship("Reponse", backref=db.backref("user", lazy="select"))

    def to_json(self) -> dict:
        return {
            "U_username": self.U_username,
            "questionnaires": [q.to_json_short() for q in self.questionnaires],  # Shortened questionnaires
            "questions": [q.to_json_short() for q in self.questions],  # Shortened questions
            "reponses": [r.to_json_short() for r in self.reponses]  # Shortened responses
        }

    def to_json_short(self) -> dict:
        return {
            "id": self.U_username,  # Using U_username as the ID
            "U_username": self.U_username
        }

def mget_max_id(table: type) -> int:
    max_id = db.session.query(func.max(table.id)).scalar()
    next_id = (max_id or 0) + 1
    return next_id

def mget_questionnaires() -> List[dict]:
    questionnaires = Questionnaire.query.all()
    return [{"id": q.id, "name": q.name} for q in questionnaires]

def mget_questionnaire(id: int) -> Questionnaire:
    return Questionnaire.query.get_or_404(id)

def mget_question(id: int) -> Question:
    return Question.query.get_or_404(id)

def mget_reponse(id: int) -> Reponse:
    return Reponse.query.get_or_404(id)

def muget_questionnaire(user: User) -> List[Questionnaire]:
    return user.questionnaires

def muget_question(user: User, questionnaire_id: int) -> List[Question]:
    # Fixed: Filter questionnaires by ID and return its questions
    questionnaire = next((q for q in user.questionnaires if q.id == questionnaire_id), None)
    return questionnaire.questions.all() if questionnaire else []

def muget_reponse(user: User) -> List[Reponse]:
    # Fixed: Return all responses for the user instead of get_or_404
    return user.reponses

def mdelete_questionnaire(questionnaire: Questionnaire) -> Questionnaire:
    db.session.delete(questionnaire)
    db.session.commit()
    return questionnaire

def mdelete_question(question: Question) -> Question:
    db.session.delete(question)
    db.session.commit()
    return question

def madd_questionnaire(title: str) -> Questionnaire:
    q = Questionnaire(title)
    db.session.add(q)
    db.session.commit()
    return q

def madd_question(questionnaire: Questionnaire, title: str, reponse: str) -> Question:
    q = Question(title=title, questionnaire=questionnaire, reponse=reponse)
    db.session.add(q)
    db.session.commit()
    return q

def madd_reponse(question: Question, user: User, reponse: str) -> Reponse:
    q = Reponse(question=question, user=user, reponse=reponse)
    db.session.add(q)
    db.session.commit()
    return q

def mget_user(id: str) -> Optional[User]:
    # Fixed: Use the provided id instead of hardcoded 0
    return User.query.get(id)  # Returns None if not found, unlike get_or_404
    # Uncomment and use this if you prefer 404 behavior:
    # return User.query.get_or_404(id)