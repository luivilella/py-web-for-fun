from http import HTTPStatus
from flask.views import MethodView
from flask import jsonify


class BaseView(MethodView):

    HTTP = HTTPStatus

    def json_response(self, _dict, status_code=HTTPStatus.OK):
        return jsonify(_dict), status_code
