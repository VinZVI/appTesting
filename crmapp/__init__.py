from flask import Flask
from flask_login import LoginManager
from crmapp.user.forms import LoginForm
from crmapp.db import db
from crmapp.user.models import User
from crmapp.user.views import blueprint as user_blueprint
from crmapp.admin.views import blueprint as admin_blueprint
from crmapp.tables.views import blueprint as tables_blueprint


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'user.login'

    app.register_blueprint(user_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(tables_blueprint)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    return app
