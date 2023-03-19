from crmapp.db import db



class Tables(db.Model):
    pass
    id = db.Column(db.Integer, primary_key=True)  # первичный ключ
    title = db.Column(db.String, nullable=False)  # nullable=False - не может быть пустым
    url = db.Column(db.String, unique=True, nullable=False)  # unique=True - url уникальный
    published = db.Column(db.DateTime, nullable=False)
    text = db.Column(db.Text, nullable=True)

    def __repr__(self):  # метод для отображения объекта
        return '<News {} {}>'.format(self.title, self.url)