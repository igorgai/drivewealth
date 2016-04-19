from .schema_base import BaseSchema

from marshmallow import fields, post_load, Schema

from decimal import Decimal


class InstrumentDataSchema(Schema):
    # Can't inherit from BaseSchema because marshmallow throws an exception
    fifty_two_week_low_price = fields.Decimal(load_from='fiftyTwoWeekLowPrice')

    @post_load()
    def post_load(self, data):
        return BaseSchema.create_object('InstrumentData', data)


class InstrumentSchema(BaseSchema):
    instrument_id = fields.UUID(load_from='instrumentID')
    name = fields.String()
    symbol = fields.String()
    exchange_id = fields.String(load_from='exchangeID')
    trade_status = fields.Integer(load_from='tradeStatus')
    long_only = fields.Boolean(load_from='longOnly')
    prior_close = fields.Decimal(load_from='priorClose')
    order_size_maximum = fields.Decimal(load_from='orderSizeMax')
    order_size_minimum = fields.Decimal(load_from='orderSizeMin')
    order_size_step = fields.Decimal(load_from='orderSizeStep')
    rate_ask = fields.Decimal(load_from='rateAsk')
    rate_bid = fields.Decimal(load_from='rateBid')
    data = fields.Nested(InstrumentDataSchema, load_from='fundamentalDataModel')  # required=False


class OrderSchema(Schema):
    # Can't inherit from BaseSchema because marshmallow throws an exception
    order_id = fields.UUID(load_from='orderID')
    commission = fields.Decimal(load_from='commission')
    order_number = fields.String(load_from='orderNo')
    order_quantity = fields.Decimal(load_from='orderQty')
    order_status = fields.String(load_from='ordStatus')
    price = fields.Decimal(load_from='price')
    limit_price = fields.Decimal(load_from='limitPrice')
    resting_order_expires = fields.DateTime(load_from='isoTimeRestingOrderExpires')
    amount_cash = fields.Decimal(load_from='amountCash')
    rate_ask = fields.Decimal(load_from='rateAsk')
    rate_bid = fields.Decimal(load_from='rateBid')
    instrument_id = fields.UUID(load_from='instrumentID')

    @post_load()
    def post_load(self, data):
        return BaseSchema.create_object('Order', data)


class PositionSchema(Schema):
    # Can't inherit from BaseSchema because marshmallow throws an exception
    initial_quantity = fields.Decimal(load_from='initQty')
    open_quantity = fields.Decimal(load_from='openQty')
    instrument_id = fields.UUID(load_from='instrumentID')
    cost_basis = fields.Decimal(load_from='costBasis')

    @post_load()
    def post_load(self, data):
        return BaseSchema.create_object('Position', data)


class AccountSchema(Schema):
    # Can't inherit from BaseSchema because marshmallow throws an exception
    id = fields.String(load_from='accountID')
    currency_id = fields.String(load_from='currencyID')
    cash_available_for_withdrawal = fields.Decimal(load_from='rtCashAvailForWith')
    cash_available_for_trading = fields.Decimal(load_from='rtCashAvailForTrading')
    status = fields.Integer(load_from='status')
    positions = fields.Nested(PositionSchema, many=True)
    orders = fields.Nested(OrderSchema, many=True)
    type = fields.Integer(load_from='accountType')
    cash = fields.Decimal(load_from='cash')
    account_number = fields.String(load_from='accountNo')

    @post_load()
    def post_load(self, data):
        return BaseSchema.create_object('Account', data)


class SessionSchema(BaseSchema):
    session_key = fields.String(load_from='sessionKey')
    user_id = fields.UUID(load_from='userID')
    accounts = fields.Nested(AccountSchema, many=True)


class UserSchema(BaseSchema):
    status = fields.Integer(load_from='status')
    country_id = fields.String(load_from='countryID')
    email = fields.Email(load_from='emailAddress1')
    session_key = fields.String(load_from='sessionKey')
    last_login = fields.DateTime(load_from='lastLoginWhen')
    id = fields.UUID(load_from='userID')
    username = fields.String(load_from='username')
    first_name = fields.String(load_from='firstName')
    last_name = fields.String(load_from='lastName')


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
