from .extensions import db
from .models import Article , Comment
from .myapp import app

@app.cli.command ()
def syncdb ():
    db.create_all ()
    db.session.query(Article).delete ()
    db.session.query(Comment).delete ()
    article1 = Article(title="Premier Article", content="Ceci est mon premier article")
    article2 = Article(title="Second Article", content="Ceci est mon second article")
    comment1 = Comment(content="Super article",article_id =1)
    db.session.add(article1)
    db.session.add(article2)
    db.session.add(comment1)
    db.session.commit ()