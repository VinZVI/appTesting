import os
basedir = os.path.abspath(os.path.dirname(__file__))
from datetime import timedelta

REMEMBER_COOKIE_DURATION = timedelta(days=5)
SQLALCHEMY_DATABASE_URI = \
    'sqlite:///' + os.path.join(basedir, '..\.', 'crmapp.db')


WEATHER_API_KEY = '4b12746ddce34c1ca25153404232402'
WEATHER_DEFAULT_CITY = 'Moscow'

SECRET_KEY = "dsnckejwhuohvn12jj34r9u3638$@&falm9*#q2j"

SQLALCHEMY_TRACK_MODIFICATIONS = False