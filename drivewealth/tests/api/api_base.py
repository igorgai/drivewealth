from ...api import Api

from unittest import TestCase
import pytest


@pytest.mark.integration
class TestApiBase(TestCase):
    '''
    Provides a clean base for API integration tests
    '''
    def _get_username_and_password(self):
        username = pytest.config.getoption("--username")

        if not username:
            pytest.fail("Username is required to be passed in with --username command-line option")

        password = pytest.config.getoption("--password")

        if not password:
            pytest.fail('Password is required to be passed in with --password command-line option')

        return (username, password)

    def setUp(self):
        (self.username, self.password) = self._get_username_and_password()
        self.api = Api(self.username, self.password)

    def tearDown(self):
        self.api = None
