from flask import Blueprint, request
from flask import render_template, flash, redirect, url_for
from flask_login import current_user
from datetime import datetime, time, timedelta
import calendar

from crmapp.db import db
from crmapp.exceptions import DBSaveException, DataBaseSaveError
from crmapp.hookahs.forms import HookahForm, HookahDeleteForm, WorkingDayForm
from crmapp.tables.forms import TableForm
from crmapp.hookahs.models import Hookah, WorkerDay, WeekDayEnum
from crmapp.tables.models import Table, DateTimeBooked
from crmapp.user.decorators import manager_required

blueprint = Blueprint('dashboards', __name__, '/dashboard')

def get_day_week_today(today: datetime.utcnow()) -> WeekDayEnum:
    for day in WeekDayEnum:
        if day.value[2] == today.date().isoweekday():
            return day


@blueprint.route('/dashboard/<name_hookah>')
def bar_dashboard(name_hookah):
    bar = Hookah.query.filter_by(name_hookah=name_hookah).first()
    title = name_hookah
    today = datetime.utcnow()
    month = calendar.month_name[today.month]
    weekday = get_day_week_today(today)
    working_day = bar.worker_days.filter_by(week_day=weekday).first()
    time_panel_list = working_day.get_time_panel_list
    tables_list = bar.tables.all()
    tables_booked_list = []
    for table in tables_list:
        table_booking = table.booked.filter(DateTimeBooked.start_date_time_brooke == today.date()).all()
        tables_booked_list.append((table, table_booking))
    return render_template(
        "dashboards/bar_dashboard.html",
        title=title,
        tables_booked_list=tables_booked_list,
        time_panel_list=time_panel_list,
        today=today,
        month=month
    )


# @blueprint.route("/add_bar", methods=['POST'])
# @manager_required
# def add_bar():
#     form = HookahForm(request.form)
#     if form.validate_on_submit():
#         user = current_user._get_current_object()
#         new_bar = Hookah(
#             name_hookah=form.name_hookah.data,
#             user_id=user.id
#         )
#         db.session.add(new_bar)
#         try:
#             db.session.commit()
#         except DBSaveException as e:
#             print(e)
#             db.session.rollback()
#             raise DataBaseSaveError(e)
#         new_bar = Hookah.query.filter_by(name_hookah=form.name_hookah.data).first()
#         working_day_list = new_bar.set_worker_days()
#         for day in working_day_list:
#             db.session.add(day)
#         for table_number in range(1, form.count_tables.data+1):
#             new_table = Table(
#                 table_number=table_number,
#                 hookah_id=new_bar.id
#             )
#             db.session.add(new_table)
#         try:
#             db.session.commit()
#         except DBSaveException as e:
#             print(e)
#             db.session.rollback()
#             raise DataBaseSaveError(e)
#         flash(f'Вы успешно добавили кальянную {form.name_hookah.data} \
# с {form.count_tables.data} столами')
#         return redirect(url_for('hookahs.bars'))
#     flash(f'Название {form.name_hookah.data} \
# кальянной уже существует, введите другое название')
#     return redirect(url_for('hookahs.bars'))
#
#
# @blueprint.route('/bar_delete/<name_hookah>', methods=['GET', 'POST'])
# @manager_required
# def bar_delete(name_hookah):
#     title = 'Delete hookah'
#     form = HookahDeleteForm(request.form)
#     if request.method == 'POST' and form.validate_on_submit():
#         user = current_user._get_current_object()
#         if form.name_hookah.data == name_hookah and user.check_password(form.login_password.data):
#             bar = Hookah.query.filter_by(name_hookah=form.name_hookah.data).first()
#             db.session.delete(bar)
#             try:
#                 db.session.commit()
#             except DBSaveException as e:
#                 print(e)
#                 db.session.rollback()
#                 raise DataBaseSaveError(e)
#             flash(f'Вы удалили кальянную {name_hookah}')
#             return redirect(url_for('hookahs.bars'))
#         flash(f'Не верно введены данные "Название кальянной" или "Password"')
#     return render_template(
#         "hookahs/bar_delete.html",
#         title=title,
#         name_hookah=name_hookah,
#         form=form
#     )
#
# @blueprint.route('/<name_hookah>/working_day/<working_day_id>', methods=['GET', 'POST'])
# @manager_required
# def working_day_edit(name_hookah, working_day_id):
#     bar = Hookah.query.filter_by(name_hookah=name_hookah).first()
#     table_form = TableForm(hookah_id=bar.id)
#     title = name_hookah
#     tables_list = bar.tables.all()
#     worker_days = bar.worker_days.all()
#     working_day = WorkerDay.query.get_or_404(working_day_id)
#     week_day = working_day.week_day
#     worker_days_form = WorkingDayForm(obj=working_day)
#     if request.method == 'POST' and worker_days_form.validate_on_submit():
#         worker_days_form.populate_obj(working_day)
#         working_day.week_day = week_day
#         db.session.add(working_day)
#         try:
#             db.session.commit()
#         except DBSaveException as e:
#             print(e)
#             db.session.rollback()
#             raise DataBaseSaveError(e)
#         flash(f'Вы успешно внесли изменения в расписание рабочего дня {working_day.week_day.value}')
#         return redirect(url_for('hookahs.bar_edit', name_hookah=name_hookah))
#
#     return render_template(
#         "hookahs/bar_edit.html",
#         title=title,
#         tables_list=tables_list,
#         worker_days=worker_days,
#         bar=bar,
#         worker_days_form=worker_days_form,
#         table_form=table_form
#     )


