from flask import Blueprint, request
from flask import render_template, flash, redirect, url_for
from flask_login import current_user
from datetime import datetime, date, time, timedelta
import calendar

from crmapp.db import db
from crmapp.exceptions import DBSaveException, DataBaseSaveError
from crmapp.hookahs.forms import HookahForm, HookahDeleteForm, WorkingDayForm
from crmapp.dashboards.forms import BookingForm
from crmapp.hookahs.models import Hookah, WeekDayEnum
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
    time_panel_list: list[tuple[str, str]] = working_day.get_time_panel_list
    tables_list = bar.tables.all()

    booking_form = BookingForm()
    new_time_panel_list = []
    for table in tables_list:
        table_booking = table.booked.filter(DateTimeBooked.start_date_time_brooke >= today.date()).all()

        for time_period in time_panel_list:
            l = len(time_period)
            for booking_item in table_booking:
                if time_period[0] == booking_item.start_date_time_brooke.time().strftime("%H:%M"):
                    time_period.append(booking_item)
                    break
            if len(time_period) == l:
                time_period.append((table.id, None))

    return render_template(
        "dashboards/bar_dashboard.html",
        title=title,
        tables_list=tables_list,
        time_panel_list=time_panel_list,
        today=today,
        month=month,
        booking_form=booking_form
    )


@blueprint.route("/dashboard/<name_hookah>/booking/<table_id>", methods=['POST'])
def booking(name_hookah, table_id):
    form = BookingForm(request.form)
    if form.validate_on_submit():
        new_booking = DateTimeBooked(
            bookers_name=form.bookers_name.data,
            table_id=table_id,
            start_date_time_brooke=datetime.combine(date.today(), form.start_date_time_brooke.data),
            finish_date_time_brooke=datetime.combine(date.today(), form.finish_date_time_brooke.data)
        )
        db.session.add(new_booking)
        try:
            db.session.commit()
        except DBSaveException as e:
            print(e)
            db.session.rollback()
            raise DataBaseSaveError(e)
        flash(f'Вы успешно забронировали стол на время {form.start_date_time_brooke.data}')
        return redirect(url_for('dashboards.bar_dashboard', name_hookah=name_hookah))
    flash(f'Бронирование не удалось, попробуйте снова')
    return redirect(url_for('dashboards.bar_dashboard', name_hookah=name_hookah))


@blueprint.route('/dashboard/<name_hookah>/booking-delete/<booking_id>', methods=['DELETE'])
@manager_required
def booking_delete(name_hookah, booking_id):
    reservation = DateTimeBooked.query.get(booking_id)
    if request.method == 'DELETE' and booking is not None:
        db.session.delete(reservation)
        try:
            db.session.commit()
        except DBSaveException as e:
            print(e)
            db.session.rollback()
            raise DataBaseSaveError(e)
        flash(f'Вы удалили бронирование')
        return redirect(url_for('dashboards.bar_dashboard', name_hookah=name_hookah))
        flash(f'Такого бронирования нет, попробуйте еще раз выбрать бронирование для удаления')
    return redirect(url_for('dashboards.bar_dashboard', name_hookah=name_hookah))

