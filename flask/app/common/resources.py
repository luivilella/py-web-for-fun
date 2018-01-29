class GenericResource:
    model = NotImplemented
    schema_detail = NotImplemented
    schema_list = NotImplemented

    def list(self):
        return self.schema_list.dump(self.model.query.all()).data

    def detail(self, obj_id):
        obj = self.model.query.filter_by(id=obj_id).one()
        return self.schema_detail.dump(obj).data

    def create(self, data):
        pass
