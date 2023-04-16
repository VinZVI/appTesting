from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, PasswordField, HiddenField, TimeField, SelectField
from wtforms.validators import DataRequired, NumberRange, ValidationError, Length
from crmapp.hookahs.models import Hookah, WeekDayEnum


class HookahForm(FlaskForm):
    name_hookah = StringField(
        'Название Кальянной',
        validators=[DataRequired(), Length(min=3, max=25)],
        render_kw={
            "class": "form-control",
            "placeholder": "Название Кальянной"
        }
    )

    count_tables = IntegerField(
        'Количество столов',
        validators=[NumberRange(min=1, max=25)],
        render_kw={
            "class": "form-control",
            "placeholder": "Количество столов"
        }
    )

    def validate_hookahname(self, name_hookah: StringField) -> Exception:
        users_count = Hookah.query.filter_by(name_hookah=name_hookah.data).count()
        if users_count > 0:
            raise ValidationError('Введены не корректные данные "Название кальянной"')


class HookahDeleteForm(FlaskForm):
    name_hookah = StringField(
        'Название Кальянной',
        validators=[DataRequired(), Length(min=3, max=25)],
        render_kw={
            "class": "form-control",
            "placeholder": "Название Кальянной"
        }
    )

    login_password = PasswordField(
        validators=[DataRequired(), Length(max=35)],
        render_kw={
            "class": "form-control",
            "placeholder": "Password"
        }
    )

    submit = SubmitField(
        'DELETE',
        render_kw={"class": "btn btn-primary"}
    )

    def validate_deletehookahname(self, name_hookah: StringField) -> Exception:
        users_count = Hookah.query.filter_by(name_hookah=name_hookah.data).first()
        if users_count is None:
            raise ValidationError('Кальянной с таким названием не существует.')


class WorkingDayForm(FlaskForm):
    week_day = HiddenField(
        'День недели'
    )

    startWD_time = TimeField(
        validators=[DataRequired()],
        render_kw={
            "class": "form-control"
        }
    )

    finishWD_time = TimeField(
        validators=[DataRequired()],
        render_kw={
            "class": "form-control"
        }
    )

    period_time_panel = TimeField(
        validators=[DataRequired()],
        render_kw={
            "class": "form-control"
        }
    )

