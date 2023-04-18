from datetime import datetime

from crmapp.db import db
from sqlalchemy.orm import relationship


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(25), nullable=False)
    category_description = db.Column(db.String(60), nullable=True)

    hookah_id = db.Column(
        db.Integer,
        db.ForeignKey('hookahs.id', ondelete='CASCADE'),
        index=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        index=True
    )

    hookah = relationship('Hookah', backref='categories')
    user = relationship('User', backref='categories')
    items = relationship('Item', backref='category', uselist=False)

    def items_count(self):
        return Item.query.filter(Item.category_id == self.id).count()
    
    def __repr__(self):  # метод для отображения объекта
        return '<Category {} {}>'.format(self.id, self.category_name)
    
class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(50), nullable=False)
    item_description = db.Column(db.String(150), nullable=True)
    price = db.Column(db.Integer, index=True, nullable=False)
    availability = db.Column(db.Integer, index=True, nullable=False)
    is_archived = db.Column(db.Boolean, index=True, default=False, nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    archivation_date = db.Column(db.DateTime, nullable=False)

    category_id = db.Column(
        db.Integer,
        db.ForeignKey('categories.id', ondelete='CASCADE'),
        index=True
    )
    
    hookah_id = db.Column(
        db.Integer,
        db.ForeignKey('hookahs.id', ondelete='CASCADE'),
        index=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        index=True
    )

    hookah = relationship('Hookah', backref='items')
    user = relationship('User', backref='items')

    def __repr__(self):  # метод для отображения объекта
        return '<Item {} {}>'.format(self.id, self.item_name)    

