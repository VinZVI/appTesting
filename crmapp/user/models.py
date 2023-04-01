from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from crmapp.db import db
from enum import Enum


class RolesEnum(Enum):
    admin = "admin"
    manager = "manager"
    personal = "personal"


class User(db.Model, UserMixin):
    __tablename__: str = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(
        db.String(),
        index=True,
        nullable=False,
        unique=True
    )
    password = db.Column(db.String(), nullable=False)
    email = db.Column(
        db.String(),
        unique=True,
        nullable=False
    )
    role = db.Column(
        db.Enum(RolesEnum),
        nullable=False,
        index=True,
        default=RolesEnum.manager
    )

    hookahs = db.relationship(
        'Hookah',
        backref='user',
        lazy='dynamic'
    )

    def set_password(self, password: str) -> None:
        self.password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    @property
    def is_admin(self) -> bool:
        return self.role == RolesEnum.admin

    @property
    def is_manager(self) -> bool:
        return self.role == RolesEnum.manager

    def __repr__(self) -> str:
        return '<User {}>'.format(self.username)

