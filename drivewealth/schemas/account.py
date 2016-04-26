from .base import BaseSchema

from marshmallow import fields, post_load, Schema


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
