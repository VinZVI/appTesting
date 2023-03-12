from flask import render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user
from crmapp.db import db
from crmapp.user.forms import LoginForm, RegistrationForm
from crmapp.user.models import User

from flask import Blueprint

blueprint = Blueprint('user', __name__, url_prefix='/users')


@blueprint.route("/login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for('tables.index'))
    title = "Авторизация"
    login_form = LoginForm()
    return render_template('user/login.html', title=title, form=login_form)


@blueprint.route('/process-login', methods=['POST'])
def process_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.login_username.data).first()
        if user and user.check_password(form.login_password.data):
            login_user(user, remember=form.remember_me.data)
            flash('Вы вошли на сайт')
            return redirect(url_for('tables.index'))
    flash('Неправильное имя пользователя или пароль')
    return redirect(url_for('user.login'))


@blueprint.route('/register')
def register():
    if current_user.is_authenticated:
        return redirect(url_for('tables.index'))
    form = RegistrationForm()
    title = "Регистрация"
    return render_template('user/registration.html', title=title, form=form)


@blueprint.route('/process-reg', methods=['POST'])
def process_reg():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data,
                         email=form.email.data, role='admin')
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Вы успешно зарегистрировались!')
        return redirect(url_for('user.login'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash('Ошибка в поле "{}": - {}'.format(
                    getattr(form, field).label.text,
                    error
                ))
        return redirect(url_for('user.register'))
    flash('Пожалуйста, исправьте ошибки в форме')
    return redirect(url_for('user.register'))


@blueprint.route('/logout')
def logout():
    logout_user()
    flash('Вы вышли из системы')
    return redirect(url_for('tables.index'))
