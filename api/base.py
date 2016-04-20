from hammock import Hammock as DriveWealth

from instrument import InstrumentApiMixin
from session import SessionApiMixin
from user import UserApiMixin


class Api(SessionApiMixin, UserApiMixin, InstrumentApiMixin):
    API_BASE_URL = 'https://api.drivewealth.io/v1'

    def __init__(self, username, password, api_base_url=API_BASE_URL):
        self.username = username
        self.password = password
        self.api_base_url = api_base_url

        # Initial api setup before a session has been created
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        self.drive_wealth = DriveWealth(self.api_base_url, headers=headers)

        # from session import create_session
        self.create_session(username, password)

        # Create api with the generated session
        headers['x-mysolomeo-session-key'] = self.session_key
        self.drive_wealth = DriveWealth(self.api_base_url, headers=headers)
