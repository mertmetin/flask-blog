from flask import Flask
from flask.ext.mongoengine import MongoEngine
from flask.ext.admin import Admin


app = Flask(__name__)
app.config.from_object('config.Configuration')


from models import db, Post, Comment
db.init_app(app)


def register_blueprints(app):
    # Prevents circular imports
    from views import posts
    app.register_blueprint(posts)


register_blueprints(app)


if __name__ == "__main__":
    app.run(debug = True)
