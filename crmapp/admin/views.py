
from crmapp.user.decorators import admin_required
from flask import Blueprint, render_template

blueprint = Blueprint('admin', __name__, url_prefix='/admin')


@blueprint.route("/")
@admin_required
def admin_index():
    title = "Панель администратора"
    return render_template('/admin/index.html', title=title)
