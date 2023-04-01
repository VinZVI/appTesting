from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from crmapp.hookahs.models import Hookah


class HookahForm(FlaskForm):
    name_hookah = StringField(
        'Название Кальянной',
        validators=[DataRequired(), Length(min=3, max=25)],
        render_kw={
            "class": "form-hookah-table",
            "placeholder": "Название Кальянной"
        }
    )

    # submit = SubmitField(
    #     'Add',
    #     render_kw={
    #         "class": "bi bi-plus"
    #     }
    # )

    def validate_hookah_name(self, name_hookah: StringField) -> Exception:
        users_count = Hookah.query.filter_by(name_hookah=name_hookah.data).count()
        if users_count > 0:
            raise ValidationError('Введены не корректные данные "Имя пользователя"')


class RegistrationForm(FlaskForm):
    username = StringField(
        'Имя пользователя',
        validators=[DataRequired(),  Length(min=3, max=25)],
        render_kw={
            "class": "form-control",
            "placeholder": "User name"
        })
    email = StringField(
        'Email',
        validators=[DataRequired(), Email(),  Length(min=6, max=35)],
        render_kw={
            "class": "form-control",
            "type": "email",
            "placeholder": "Email"
        }
    )

    submit = SubmitField(
        'Отправить!',
        render_kw={"class": "btn btn-primary"}
    )

    def validate_hookah_name(self, username: StringField) -> Exception:
        users_count = Hookah.query.filter_by(username=username.data).count()
        if users_count > 0:
            raise ValidationError('Введены не корректные данные "Имя пользователя"')


