from flask_restx import fields
from .extensions import api

### ARTICLES ###

article_model = api.model("Article", {
    "id": fields.Integer,
    "title": fields.String,
    "content": fields.String
})

article_model_id = api.model("Article", {
    "id": fields.Integer,
})

article_input_model = api.model("ArticleInput", {
    "title": fields.String,
    "content": fields.String
})

### COMMENTS ###

comment_model = api.model("Comment", {
    "id": fields.Integer,
    "content": fields.String,
    "article_id": fields.Integer,
})

comment_model_id = api.model("Comment", {
    "id": fields.Integer,
})

comment_create_model = api.model("Comment", {
    "article_id": fields.Integer,
    "content": fields.String,
})

comment_create_model_edit = api.model("Comment", {
    "content": fields.String,
})
