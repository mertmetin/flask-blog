import datetime
from wtforms import form, fields, validators
from flask.ext.mongoengine import MongoEngine

db = MongoEngine()


class User(db.Document):
    username = db.StringField(unique = True, required = True, max_length=40)
    password = db.StringField(max_length=40)




class Post(db.Document):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    author = db.ReferenceField(User)
    title = db.StringField(max_length=255, required=True)
    slug = db.StringField(max_length=255, required=True)
    body = db.StringField(required=True)
    comments = db.ListField(db.EmbeddedDocumentField('Comment'))

    meta = {
        'ordering': ['-created_at']
    }


class Comment(db.EmbeddedDocument):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    body = db.StringField(verbose_name="Comment", required=True)
    author = db.StringField(verbose_name="Name", max_length=255, required=True)
