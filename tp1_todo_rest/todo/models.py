import time
from sqlalchemy import Column, Float, Integer, Text, Date, Boolean
from sqlalchemy.orm import relationship 
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy import func
from .app import  db, app

tasks = [
    {
        "id": 1,
        "title": "Courses",
        "description": "Salade , Oignons , Pommes , Clementines",
        "done": True
    },
    {
        "id": 2,
        "title": "Apprendre REST",
        "description": "Apprendre mon cours et comprendre les exemples ",
        "done": False
    },
    {
        "id": 3,
        "title": "Apprendre Ajax",
        "description": "Revoir les exemples et ecrire un client REST JS avecAjax",
        "done": False
    }
]

class Questionnaire (db.Model ):
    id = db.Column(db.Integer , primary_key = True)
    name = db.Column (db.String (100) )
    def __init__ (self , name):
        self.name = name
    def __repr__ (self):
        return "<Questionnaire (%d) %s>" % (self.id , self.name)
    def to_json (self):
        return {
            "id":self.id,
            "name":self.name
            }

class Question (db.Model ):
    id = db.Column (db.Integer , primary_key = True)
    title = db.Column (db.String (120) )
    ### questionType = db.Column (db.String (120) )
    ### questionnaire_id = db.Column (db.Integer , db.ForeignKey ("questionnaire.id"))
    questionnaire = db. relationship ("Questionnaire", backref = db. backref (
    "questions", lazy="dynamic"))
    ### reponses = db. relationship ("Reponse", backref = db. backref (
    ### "question", lazy="dynamic"))
    reponse = db.Column (db.String (120) )

### class Reponse (db.Model ):
###     id = db.Column (db.Integer , primary_key = True)
###     question = db. relationship ("Question", backref = db. backref (
###     "reponses", lazy="dynamic"))

def get_all():
    return Question.query.all()

def get_max_id(table):
    max_id = db.session.query(func.max(table.id)).scalar()
    next_id = (max_id or 0) + 1
    return next_id

def add_question(title : str):
    next_id = get_max_id(Question)
    q = Question(next_id,title)
    db.session.add(q)

def add_questionnaire(title : str):
    next_id = get_max_id(Questionnaire)
    q = Questionnaire(next_id,title)
    db.session.add(q)

### def add_reponse(user):
###     next_id = get_max_id(Reponse)
###     q = Questionnaire(next_id,user)
###     db.session.add(q)

add_questionnaire("questionnaire")
add_question("question")