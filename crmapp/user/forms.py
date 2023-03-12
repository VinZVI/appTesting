from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from crmapp.user.models import User


class LoginForm(FlaskForm):
    login_username = StringField('Имя пользователя',
                                 validators=[DataRequired()],
                                 render_kw={"class": "form-control",
                                            "placeholder": "Имя пользователя"})
    login_password = PasswordField(validators=[DataRequired()],
                                   render_kw={"class": "form-control",
                                              "placeholder": "Password"})
    submit = SubmitField('Отправить',
                         render_kw={"class": "w-100 btn btn-lg btn-primary"})
    remember_me = BooleanField('Запомнить меня', default=True)


class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()],
                           render_kw={"class": "form-control",
                                      "placeholder": "User name"})
    email = StringField('Email', validators=[DataRequired(), Email()],
                        render_kw={"class": "form-control", "type": "email",
                                   "placeholder": "Email"})
    password = PasswordField('Пароль', validators=[DataRequired()],
                             render_kw={"class": "form-control",
                                        "type": "password",
                                        "placeholder": "Password"})
    password2 = PasswordField('Повторите пароль',
                              validators=[DataRequired(), EqualTo('password')],
                              render_kw={"class": "form-control",
                                         "type": "password",
                                         "placeholder": "Password"})
    submit = SubmitField('Отправить!', render_kw={"class": "btn btn-primary"})

    def validate_username(self, username):
        users_count = User.query.filter_by(username=username.data).count()
        if users_count > 0:
            raise ValidationError(
                'Пользователь с таким именем уже зарегистрирован')

    def validate_email(self, email):
        users_count = User.query.filter_by(email=email.data).count()
        if users_count > 0:
            raise ValidationError(
                'Пользователь с такой электронной почтой уже зарегистрирован'
            )