from .exceptions import InstrumentNotFoundError
from .schemas import create_object_from_json_response

from cachetools.func import ttl_cache
from hammock import Hammock as DriveWealth
from requests.exceptions import HTTPError

import json


class Api(object):
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
        self.api = DriveWealth(self.api_base_url, headers=headers)
        self._create_session(username, password)

        # Create api with the generated session
        headers['x-mysolomeo-session-key'] = self.session_key
        self.api = DriveWealth(self.api_base_url, headers=headers)

    def _create_session(self, username, password, os_type='Linux', os_version='Linux',
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

        res = self.api.userSessions.POST(data=json.dumps(params))
        session = create_object_from_json_response('Session', res)
        self.session_key = session.session_key
        self.user_id = session.user_id
        self.accounts = session.accounts

    def get_user(self, user_id):
        '''
        Provides details on a specific user.
        '''
        res = self.api.users(user_id).GET()
        return create_object_from_json_response('User', res)

    def heartbeat(self):
        params = {
            'action': 'heartbeat',
        }
        res = self.api.userSessions(self.session_key).PUT(params=params)
        res.raise_for_status()

    def logout(self):
        res = self.api.userSessions(self.session_key).DELETE()
        res.raise_for_status()

    @ttl_cache(maxsize=128, ttl=60*15, typed=True)
    def search_instruments(self, symbol=None, name=None, tag=None):
        '''
        Searches for a particular instrument by symbol, name, or tag.
        Returns a list of instruments.
        '''
        params = {
            'symbol': symbol,
            'name': name,
            'tag': tag,
        }
        res = self.api.instruments.GET(params=params)
        return create_object_from_json_response('Instrument', res, many=True)

    @ttl_cache(maxsize=128, ttl=60*15)
    def get_instrument(self, instrument_id):
        '''
        Gets a particular instrument by instrument id.
        Returns an instrument or 404 if not found.
        '''
        params = {
            'options': 'F',  # get the fundamental data
        }
        res = self.api.instruments(instrument_id).GET(params=params)

        try:
            return create_object_from_json_response('Instrument', res, many=False)
        except HTTPError, e:
            raise InstrumentNotFoundError(e, instrument_id)
