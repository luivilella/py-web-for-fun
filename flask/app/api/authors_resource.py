from ..models.authors import Author
from .authors_schema import author_schema, authors_schema


class AuthorResource:
    def list(self):
        return authors_schema.dump(Author.query.all()).data

    def detail(self, author_id):
        author = Author.query.filter_by(id=author_id).one()
        return author_schema.dump(author).data
