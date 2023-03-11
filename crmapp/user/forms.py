from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()],
                        render_kw={"class": "form-control", "id": "floatingInput", "placeholder": "Имя пользователя"})
    password = PasswordField(validators=[DataRequired()],
                             render_kw={"class": "form-control", "id": "floatingInput", "placeholder": "Password"})
    submit = SubmitField('Отправить', render_kw={"class": "w-100 btn btn-lg btn-primary"})
    remember_me = BooleanField('Запомнить меня', default=True)
