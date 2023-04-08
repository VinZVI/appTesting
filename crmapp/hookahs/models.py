from enum import Enum

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

    def __repr__(self) -> str:  # метод для отображения объекта
        return '<Hookah {}: user {}>'.format(self.name_hookah, self.user_id)


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


