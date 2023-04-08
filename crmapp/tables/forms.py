from flask_wtf import FlaskForm
from wtforms import HiddenField, IntegerField, TextAreaField, StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, NumberRange, ValidationError, Length
from crmapp.tables.models import Table


class TableForm(FlaskForm):
    table_number = StringField(
        'Название стола',
        validators=[DataRequired(), Length(min=1, max=25)],
        render_kw={
            "class": "form-control",
            "placeholder": "Название стола"
        }
    )

    description = TextAreaField(
        'Описание стола',
        validators=[DataRequired(), Length(min=1, max=250)],
        render_kw={
            "class": "form-control",
            "placeholder": "Описание стола"
        }
    )

    total_of_persons = IntegerField(
        'Количество персон',
        validators=[NumberRange(min=1, max=15)],
        render_kw={
            "class": "form-control",
            "placeholder": "Количество персон"
        }
    )

    hookah_id = HiddenField(
        'ID кальянной',
        validators=[DataRequired()]
    )


    def validate_tablename(self, table_number: StringField) -> Exception:
        users_count = Table.query.filter_by(table_number=table_number.data).count()
        if users_count > 0:
            raise ValidationError('Введены не корректные данные "Название стола"')


class TableDeleteForm(FlaskForm):
    table_number = StringField(
        'Название стола',
        validators=[DataRequired(), Length(min=1, max=25)],
        render_kw={
            "class": "form-control",
            "placeholder": "Название стола"
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

    def validate_deletetablehname(self, table_number: StringField) -> Exception:
        users_count = Table.query.filter_by(table_number=table_number.data).first()
        if users_count is None:
            raise ValidationError('Стола с таким названием не существует.')


