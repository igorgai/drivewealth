from ..schemas import create_object_from_json_response

import json


class SessionApiMixin:
    def create_session(self, username, password, os_type='Linux', os_version='Linux',
        screen_resolution='1920x1080', ip_address='127.0.0.1'):
        '''
        Create a user session by logging in with a valid username and password.
        '''
        params = {
            'username': username,
            'password': password,
            'appTypeID': '26',  # 26 is the default App Type
            'appVersion': '0.1',  # App version is 0.1
            'languageID': 'en_US',  # Default to English
            'osType': os_type,
            'osVersion': os_version,
            'scrRes': screen_resolution,
            'ipAddress': ip_address,
        }

        res = self.drive_wealth.userSessions.POST(data=json.dumps(params))
        session = create_object_from_json_response('Session', res)
        self.session_key = session.session_key
        self.user_id = session.user_id
        self.accounts = session.accounts

    def heartbeat(self):
        params = {
            'action': 'heartbeat',
        }
        res = self.drive_wealth.userSessions(self.session_key).PUT(params=params)
        res.raise_for_status()

    def logout(self):
        res = self.drive_wealth.userSessions(self.session_key).DELETE()
        res.raise_for_status()
