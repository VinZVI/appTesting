import os.path

from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate

from crmapp.db import db
from crmapp.user.forms import LoginForm
from crmapp.user.models import User
from crmapp.blueprints import init_blueprints


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    migrate = Migrate(app, db)

    if os.path.isfile('crmapp.db'):
        with app.app_context():
            db.create_all()

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'user.login'

    init_blueprints(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    return app
