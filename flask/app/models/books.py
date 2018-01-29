from .. import db
from .base import BaseMixin


class Book(BaseMixin, db.Model):
    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    author = db.relationship(
        'Author', foreign_keys=[author_id],
        backref=db.backref('books', lazy='dynamic'),
    )
