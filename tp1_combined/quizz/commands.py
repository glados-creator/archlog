from .models import *
import yaml
import click
from .app import app, db
from hashlib import sha256


@app.cli.command()
def loaddb():
    """Creates the tables and populates them with data."""
    # création de toutes les tables
    db.create_all()

    tmp = mcreate_task("Courses","Salade , Oignons , Pommes , Clementines")
    tmp.done = True
    db.session.commit()

    mcreate_task("Apprendre REST","Apprendre mon cours et comprendre les exemples")
    mcreate_task("Apprendre Ajax","Revoir les exemples et ecrire un client REST JS avecAjax")

    # add default user
    m = sha256()
    m.update(str("passwd").encode())
    u = User(U_username="admin", U_password=m.hexdigest())
    db.session.add(u)
    db.session.commit()

    # add default
    q = madd_questionnaire("questionnaire_test")
    qu = madd_question(q,"question_test","123")
    madd_reponse(qu,u,"test_test_test")

    q = madd_questionnaire("questionnairedos_test")
    qu = madd_question(q,"questiondos_test","123")

    db.session.commit()
    print("db created success")


@app.cli.command()
def syncdb():
    """Creates all missing tables."""
    db.create_all()

@app.cli.command()
@click.argument('username')
@click.argument('password')
def newuser(username, password):
    """Adds a new user."""
    m = sha256()
    m.update(password.encode())
    u = User(U_username=username, U_password=m.hexdigest())
    db.session.add(u)
    db.session.commit()


@app.cli.command()
@click.argument('username')
@click.argument('password')
def passwd(username, password):
    """change a user passwd."""
    from .models import User
    from hashlib import sha256
    m = sha256()
    m.update(password.encode())
    x = User.query.get(username)
    x.password = m.hexdigest()
    db.session.commit()
