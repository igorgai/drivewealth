from marshmallow import Schema, post_load

from collections import namedtuple

from decimal import Decimal


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


def create_object_from_json_response(object_name, res, many=False):
    '''
    Creates an object with the name `object_name` from an API
    response (assumes that the response has valid JSON attached to it).
    '''
    res.raise_for_status()

    schema_class = _get_schema_class(object_name)
    schema = schema_class(object_name, many=many)

    user_data = res.json(parse_float=Decimal)
    result = schema.load(user_data)

    return result.data


def _get_schema_class(object_name):
    '''
    Basically a factory method to get the appropriate schema class
    based on the object_name.
    '''
    # Key is the name of the object, value is the schema class

    from .instrument import InstrumentSchema, InstrumentDataSchema
    from .account import OrderSchema, PositionSchema, AccountSchema, SessionSchema, UserSchema

    schema_dict = {
        'Session': SessionSchema,
        'User': UserSchema,
        'Account': AccountSchema,
        'Order': OrderSchema,
        'Position': PositionSchema,
        'Instrument': InstrumentSchema,
        'InstrumentData': InstrumentDataSchema,
    }

    schema_class = schema_dict.get(object_name)

    if not schema_class:
        raise Exception('Invalid object_name passed in: "%s"' % object_name)

    return schema_class
