from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from crmapp.db import db
from enum import Enum


class RolesEnum(Enum):
    admin = "admin"
    manager = "manager"
    user = "user"


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), index=True, unique=True)
    password = db.Column(db.String())
    email = db.Column(db.String(), unique=True)
    role = db.Column(db.String(), index=True)

    def set_password(self, password: str) -> None:
        self.password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    @property
    def is_admin(self) -> bool:
        return self.role == RolesEnum.admin

    def __repr__(self) -> str:
        return '<User {}>'.format(self.username)

