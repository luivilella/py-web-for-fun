from ..models.authors import Author
from .authors_schema import author_schema, authors_schema
from ..common.resources import GenericResource


class AuthorResource(GenericResource):
    model = Author
    schema_detail = author_schema
    schema_list = authors_schema
