from flask import render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user

from crmapp.user.forms import LoginForm
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
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('Вы вошли на сайт')
            return redirect(url_for('tables.index'))
    flash('Неправильное имя пользователя или пароль')
    return redirect(url_for('user.login'))


@blueprint.route('/logout')
def logout():
    logout_user()
    flash('Вы вышли из системы')
    return redirect(url_for('tables.index'))
