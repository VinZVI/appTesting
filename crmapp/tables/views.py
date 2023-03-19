from flask import render_template
from flask_login import login_required
# from crmapp.tables.models import Tables
from flask import Blueprint

blueprint = Blueprint('tables', __name__)


@blueprint.route("/dashboard")
@login_required
def index():
    title = "Dashboard"
    # weather = weather_by_city(current_app.config['WEATHER_DEFAULT_CITY'])
    # news_list = News.query.order_by(News.published.desc()).all()
    return render_template("tables/index.html", title=title)
