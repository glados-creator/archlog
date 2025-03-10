from flask_restx import Resource , Namespace , abort
from .models import *
from .api_models import *

# creation du namespace , racine de tous les endpoints
ns = Namespace("api")

# definition d’une route


@ns.route("/hello")
class Hello(Resource):
    def get(self):
        return {"hello": "restx"}


@ns.route("/articles")
class ArticleCollection(Resource):
    @ns.marshal_list_with(article_model)
    def get(self):
        return get_all_articles()

    @ns.expect(article_input_model)
    @ns.marshal_with(article_model)
    def post(self):
        article = create_article(
            title=ns.payload["title"], content=ns.payload["content"])
        return article, 201

@ns.route("/comment")
class commentCollection(Resource):
    @ns.expect(comment_input_model)
    @ns.marshal_with(comment_model)
    def post(self):
        comment = create_comment(
            title=ns.payload["title"], content=ns.payload["content"])
        return comment, 201

@ns.route("/articles/<int:id>")
@ns.response(404, "Article not found")
class ArticleItem(Resource):
    @ns.marshal_with(article_model)
    def get(self, id):
        article = get_article(id)
        if article is None:
            abort(404, "Article not found")
        return article
    
    @ns.expect(article_input_model)
    @ns.marshal_with(article_model)
    def put(self ,id ):
        article = modify_article(id ,ns.payload["title"] ,ns.payload["content"])
        if article is None:
            abort (404,"Article not found")
        return article , 200

@ns.route("/comment/<int:id>")
@ns.response(404, "Comment not found")
class CommentItem(Resource):
    @ns.marshal_with(comment_model)
    def get(self, id):
        comment = get_comment(id)
        if comment is None:
            abort(404, "Comment not found")
        return comment
    
    @ns.expect(comment_input_model)
    @ns.marshal_with(comment_model)
    def put(self ,id ):
        comment = modify_comment(id ,ns.payload["title"] ,ns.payload["content"])
        if comment is None:
            abort (404,"Comment not found")
        return comment , 200
