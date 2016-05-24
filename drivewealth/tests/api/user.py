from .api_base import TestApiBase


class TestUserApi(TestApiBase):
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
