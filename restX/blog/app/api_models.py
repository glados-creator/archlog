from flask_restx import fields
from .extensions import api

### ARTICLES ###

article_model = api.model("Article", {
    "id": fields.Integer(required=True),
    "title": fields.String(required=True),
    "content": fields.String(required=True)
})

article_model_id = api.model("Article", {
    "id": fields.Integer(required=True),
})

article_input_model = api.model("ArticleInput", {
    "title": fields.String(required=True),
    "content": fields.String(required=True)
})

### COMMENTS ###

comment_model = api.model("Comment", {
    "id": fields.Integer(required=True),
    "content": fields.String(required=True),
    "article_id": fields.Integer(required=True),
})

comment_model_id = api.model("Comment", {
    "id": fields.Integer(required=True),
})

comment_create_model = api.model("Comment", {
    "article_id": fields.Integer(required=True),
    "content": fields.String(required=True),
})

comment_create_model_edit = api.model("Comment", {
    "content": fields.String(required=True),
})
