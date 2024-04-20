from flask import Flask
from .views.views import blog
from .exts import init_exts
from .views.views_admin import admin
import os

app = Flask(__name__)


def create_app():
    # create flask app
    app = Flask(__name__)

    # register blueprint
    app.register_blueprint(blueprint=blog)  # blog front page
    app.register_blueprint(blueprint=admin)  # blog admin page

    # get the absolute path of the current file
    basedir = os.path.abspath(os.path.dirname(__file__))
    # set the database path
    db_uri = 'sqlite:///' + os.path.join(basedir, 'sqldb.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # init extensions
    init_exts(app=app)

    return app
