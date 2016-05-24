from .api_base import TestApiBase

from decimal import Decimal


class TestOrderApi(TestApiBase):
    def test_get_accounts(self):
        for account in self.api.accounts:
            self.assertIsNotNone(account.cash)
            self.assertTrue(isinstance(account.cash, Decimal))
