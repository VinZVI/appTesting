from flask import Blueprint, request
from flask import render_template, flash, redirect, url_for
from flask_login import current_user

from crmapp.db import db
from crmapp.exceptions import DBSaveException, DataBaseSaveError
from crmapp.tables.forms import TableForm, TableDeleteForm
from crmapp.hookahs.models import Hookah
from crmapp.tables.models import Table
from crmapp.user.decorators import manager_required

blueprint = Blueprint('tables', __name__, '/tables')


@blueprint.route("/add_table", methods=['POST'])
@manager_required
def add_table():
    form = TableForm(request.form)
    bar = Hookah.query.get_or_404(form.hookah_id.data)
    if form.validate_on_submit():
        new_table = Table(
            table_number=form.table_number.data,
            description=form.description.data,
            total_of_persons=form.total_of_persons.data,
            hookah_id=form.hookah_id.data
        )
        db.session.add(new_table)
        try:
            db.session.commit()
        except DBSaveException as e:
            print(e)
            db.session.rollback()
            raise DataBaseSaveError(e)
        flash(f'Вы успешно добавили стол {form.table_number.data}')
        return redirect(url_for('hookahs.bar_edit', name_hookah=bar.name_hookah))
    flash(f'Название {form.table_number.data} \
стола уже существует, введите другое название')
    return redirect(url_for('hookahs.bar_edit', name_hookah=bar.name_hookah))


@blueprint.route('/<table_number>')
@manager_required
def table_edit(table_number):
    pass
    # form = TableForm()
    # title = name_hookah
    # bar = Hookah.query.filter_by(name_hookah=name_hookah).first()
    # tables_list = bar.tables.all()
    # worker_days = bar.worker_days.all()
    # return render_template(
    #     "hookahs/bar_edit.html",
    #     title=title,
    #     tables_list=tables_list,
    #     worker_days=worker_days,
    #     form=form
    # )


@blueprint.route('/table_delete/<name_hookah>/<table_number>', methods=['GET', 'POST'])
@manager_required
def table_delete(table_number, name_hookah):
    title = 'Delete table'
    form = TableDeleteForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        user = current_user._get_current_object()
        if form.table_number.data == table_number and user.check_password(form.login_password.data):
            table = Table.query.filter_by(table_number=form.table_number.data).first()
            db.session.delete(table)
            try:
                db.session.commit()
            except DBSaveException as e:
                print(e)
                db.session.rollback()
                raise DataBaseSaveError(e)
            flash(f'Вы удалили стол {table_number}')
            return redirect((url_for('hookahs.bar_edit', name_hookah=name_hookah)))
        flash(f'Не верно введены данные "Название стола" или "Password"')
    return render_template(
        "tables/table_delete.html",
        title=title,
        table_number=table_number,
        form=form,
        name_hookah=name_hookah
    )