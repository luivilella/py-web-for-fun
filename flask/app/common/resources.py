ATTRS_TO_NEVER_UPDATE = {'id', '_sa_instance_state'}


class GenericResource:
    model = NotImplemented
    serializer_class = NotImplemented

    def __init__(self):
        self.schema_detail = self.serializer_class()
        self.schema_list = self.serializer_class(many=True)

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
