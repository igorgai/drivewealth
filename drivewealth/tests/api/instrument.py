from .api_base import TestApiBase
from ...exceptions import InstrumentNotFoundError

from uuid import UUID


class TestInstrumentApi(TestApiBase):
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
            self.api.get_instrument('asdf')

        self.assertIsNotNone(context.exception)

    def test_get_instrument_invalid_uuid_instrument_id(self):
        with self.assertRaises(InstrumentNotFoundError) as context:
            self.api.get_instrument('a67422af-8504-43df-9e63-7361eb0bd98a')

        self.assertIsNotNone(context.exception)
