import time
from sqlalchemy import Column, Float, Integer, Text, Date, Boolean
from sqlalchemy.orm import relationship 
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy import func
from .app import  db, app, login_manager
from flask_login import UserMixin

### questionnaire

asso_questionaires = db.Table('asso_questionaires',
                db.Column('user_id', db.Integer,
                          db.ForeignKey('user.id')),
                db.Column('questionnaire_id', db.Integer,
                          db.ForeignKey('questionnaire.id'))
                )

asso_questions = db.Table('asso_questions',
                db.Column('user_id', db.Integer,
                          db.ForeignKey('user.id')),
                db.Column('question_id', db.Integer,
                          db.ForeignKey('question.id'))
                )
    
class Questionnaire (db.Model ):
    id = db.Column(db.Integer , primary_key = True)
    name = db.Column (db.String (100) )

    questions = db.relationship ("Question", backref = db.backref (
    "questionnaire", lazy="dynamic"))

    def __init__ (self , name):
        self.name = name
    def __repr__ (self):
        return self.to_json()
        ### return "<Questionnaire (%d) %s>" % (self.id , self.name)
    def to_json (self):
        return {
            "id":self.id,
            "name":self.name,
            "questions": list(self.questions.query(Question.id).all())
            }

class Question (db.Model ):
    id = db.Column (db.Integer , primary_key = True)
    title = db.Column (db.String (120) )
    reponse = db.Column (db.String(120))
    ### questionType = db.Column (db.String (120) )
    ### questionnaire_id = db.Column (db.Integer , db.ForeignKey ("questionnaire.id"))
    questionnaire = db.relationship ("Questionnaire", backref = db.backref (
    "questions", lazy="dynamic"))

class Reponse (db.Model ):
    id = db.Column (db.Integer , primary_key = True)
    question = db.relationship ("Question", backref = db.backref ("reponses", lazy="dynamic"))
    user = db.relationship ("User", backref = db.backref ("reponses", lazy="dynamic"))
    reponse = db.Column (db.String(120))

class User(db.Model , UserMixin):
    U_username = db.Column(db.String(50), primary_key=True)
    U_password = db.Column(db.String(64))

    def get_id(self):
        return self.U_username
    
    questionnaires = db.relationship('Questionnaire',
                                secondary=asso_questionaires,
                                lazy='subquery',
                                backref=db.backref('answered_by', lazy=True))

    questions = db.relationship('Question', 
                                secondary=asso_questions,
                                lazy='subquery',
                                backref=db.backref('answered_by', lazy=True))

    reponses = db.relationship ("Reponse", backref = db.backref ("user", lazy="dynamic"))

def mget_max_id(table):
    max_id = db.session.query(func.max(table.id)).scalar()
    next_id = (max_id or 0) + 1
    return next_id

def mget_questionnaires():
    return list(Questionnaire.query(Questionnaire.id,Questionnaire.name).all())

def mget_questionnaire(id):
    return Questionnaire.get_or_404(id)

def mget_question(id):
    return Question.get_or_404(id)

def mget_reponse(id):
    return Reponse.get_or_404(id)

def muget_questionnaire(user):
    return user.questionnaires

def muget_question(user,questionnaire_id : int):
    return user.questionnaires.query(questionnaire_id).questions

def muget_reponse(user):
    # TODO : here
    return Reponse.get_or_404(id)

def madd_questionnaire(title : str) -> Questionnaire:
    q = Questionnaire(title)
    db.session.add(q)
    return q

def madd_question(questionnaire : Questionnaire,title : str,reponse : str) -> Question:
    q = Question(title = title , questionnaire = questionnaire , reponse=reponse)
    db.session.add(q)


def madd_reponse(question : Question,user : User,reponse : str ):
    q = Reponse(question=question
                ,user=user
                ,reponse=reponse)
    db.session.add(q)

def mget_user(id):
    return User.query.get(0)
    ### return User.query.get(user_id)