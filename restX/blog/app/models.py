from .extensions import db
class Article(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    title = db.Column(db.String (50))
    content = db.Column(db.String (500))
    comments = db.relationship("Comment", back_populates="article")

class Comment(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    content = db.Column(db.String (100))
    article_id = db.Column(db.ForeignKey("article.id"))
    article = db.relationship("Article",back_populates="comments")

def get_all_articles ():
    return Article.query.all()

def create_article(title ,content):
    article = Article(title=title , content=content)
    db.session.add(article)
    db.session.commit ()
    return article

def get_article(id : int):
    return Article.query.get(id)

def get_comment(id : int):
    return Comment.query.get(id)

def modify_article(id ,title ,content):
    article = Article.query.get(id)
    if article is None:
        return None
    article.title = title
    article.content = content
    db.session.commit ()
    return article

def modify_comment(id ,title ,content):
    article = Article.query.get(id)
    if article is None:
        return None
    article.title = title
    article.content = content
    db.session.commit ()
