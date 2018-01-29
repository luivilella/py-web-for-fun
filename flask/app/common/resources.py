class GenericResource:
    model = NotImplemented
    schema_detail = NotImplemented
    schema_list = NotImplemented

    class InvalidData(Exception):
        def __init__(self, *args, **kwargs):
            self.data_error = kwargs.pop('data_error')
            super().__init__(*args, **kwargs)

    def list(self):
        query = (
            self.model.query
            .order_by(self.model.id.asc())
        )
        return self.schema_list.dump(query).data

    def obj2Dict(self, obj):
        return self.schema_detail.dump(obj).data

    def detail(self, obj_id):
        obj = self.model.query.filter_by(id=obj_id).one()
        return self.obj2Dict(obj)

    def create(self, raw_data):
        result = self.schema_detail.load(raw_data)
        if result.errors:
            raise self.InvalidData(data_error=result.errors)

        obj = result.data
        obj.create_or_update()
        return obj
