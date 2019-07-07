import datetime

class DateTimeMock(datetime.datetime):
    _bogus_current_datetime = None

    @classmethod
    def set_now(cls, dt=None):
        cls._bogus_current_datetime = dt

    @classmethod
    def now(cls, tz=None):
        if cls._bogus_current_datetime is None:
            return datetime.datetime.now()
        else:
            return cls._bogus_current_datetime

    @classmethod
    def today(cls):
        if cls._bogus_current_datetime is None:
            return datetime.datetime.today()
        else:
            return cls._bogus_current_datetime

class DateMock(datetime.date):
    _bogus_current_date = None

    @classmethod
    def set_today(cls, d=None):
        cls._bogus_current_date = d

    @classmethod
    def today(cls):
        if cls._bogus_current_date is None:
            return datetime.date.today()
        else:
            return cls._bogus_current_date