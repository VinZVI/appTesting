from flask_wtf import FlaskForm
from wtforms import TimeField, StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, NumberRange, ValidationError, Length
from crmapp.tables.models import Table


class BookingForm(FlaskForm):
    bookers_name = StringField(
        'Имя',
        validators=[DataRequired(), Length(min=1, max=25)],
        render_kw={
            "class": "form-control",
            "placeholder": "Имя"
        }
    )

    start_date_time_brooke = TimeField(
        validators=[DataRequired()],
        render_kw={
            "class": "form-control"
        }
    )

    finish_date_time_brooke = TimeField(
        validators=[DataRequired()],
        render_kw={
            "class": "form-control"
        }
    )


