from sqlalchemy import Column, Float, Integer, Text, Date, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy import func
from .app import db, app, login_manager
from flask_login import UserMixin

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
    return Tasks.query.all()

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


# questionnaire

# (Many-to-Many)
asso_questionnaires = db.Table(
    'asso_questionnaires',
    db.Column('user_id', db.String(50), db.ForeignKey('user.U_username')),  # Fixed type
    db.Column('questionnaire_id', db.Integer, db.ForeignKey('questionnaire.id'))
)

asso_questions = db.Table(
    'asso_questions',
    db.Column('user_id', db.String(50), db.ForeignKey('user.U_username')),  # Fixed type
    db.Column('question_id', db.Integer, db.ForeignKey('question.id'))
)

class Questionnaire(db.Model):
    __tablename__ = "questionnaire"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    questions = db.relationship("Question", backref="questionnaire", lazy="dynamic")

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return str(self.to_json()) 

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "questions": [q.id for q in self.questions]  
        }

class Question(db.Model):
    __tablename__ = "question"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    reponse = db.Column(db.String(120))
    questionnaire_id = db.Column(db.Integer, db.ForeignKey("questionnaire.id"))

class Reponse(db.Model):
    __tablename__ = "reponse"
    id = db.Column(db.Integer, primary_key=True)

    question_id = db.Column(db.Integer, db.ForeignKey("question.id"), nullable=False)
    user_id = db.Column(db.String(50), db.ForeignKey("user.U_username"), nullable=False)

    reponse = db.Column(db.String(120))

    question = db.relationship("Question", backref=db.backref("reponses", lazy="dynamic"))

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


def mget_max_id(table):
    max_id = db.session.query(func.max(table.id)).scalar()
    next_id = (max_id or 0) + 1
    return next_id


def mget_questionnaires():
    return list(Questionnaire.query.with_entities(Questionnaire.id, Questionnaire.name).all())


def mget_questionnaire(id):
    return Questionnaire.get_or_404(id)


def mget_question(id):
    return Question.get_or_404(id)


def mget_reponse(id):
    return Reponse.get_or_404(id)


def muget_questionnaire(user):
    return user.questionnaires


def muget_question(user, questionnaire_id: int):
    return user.questionnaires.query(questionnaire_id).questions


def muget_reponse(user):
    # TODO : here
    return Reponse.get_or_404(user)


def mdelete_questionnaire(questionnaire):
    db.session.delete(questionnaire)
    db.session.commit()
    return questionnaire


def mdelete_question(question):
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


def madd_reponse(question: Question, user: User, reponse: str):
    q = Reponse(question=question, user=user, reponse=reponse)
    db.session.add(q)
    db.session.commit()
    return q


def mget_user(id):
    return User.query.get(0)
    # return User.query.get(user_id)
