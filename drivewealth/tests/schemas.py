from ..schemas.base import _get_schema_class, create_object_from_json_response

from unittest import TestCase


class TestGetSchemaClass(TestCase):
    def test_get_schema_class_valid_object_name(self):
        schema_class = _get_schema_class('User')
        self.assertIsNotNone(schema_class)

    def test_get_schema_class_invalid_object_name(self):
        with self.assertRaises(Exception) as context:
            _get_schema_class('asdf')

        self.assertIsNotNone(context.exception)


class TestCreateObjectFromJsonResponse(TestCase):
    class FakeResponse(object):
        data = {
            'languageID': 'en_US',
            'rebateCfdValue': 0,
            'rebateEquityValue': 0,
            'lastLoginWhen': '2016-04-13T18:19:41.066Z',
            'wlpID': 'DW',
            'statementPrint': False,
            'createdWhen': '2016-04-05T17:34:26.801Z',
            'avatarUrl': 'https://secure.gravatar.com/avatar/bill.jpg',
            'userID': '9875cfd1-07e9-4647-8e7e-8c781269a4d3',
            'sessionKey': '1782cfd1-07l9-4647-8e7e-8c926071a4d9.2016-04-13T18:19:40.736Z',
            'emailAddress1': 'bill@mailinator.com',
            'referralCode': 'REF',
            'username': 'testusername',
            'rebateFxValue': 0,
            'usCitizen': False,
            'brandAmbassador': False,
            'displayName': 'Bill',
            'firstName': 'Bill',
            'lastName': 'Smith',
            'updatedWhen': '2016-04-05T17:34:26.801Z',
            'commissionRate': 2.99,
            'confirmPrint': False,
            'coinBalance': 0,
            'status': 1,
            'countryID': "US",
        }

        def __init__(self, data=data):
            self.data = data

        def json(self, parse_float=None):
            return self.data

        def raise_for_status(self):
            return None

    def test_create_object_from_json_response(self):
        res = self.FakeResponse()
        user = create_object_from_json_response('User', res)

        self.assertIsNotNone(user)
        self.assertIsNotNone(user.status)

    def test_create_object_from_invalid_json_response(self):
        data = {
            'status': "asdf",
            'countryID': "US",
        }
        res = self.FakeResponse(data=data)

        with self.assertRaises(Exception) as context:
            create_object_from_json_response('User', res)

        self.assertIsNotNone(context.exception)
