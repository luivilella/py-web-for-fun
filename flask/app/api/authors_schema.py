from marshmallow import fields
from .. import ma
from ..models.authors import Author


class AuthorSchema(ma.ModelSchema):

    name = fields.Str()
    email = fields.Email()
    created_at = fields.DateTime(dump_only=True)
    total_books = fields.Int(dump_only=True)
    last_book = fields.Method('get_last_book', dump_only=True)

    def get_last_book(self, author):
        book = author.last_book()
        return getattr(book, 'title', None)

    class Meta:
        model = Author
        fields = (
            'id',
            'created_at',
            'name',
            'email',
            'total_books',
            'last_book'
        )


author_schema = AuthorSchema()
authors_schema = AuthorSchema(many=True)
