from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask.ext.moment import Moment
from datetime import datetime
from flask_debugtoolbar import DebugToolbarExtension

import os

db = SQLAlchemy()


# Configure authentication
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "auth.login"

basedir = os.path.abspath(os.path.dirname(__file__))
toolbar = DebugToolbarExtension()
# for displaying timestamps
moment = Moment()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '~t\x86\xc9\x1ew\x8bOcX\x85O\xb6\xa2\x11kL\xd1\xce\x7f\x14<y\x9e'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db', 'realtime_er.db')
    app.config['DEBUG'] = True
    db.init_app(app)
    login_manager.init_app(app)
    moment.init_app(app)
    # toolbar.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/')

    return app
