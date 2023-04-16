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


@blueprint.route('/add_table', methods=['POST'])
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


@blueprint.route('/edit/<table_id>', methods=['GET', 'POST'])
@manager_required
def table_edit(table_id):
    table = Table.query.get_or_404(table_id)
    title = table.table_number
    form = TableForm(obj=table)
    if request.method == 'POST' and form.validate_on_submit():
        form.populate_obj(table)
        db.session.add(table)
        try:
            db.session.commit()
        except DBSaveException as e:
            print(e)
            db.session.rollback()
            raise DataBaseSaveError(e)
        flash(f'Вы изменили данные стола {form.table_number.data}')
        return redirect((url_for('tables.table_edit', table_id=table.id)))
    bar = Hookah.query.filter_by(id=table.hookah_id).first()
    return render_template(
        'tables/table_edit.html',
        title=title,
        table=table,
        form=form,
        bar=bar
    )


@blueprint.route('/table_delete/<name_hookah>/<table_id>', methods=['GET', 'POST'])
@manager_required
def table_delete(table_id, name_hookah):
    title = 'Delete table'
    table = Table.query.get_or_404(table_id)
    form = TableDeleteForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = current_user._get_current_object()
        if form.table_number.data == table.table_number and user.check_password(form.login_password.data):
            db.session.delete(table)
            try:
                db.session.commit()
            except DBSaveException as e:
                print(e)
                db.session.rollback()
                raise DataBaseSaveError(e)
            flash(f'Вы удалили стол {table.table_number}')
            return redirect(url_for('hookahs.bar_edit', name_hookah=name_hookah))
        flash(f'Не верно введены данные "Название стола" или "Password"')
    return render_template(
        'tables/table_delete.html',
        title=title,
        table=table,
        form=form,
        name_hookah=name_hookah
    )
