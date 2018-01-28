from .. import ma
from ..models.authors import Author


class AuthorSchema(ma.ModelSchema):
    class Meta:
        model = Author


author_schema = AuthorSchema()
authors_schema = AuthorSchema(many=True)
