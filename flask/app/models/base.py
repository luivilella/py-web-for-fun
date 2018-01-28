from datetime import datetime
from .. import db


def date_utcnow():
    return datetime.utcnow.date()


class BaseMixin:
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
