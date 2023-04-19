from flask import Flask
from crmapp.user.views import blueprint as user_blueprint
from crmapp.admin.views import blueprint as admin_blueprint
from crmapp.hookahs.views import blueprint as hookahs_blueprint
from crmapp.main.views import blueprint as main_blueprint
from crmapp.tables.views import blueprint as tables_blueprint
from crmapp.dashboards.views import blueprint as dashboards_blueprint


def init_blueprints(app: Flask) -> None:
    app.register_blueprint(user_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(hookahs_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(tables_blueprint)
    app.register_blueprint(dashboards_blueprint)
