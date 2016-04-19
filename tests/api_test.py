from ..api import Api as api
from ..exceptions import InstrumentNotFoundError

from unittest import TestCase
from uuid import UUID
import pytest


@pytest.mark.integration
class TestApi(TestCase):
    def setUp(self):
        self.username = pytest.config.getoption("--username")

        if not self.username:
            pytest.fail("Username is required to be passed in with --username command-line option")

        self.password = pytest.config.getoption("--password")

        if not self.password:
            pytest.fail('Password is required to be passed in with --password command-line option')

        self.api = api(self.username, self.password)

    def tearDown(self):
        self.api = None

    def test_create_session(self):
        self.api._create_session(self.username, self.password)
        self.assertIsNotNone(self.api.session_key)
        self.assertIsNotNone(self.api.user_id)
        self.assertIsNotNone(self.api.accounts)
        self.assertGreater(len(self.api.accounts), 0)

    def test_get_user(self):
        user = self.api.get_user(self.api.user_id)
        self.assertIsNotNone(user)
        self.assertEqual(user.status, 1)
        self.assertIsNotNone(user.country_id)
        self.assertIsNotNone(user.email)
        self.assertIsNotNone(user.session_key)
        self.assertIsNotNone(user.last_login)
        self.assertIsNotNone(user.id)
        self.assertIsNotNone(user.username)
        self.assertIsNotNone(user.first_name)
        self.assertIsNotNone(user.last_name)

    def test_heartbeat(self):
        self.api.heartbeat()

    def test_logout(self):
        self.api.logout()

    def test_search_instruments_by_symbol(self):
        instruments = self.api.search_instruments(symbol='AAPL')
        self.assertIsNotNone(instruments)
        self.assertGreater(len(instruments), 0)

    def test_search_instruments_by_name(self):
        instruments = self.api.search_instruments(name='Apple')
        self.assertIsNotNone(instruments)
        self.assertGreater(len(instruments), 0)

    def test_get_instrument_string(self):
        instrument = self.api.get_instrument('a67422af-8504-43df-9e63-7361eb0bd99e')
        self.assertIsNotNone(instrument)
        self.assertEqual(instrument.symbol, 'AAPL')
        self.assertIsNotNone(instrument.data)
        self.assertIsNotNone(instrument.data.fifty_two_week_low_price)

    def test_get_instrument_uuid(self):
        instrument = self.api.get_instrument(UUID('a67422af-8504-43df-9e63-7361eb0bd99e'))
        self.assertIsNotNone(instrument)
        self.assertEqual(instrument.symbol, 'AAPL')

    def test_get_instrument_invalid_string_instrument_id(self):
        with self.assertRaises(InstrumentNotFoundError) as context:
            instrument = self.api.get_instrument('asdf')

        self.assertIsNotNone(context.exception)

    def test_get_instrument_invalid_uuid_instrument_id(self):
        with self.assertRaises(InstrumentNotFoundError) as context:
            instrument = self.api.get_instrument('a67422af-8504-43df-9e63-7361eb0bd98a')

        self.assertIsNotNone(context.exception)
