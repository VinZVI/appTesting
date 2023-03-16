from getpass import getpass
import sys

from crmapp import create_app
from crmapp.db import db
from crmapp.user.models import User

app = create_app()

with app.app_context():
    username = input("Username: ")

    if User.query.filter(User.username == username).count():
        print("User already exists")
        sys.exit(0)

    password1 = getpass('Введите пароль: ')
    password2 = getpass('Повторите пароль: ')

    if not password1 == password2:
        print("Пароли не совпадают")
        sys.exit(0)

    new_user = User(username=username, role='admin')
    new_user.set_password(password1)

    db.session.add(new_user)
    db.session.commit()
    print('User with id {} added'.format(new_user.id))