import sqlalchemy as sa
from collections import Iterable


ATTRS_TO_NEVER_UPDATE = {'id', '_sa_instance_state'}


class GenericResource:
    model = NotImplemented
    serializer_class = NotImplemented
    search_fields = NotImplemented
    order_fields = NotImplemented

    def __init__(self):
        self.schema_detail = self.serializer_class()
        self.schema_list = self.serializer_class(many=True)
        if self.search_fields and not isinstance(self.search_fields, Iterable):
            self.search_fields = (self.search_fields,)

    class InvalidData(Exception):
        def __init__(self, *args, **kwargs):
            self.data_error = kwargs.pop('data_error')
            super().__init__(*args, **kwargs)

    def get_search_filters(self, search):
        for field_name in self.search_fields:
            field = getattr(self.model, field_name)
            yield field.ilike('%{}%'.format(search))

    def get_ordering_fields(self, ordering):
        for field_name in ordering.split(','):
            order = 'asc'
            if field_name.startswith('-'):
                order = 'desc'
                field_name = field_name[1:]

            field = getattr(self.model, field_name)
            yield getattr(field, order)()

    def get_query(self, search=None, ordering=None):
        query = self.model.query

        if search and self.search_fields:
            query = query.filter(
                sa.or_(*list(self.get_search_filters(search)))
            )

        if ordering and self.order_fields:
            query = query.order_by(
                *list(self.get_ordering_fields(ordering))
            )
        else:
            query = query.order_by(*list(self.get_ordering_fields('-id')))

        return query

    def list(self, search=None, ordering=None):
        query = self.get_query(search, ordering)
        return self.schema_list.dump(query).data

    def obj2Dict(self, obj):
        return self.schema_detail.dump(obj).data

    def detail(self, obj_id):
        obj = self.model.get_by(id=obj_id)
        return self.obj2Dict(obj)

    def create(self, raw_data):
        result = self.schema_detail.load(raw_data)
        if result.errors:
            raise self.InvalidData(data_error=result.errors)

        obj = result.data
        obj.create_or_update()
        return obj

    def update(self, obj_id, raw_data):
        result = self.schema_detail.load(raw_data)
        if result.errors:
            raise self.InvalidData(data_error=result.errors)

        new_data = (
            (k, v) for k, v in result.data.__dict__.items()
            if k not in ATTRS_TO_NEVER_UPDATE
        )

        instance = self.model.get_by(id=obj_id)
        for attr, value in new_data:
            setattr(instance, attr, value)
        instance.create_or_update()

        return instance

    def delete(self, obj_id):
        instance = self.model.get_by(id=obj_id)
        instance.delete()
