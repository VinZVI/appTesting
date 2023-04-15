from enum import Enum
from datetime import timedelta, time
from typing import List

from crmapp.db import db
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

    def set_worker_days(self) -> List[object]:
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
    MONDAY = "mon"
    TUESDAY = "tue"
    WEDNESDAY = "wed"
    THURSDAY = "thu"
    FRIDAY = "fri"
    SATURDAY = "sat"
    SUNDAY = "sun"


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


