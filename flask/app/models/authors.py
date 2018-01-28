from .. import db
from .base import BaseMixin


class Author(BaseMixin, db.Model):
    __tablename__ = 'author'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
