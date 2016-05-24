from .api_base import TestApiBase


class TestSessionApi(TestApiBase):
    def test_create_session(self):
        self.api.create_session(self.username, self.password)
        self.assertIsNotNone(self.api.session_key)
        self.assertIsNotNone(self.api.user_id)
        self.assertIsNotNone(self.api.accounts)
        self.assertGreater(len(self.api.accounts), 0)

    def test_heartbeat(self):
        self.api.heartbeat()

    def test_logout(self):
        self.api.logout()
