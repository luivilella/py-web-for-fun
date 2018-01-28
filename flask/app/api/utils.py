from flask.views import MethodView
from flask import jsonify


class BaseView(MethodView):

    def json_response(self, _dict, status_code=200):
        return jsonify(_dict), status_code
