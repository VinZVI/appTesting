from flask import Flask
from crmapp.user.views import blueprint as user_blueprint
from crmapp.admin.views import blueprint as admin_blueprint
from crmapp.tables.views import blueprint as tables_blueprint
from crmapp.main.views import blueprint as main_blueprint


def init_blueprints(app: Flask) -> None:
    app.register_blueprint(user_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(tables_blueprint)
    app.register_blueprint(main_blueprint)
