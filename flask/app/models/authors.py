from sqlalchemy.sql import text
from .. import db
from .base import BaseMixin


class Author(BaseMixin, db.Model):
    __tablename__ = 'author'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255), nullable=True)

    @property
    def total_books(self):
        return self.books.count()

    def last_book(self):
        return self.books.order_by(text('created_at DESC')).first()
