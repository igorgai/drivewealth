class InstrumentNotFoundError(Exception):
    def __init__(self, exception, instrument_id):
        super(InstrumentNotFoundError, self).__init__(exception)

        self.instrument_id = instrument_id
