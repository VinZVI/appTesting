from flask import Blueprint, request
from flask import render_template, flash, redirect, url_for
from flask_login import current_user

from crmapp.db import db
from crmapp.exceptions import DBSaveException, DataBaseSaveError
from crmapp.hookahs.forms import HookahForm, HookahDeleteForm
from crmapp.tables.forms import TableForm
from crmapp.hookahs.models import Hookah
from crmapp.tables.models import Table
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
        new_bar = Hookah.query.filter_by(name_hookah=form.name_hookah.data).first()
        for table_number in range(1, form.count_tables.data+1):
            new_table = Table(
                table_number=table_number,
                hookah_id=new_bar.id
            )
            db.session.add(new_table)
        try:
            db.session.commit()
        except DBSaveException as e:
            print(e)
            db.session.rollback()
            raise DataBaseSaveError(e)
        flash(f'Вы успешно добавили кальянную {form.name_hookah.data} \
с {form.count_tables.data} столами')
        return redirect(url_for('hookahs.bars'))
    flash(f'Название {form.name_hookah.data} \
кальянной уже существует, введите другое название')
    return redirect(url_for('hookahs.bars'))


@blueprint.route('/<name_hookah>')
@manager_required
def bar_edit(name_hookah):
    bar = Hookah.query.filter_by(name_hookah=name_hookah).first()
    form = TableForm(hookah_id=bar.id)
    title = name_hookah
    tables_list = bar.tables.all()
    worker_days = bar.worker_days.all()
    return render_template(
        "hookahs/bar_edit.html",
        title=title,
        tables_list=tables_list,
        worker_days=worker_days,
        bar=bar,
        form=form
    )


@blueprint.route('/bar_delete/<name_hookah>', methods=['GET', 'POST'])
@manager_required
def bar_delete(name_hookah):
    title = 'Delete hookah'
    form = HookahDeleteForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        user = current_user._get_current_object()
        if form.name_hookah.data == name_hookah and user.check_password(form.login_password.data):
            bar = Hookah.query.filter_by(name_hookah=form.name_hookah.data).first()
            db.session.delete(bar)
            try:
                db.session.commit()
            except DBSaveException as e:
                print(e)
                db.session.rollback()
                raise DataBaseSaveError(e)
            flash(f'Вы удалили кальянную {name_hookah}')
            return redirect(url_for('hookahs.bars'))
        flash(f'Не верно введены данные "Название кальянной" или "Password"')
    return render_template(
        "hookahs/bar_delete.html",
        title=title,
        name_hookah=name_hookah,
        form=form
    )


