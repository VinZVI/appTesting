from datetime import datetime, timedelta, time
from enum import Enum

from flask import current_app
from crmapp.db import db
from crmapp.config import DELTA_TIME_ROUND


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

    def __repr__(self):  # метод для отображения объекта
        return '<Hookah {}: user {}>'.format(self.name_hookah, self.user_id)



class TableStateEnum(Enum):
    open_order = "open_order"
    free = "free"
    booked = "booked"


class Table(db.Model):
    __tablename__: str = "tables"
    id = db.Column(db.Integer, primary_key=True)  # первичный ключ
    table_number = db.Column(db.String, nullable=False)  # nullable=False - не может быть пустым
    description = db.Column(db.Text)
    total_of_persons = db.Column(db.Integer, nullable=False, default=4)
    table_state = db.Column(db.String)
    booked = db.relationship(
        'DateTimeBooked',
        backref='table_number',
        lazy='dynamic'
    )

    hookah_id = db.Column(
        db.Integer,
        db.ForeignKey('hookahs.id', ondelete='CASCADE'),
        index=True
    )

    def __repr__(self):  # метод для отображения объекта
        return '<Table {}: hookah {}>'.format(self.table_number, self.hookah_id)


def round_dt_to_delta(dt: datetime = datetime.now(), delta: timedelta = timedelta(minutes=30)) -> timedelta:
    """Округляет время до периода бронирования столов
    :param dt: Timestamp to round (default: now)
    :param delta: Lapse to round in minutes (default: minutes=30)
    """
    ref = datetime.min.replace(tzinfo=dt.tzinfo)
    return ref + round((dt - ref) / delta) * delta


class DateTimeBooked(db.Model):
    __tablename__: str = "dt_booked"
    id = db.Column(db.Integer, primary_key=True)  

    start_date_time_brooke = db.Column(db.DateTime, nullable=False)
    finish_date_time_brooke = db.Column(db.DateTime, nullable=False)

    table_id = db.Column(
        db.Integer,
        db.ForeignKey('tables.id', ondelete='CASCADE'),
        index=True
    )

    def __init__(self, **kwargs):
        super(DateTimeBooked, self).__init__(**kwargs)
        if self.start_date_time_brooke is None:
            self.start_date_time_brooke = round_dt_to_delta(
                                                            datetime.utcnow,
                                                            current_app.config['DELTA_TIME_ROUND']
                                                            )

    def __repr__(self):  
        return f'<Table {self.table_number_id}: start_dt_brooke {self.start_date_time_brooke}>'


class WeekDayEnum(Enum):
    MONDAY = "mon"
    TUESDAY = "tue"
    WEDNESDAY = "wed"
    THURSDAY = "thu"
    FRIDAY = "fri"
    SATURDAY = "sat"
    SUNDAY = "sun"


class WorkerDay(db.Model):
    __tablename__: str = "worker_day"
    id = db.Column(db.Integer, primary_key=True)
    week_day = db.Column(db.Enum(WeekDayEnum), nullable=False)
    startWD_time = db.Column(db.Time, nullable=False)
    finishWD_time = db.Column(db.Time, nullable=False)
    period_time_panel = db.Column(
        db.Time,
        nullable=False,
        default=DELTA_TIME_ROUND
    )

    hookah_id = db.Column(db.Integer, db.ForeignKey('hookahs.id'))

    def __repr__(self):
        return f'<Day of week {self.day_of_week}>'


