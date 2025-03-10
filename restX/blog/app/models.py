from .extensions import db


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    content = db.Column(db.String(500))
    comments = db.relationship("Comment", back_populates="article")

    @staticmethod
    def get_all_articles():
        return Article.query.all()

    @staticmethod
    def get_article(id: int):
        return Article.query.get(id)

    @staticmethod
    def create_article(title, content):
        article = Article(title=title, content=content)
        db.session.add(article)
        db.session.commit()
        return article

    @staticmethod
    def modify_article(id, title, content):
        article = Article.query.get(id)
        if article is None:
            return None
        article.title = title
        article.content = content
        db.session.commit()
        return article
    
    @staticmethod
    def delete_article(id ):
        article = Article.query.get(id )
        db.session.delete(article)
        db.session.commit ()
        return article


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100))
    article_id = db.Column(db.ForeignKey("article.id"))
    article = db.relationship("Article", back_populates="comments")

    @staticmethod
    def get_comment(id: int):
        return Comment.query.get(id)

    @staticmethod
    def create_comment(article_id, content):
        comment = Comment(article_id=article_id, content=content)
        db.session.add(comment)
        db.session.commit()
        return comment

    @staticmethod
    def modify_comment(id, content):
        comment = Comment.query.get(id)
        if comment is None:
            return None
        comment.content = content
        db.session.commit()
        return comment

    @staticmethod
    def delete_comment(id ):
        comment = Comment.query.get(id )
        db.session.delete(comment)
        db.session.commit ()
        return comment