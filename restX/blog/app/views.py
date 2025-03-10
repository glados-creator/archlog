from flask_restx import Resource, Namespace, abort
from .models import *
from .api_models import *

# creation du namespace , racine de tous les endpoints
ns = Namespace("api/v1.0.0")

# definition d’une route


@ns.route("/hello")
class Hello(Resource):
    def get(self):
        return {"hello": "restx"}


@ns.route("/articles")
class ArticleCollection(Resource):
    @ns.marshal_list_with(article_model_id)
    def get(self):
        return Article.get_all_articles()

    @ns.expect(article_input_model)
    @ns.marshal_with(article_model_id)
    def post(self):
        return Article.create_article(title=ns.payload["title"], content=ns.payload["content"]), 201


@ns.route("/comments")
@ns.response(404, "Article not found")
class commentCollection(Resource):
    @ns.expect(comment_create_model)
    @ns.marshal_with(comment_model_id)
    def post(self):
        comment = Comment.create_comment(article_id=ns.payload["article_id"], content=ns.payload["content"])
        if comment is None:
            abort(404, "Article not found")
        return comment, 201


@ns.route("/articles/<int:id>")
@ns.response(404, "Article not found")
class ArticleItem(Resource):
    @ns.marshal_with(article_model)
    def get(self, id):
        article = Article.get_article(id)
        if article is None:
            abort(404, "Article not found")
        return article

    @ns.expect(article_input_model)
    @ns.marshal_with(article_model)
    def put(self, id):
        article = Article.modify_article(
            id, ns.payload["title"], ns.payload["content"])
        if article is None:
            abort(404, "Article not found")
        return article, 200

    @ns.marshal_with(article_model)
    def delete(self, id):
        article = Article.delete_article(id)
        if article is None:
            abort(404, "Article not found")
        return article , 204


@ns.route("/article/<int:id>/comments")
@ns.response(404, "Article not found")
class ArticleItem_dos(Resource):
    @ns.marshal_list_with(comment_model_id)
    def get(self, id):
        comment_article = Article.get_comments(id)
        if comment_article is None:
            abort(404, "Article not found")
        return comment_article


@ns.route("/comment/<int:id>")
@ns.response(404, "Comment not found")
class CommentItem(Resource):
    @ns.marshal_with(comment_model)
    def get(self, id):
        comment = Comment.get_comment(id)
        if comment is None:
            abort(404, "Comment not found")
        return comment

    @ns.expect(comment_create_model_edit)
    @ns.marshal_with(comment_model_id)
    def put(self, id):
        comment = Comment.modify_comment(
            id, ns.payload["title"], ns.payload["content"])
        if comment is None:
            abort(404, "Comment not found")
        return comment, 200
    
    @ns.marshal_with(comment_model)
    def delete(self, id):
        comment = Comment.delete_comment(id)
        if comment is None:
            abort(404, "Comment not found")
        return comment , 204
