from flask import request
from sqlalchemy.orm.exc import NoResultFound
from . import api
from .authors_schema import AuthorSchema
from ..models.authors import Author
from ..common.resources import GenericResource
from ..common.views import BaseView


class AuthorResource(GenericResource):
    model = Author
    serializer_class = AuthorSchema
    search_fields = ('name', 'email')
    order_fields = ('name', 'email')
    filter_fields = ('name', 'email')


class AuthorView(BaseView):
    resource = AuthorResource()

    def get(self, author_id=None):
        if author_id:
            try:
                return self.json_response(
                    self.resource.detail(author_id), self.HTTP.OK
                )
            except NoResultFound:
                return self.json_response(
                    {}, self.HTTP.NOT_FOUND
                )

        search = request.args.get('search')
        ordering = request.args.get('ordering')
        filters = request.args.get('filters')
        return self.json_response(
            self.resource.list(
                search=search, filters=filters, ordering=ordering
            ),
            self.HTTP.OK
        )

    def post(self):
        data = request.get_json()
        try:
            author = self.resource.create(data)
            return self.json_response(
                self.resource.obj2Dict(author), self.HTTP.CREATED
            )
        except self.resource.InvalidData as e:
            return self.json_response(
                dict(errors=e.data_error), self.HTTP.BAD_REQUEST
            )

    def put(self, author_id):
        data = request.get_json()
        try:
            author = self.resource.update(author_id, data)
            return self.json_response(
                self.resource.obj2Dict(author), self.HTTP.CREATED
            )
        except self.resource.InvalidData as e:
            return self.json_response(
                dict(errors=e.data_error), self.HTTP.BAD_REQUEST
            )

    def delete(self, author_id):
        self.resource.delete(author_id)
        return self.json_response({}, self.HTTP.NO_CONTENT)


view = AuthorView.as_view('AuthorView')
api.add_url_rule('/authors', view_func=view)
api.add_url_rule('/authors/<int:author_id>', view_func=view)
