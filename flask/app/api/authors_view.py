from sqlalchemy.orm.exc import NoResultFound
from . import api
from ..common.views import BaseView
from .authors_resource import AuthorResource


class AuthorView(BaseView):
    resource = AuthorResource()

    def get(self, author_id=None):
        if author_id:
            try:
                return self.json_response(self.resource.detail(author_id))
            except NoResultFound:
                return self.json_response({}, 404)

        return self.json_response(self.resource.list())


view = AuthorView.as_view('AuthorView')
api.add_url_rule('/authors', view_func=view)
api.add_url_rule('/authors/<int:author_id>', view_func=view)
