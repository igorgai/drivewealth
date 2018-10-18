from ..exceptions import InstrumentNotFoundError
from ..schemas import create_object_from_json_response

from cachetools.func import ttl_cache
from requests.exceptions import HTTPError


class InstrumentApiMixin:
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
        res = self.drive_wealth.instruments.GET(params=params)
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
        res = self.drive_wealth.instruments(instrument_id).GET(params=params)

        try:
            return create_object_from_json_response('Instrument', res, many=False)
        except HTTPError as e:
            raise InstrumentNotFoundError(e, instrument_id)
