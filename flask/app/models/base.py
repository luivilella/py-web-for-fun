from datetime import datetime
from .. import db


def date_utcnow():
    return datetime.utcnow.date()


class BaseMixin:
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def create_or_update(self, auto_commit=True):
        if not self.id:
            db.session.add(self)

        if auto_commit:
            self.session_commit()

    def delete(self, auto_commit=True):
        db.session.delete(self)

        if auto_commit:
            self.session_commit()

    @classmethod
    def create(cls, **kwargs):
        auto_commit = kwargs.pop('auto_commit', None)
        obj = cls(**kwargs)

        db.session.add(obj)
        if auto_commit:
            cls.session_commit()

        return obj

    @staticmethod
    def session_commit():
        db.session.commit()

    @classmethod
    def get_by(cls, **kwargs):
        return cls.query.filter_by(**kwargs).one()
