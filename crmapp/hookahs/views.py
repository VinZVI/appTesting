from flask import Blueprint, request
from flask import render_template, flash, redirect, url_for
from flask_login import current_user

from crmapp.db import db
from crmapp.exceptions import DBSaveException, DataBaseSaveError
from crmapp.hookahs.forms import HookahForm
from crmapp.hookahs.models import Hookah
from crmapp.user.decorators import manager_required

blueprint = Blueprint('hookahs', __name__, '/hookahs')


@blueprint.route("/")
@manager_required
def bars():
    title = "Hookah bars"
    user = current_user._get_current_object()
    hookahs_list = user.hookahs.all()
    form = HookahForm()
    return render_template(
        "hookahs/bars.html",
        title=title,
        hookahs_list=hookahs_list,
        form=form
    )


@blueprint.route("/add_bar", methods=['POST'])
@manager_required
def add_bar():
    form = HookahForm(request.form)
    if form.validate_on_submit():
        user = current_user._get_current_object()
        new_bar = Hookah(
            name_hookah=form.name_hookah.data,
            user_id=user.id
        )
        db.session.add(new_bar)
        try:
            db.session.commit()
        except DBSaveException as e:
            print(e)
            db.session.rollback()
            raise DataBaseSaveError(e)
        flash(f'Вы успешно добавили кальянную {form.name_hookah.data}')
        return redirect(url_for('hookahs.bars'))
    flash(f'Название {form.name_hookah.data}\
кальянной уже существует, введите другое название')
    return redirect(url_for('hookahs.bars'))


@blueprint.route('/<name_hookah>')
@manager_required
def bar_edit(name_hookah):
    title = name_hookah
    bar = Hookah.query.filter_by(name_hookah='Hookah1').first()
    tables_list = bar.tables.all()
    worker_days = bar.worker_days.all()
    return render_template(
        "hookahs/bars.html",
        title=title,
        hookahs_list=tables_list,
        worker_days=worker_days
    )
