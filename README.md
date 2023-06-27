# CRM-hookahBars
### Project for Learn Python, track:  Web development
## Web application: CRM system for hookah bars

[![Python Version](https://img.shields.io/badge/python-3.10-brightgreen.svg)](https://python.org)
[![Flask Version](https://img.shields.io/badge/Flask-2.2.3-brightgreen.svg)](https://djangoproject.com)

Install the requirements:
```bash
pip install -r requirements.txt
```
add to `.env` 'SECRET_KEY' and add path to `config.py`
```python
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
```
Initializing the migration<br>
_Linux и Mac:_ 
```bash 
export FLASK_APP=crmapp && flask db init
```
_Windows:_ 
```bash
set FLASK_APP=crmapp && flask db init
```
Let's create the first migration<br>
_Linux и Mac:_ 
```bash
export FLASK_APP=crmapp && flask db migrate -m "your_comment"
```
_Windows:_ 
```bash
set FLASK_APP=crmapp && flask db migrate -m "your_comment"
```
Apply the migration and create the database
```bash
flask db upgrade
```

