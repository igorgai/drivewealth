from ..schemas import _get_schema_class, create_object_from_json_response

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
            u'languageID': u'en_US',
            u'rebateCfdValue': 0,
            u'rebateEquityValue': 0,
            u'lastLoginWhen': u'2016-04-13T18:19:41.066Z',
            u'wlpID': u'DW',
            u'statementPrint': False,
            u'createdWhen': u'2016-04-05T17:34:26.801Z',
            u'avatarUrl': u'https://secure.gravatar.com/avatar/bill.jpg',
            u'userID': u'9875cfd1-07e9-4647-8e7e-8c781269a4d3',
            u'sessionKey': u'1782cfd1-07l9-4647-8e7e-8c926071a4d9.2016-04-13T18:19:40.736Z',
            u'emailAddress1': u'bill@mailinator.com',
            u'referralCode': u'REF',
            u'username': u'testusername',
            u'rebateFxValue': 0,
            u'usCitizen': False,
            u'brandAmbassador': False,
            u'displayName': u'Bill',
            u'firstName': u'Bill',
            u'lastName': u'Smith',
            u'updatedWhen': u'2016-04-05T17:34:26.801Z',
            u'commissionRate': 2.99,
            u'confirmPrint': False,
            u'coinBalance': 0,
            u'status': 1,
            u'countryID': "US",
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
            u'status': "asdf",
            u'countryID': "US",
        }
        res = self.FakeResponse(data=data)

        with self.assertRaises(Exception) as context:
            create_object_from_json_response('User', res)

        self.assertIsNotNone(context.exception)
