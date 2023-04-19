from enum import Enum
from datetime import datetime as DT, time, date, timedelta
from itertools import product

from crmapp.db import db
from crmapp.time_fuctions import round_dt_to_delta
from flask import current_app


class Hookah(db.Model):
    __tablename__ = 'hookahs'
    id = db.Column(db.Integer, primary_key=True)
    name_hookah = db.Column(db.String, unique=True, nullable=False)

    tables = db.relationship(
        'Table',
        backref='hookah',
        lazy='dynamic'
    )

    worker_days = db.relationship(
        'WorkerDay',
        backref='hookah',
        lazy='dynamic'
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        index=True
    )

    def __repr__(self) -> str:  # метод для отображения объекта
        return '<Hookah {}: user {}>'.format(self.name_hookah, self.user_id)

    def set_worker_days(self) -> list[object]:
        working_day_list = []
        for weekdayEnum in WeekDayEnum:
            working_day = WorkerDay(
                week_day=weekdayEnum,
                startWD_time=time(12, 00, 00),
                finishWD_time=time(00, 00, 00),
                period_time_panel=current_app.config['DELTA_TIME_ROUND'],
                hookah_id=self.id
            )
            working_day_list.append(working_day)
        return working_day_list


class WeekDayEnum(Enum):
    MONDAY = ("Monday", "mon", 1)
    TUESDAY = ("Tuesday", "tue", 2)
    WEDNESDAY = ("Wednesday", "wed", 3)
    THURSDAY = ("Thursday", "thu", 4)
    FRIDAY = ("Friday", "fri", 5)
    SATURDAY = ("Saturday", "sat", 6)
    SUNDAY = ("Sunday", "sun", 7)


class WorkerDay(db.Model):
    __tablename__: str = "worker_days_table"
    id = db.Column(db.Integer, primary_key=True)
    week_day = db.Column(db.Enum(WeekDayEnum), nullable=False)
    startWD_time = db.Column(db.Time, nullable=False)
    finishWD_time = db.Column(db.Time, nullable=False)
    period_time_panel = db.Column(
        db.Time,
        nullable=False
    )

    hookah_id = db.Column(
        db.Integer,
        db.ForeignKey(
            'hookahs.id',
            ondelete='CASCADE'
        ))

    def __repr__(self):
        return f'<Day of week {self.day_of_week}>'

    def get_time_is_rounded(self, time_count: time, period_time_panel: time) -> time:
        period_time_panel = timedelta(minutes=period_time_panel)
        return round_dt_to_delta(time_count, period_time_panel)

    @property
    def get_time_panel_list(self) -> list[time]:
        period = self.period_time_panel.minute
        start_h = self.startWD_time.hour
        end_h = self.finishWD_time.hour
        time_panel_list = []
        if start_h > end_h:
            for i in range(start_h * 60, 24 * 60, period):
                time_period = (DT.combine(date.today(), time(0, 0)) + timedelta(minutes=i)).time().strftime("%H:%M")
                time_panel_list.append(time_period)
            for i in range(0, end_h * 60, period):
                time_period = (DT.combine(date.today(), time(0, 0)) + timedelta(minutes=i)).time().strftime("%H:%M")
                time_panel_list.append(time_period)
        else:
            for i in range(start_h * 60, end_h * 60, period):
                time_period = (DT.combine(date.today(), time(0, 0)) + timedelta(minutes=i)).time().strftime("%H:%M")
                time_panel_list.append(time_period)
            # time_panel_list = [(DT.combine(date.today(), time(0, 0)) + timedelta(minutes=i)).time().strftime("%H:%M") for i in range(start_h*60, end_h*60, period)]
        return time_panel_list


