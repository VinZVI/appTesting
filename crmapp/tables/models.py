from datetime import datetime, timedelta, time
from enum import Enum

from flask import current_app
from crmapp.db import db
from crmapp.time_fuctions import round_dt_to_delta


class TableStateEnum(Enum):
    open_order = "open order"
    free = "free"
    booked = "booked"


class Table(db.Model):
    __tablename__: str = "tables"
    id = db.Column(db.Integer, primary_key=True)  # первичный ключ
    table_number = db.Column(db.String, nullable=False)  # nullable=False - не может быть пустым
    description = db.Column(db.Text)
    total_of_persons = db.Column(
        db.Integer,
        nullable=False,
        default=4
    )
    table_state = db.Column(
        db.Enum(TableStateEnum),
        default=TableStateEnum.free
    )
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
