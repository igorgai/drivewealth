from marshmallow import Schema, post_load

from collections import namedtuple


class BaseSchema(Schema):
    '''
    Provides an easy way to an object (namedtuple) from a schema.
    '''
    def __init__(self, object_name, many=False, strict=True):
        self.object_name = object_name
        super(BaseSchema, self).__init__(many=many, strict=strict)

    @post_load()
    def post_load(self, data):
        return BaseSchema.create_object(self.object_name, data)

    @staticmethod
    def create_object(object_name, data):
        fields = data.keys()
        o = namedtuple(object_name, fields)
        return o(**data)
