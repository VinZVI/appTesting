from flask import render_template, current_app

# from crmapp.tables.models import Tables
from flask import Blueprint

blueprint = Blueprint('news', __name__)


@blueprint.route("/")
def index():
    title = "CRM-HookahBars"
    # weather = weather_by_city(current_app.config['WEATHER_DEFAULT_CITY'])
    # news_list = News.query.order_by(News.published.desc()).all()
    return render_template("tables/index.html", title=title)
