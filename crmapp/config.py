import os

from datetime import timedelta
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '..\.', '.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

basedir = os.path.abspath(os.path.dirname(__file__))

# Устанавливает время хранения файлов cookie в браузере
REMEMBER_COOKIE_DURATION = timedelta(days=5)

# Устанавливает директорию для хранения файла БД (SQLite3)
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '..\.', 'crmapp.db')

# Секретный ключ для хеширования пароля
SECRET_KEY = os.environ['SECRET_KEY']

# Это отключит функционал отправки сигнала приложению при изменениях в БД
SQLALCHEMY_TRACK_MODIFICATIONS = False
