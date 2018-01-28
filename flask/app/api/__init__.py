from flask import Blueprint

api = Blueprint('api', __name__)

from . import authors_view   # noqa: E402, F401
