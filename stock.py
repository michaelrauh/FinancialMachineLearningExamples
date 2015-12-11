import data_cache
import parser
from dateutil.rrule import DAILY, rrule, MO, TU, WE, TH, FR
import datetime


def date_range(start_date, end_date):
    return rrule(DAILY, dtstart=start_date, until=end_date, byweekday=(MO, TU, WE, TH, FR))


class Stock:

    def __init__(self, symbol, cap, ipo, sector, industry, start_date, end_date):
        self.symbol = symbol
        self.cap = cap
        self.ipo = ipo
        self.sector = sector
        self.industry = industry
        self.start_date = start_date
        self.end_date = end_date
        self.blacklist_date = datetime.date(1900, 1, 1)
        self.price_history = []

    def push_price(self, tick):
        self.price_history.push(tick)

    def current_price(self):
        return self.price_history[0]

    def get_open_price(self, date):
        return self.__fetch_data__(date, parser.DataOrder.open)

    def get_high_price(self, date):
        return self.__fetch_data__(date, parser.DataOrder.high)

    def get_low_price(self, date):
        return self.__fetch_data__(date, parser.DataOrder.low)

    def get_close_price(self, date):
        return self.__fetch_data__(date, parser.DataOrder.close)

    def get_volume(self, date):
        return self.__fetch_data__(date, parser.DataOrder.volume)

    def get_open_price_backward(self, date):
        return self.__fetch_backward__(date, parser.DataOrder.open)

    def get_high_price_backward(self, date):
        return self.__fetch_backward__(date, parser.DataOrder.high)

    def get_low_price_backward(self, date):
        return self.__fetch_backward__(date, parser.DataOrder.low)

    def get_close_price_backward(self, date):
        return self.__fetch_backward__(date, parser.DataOrder.close)

    def get_volume_backward(self, date):
        return self.__fetch_backward__(date, parser.DataOrder.volume)

    def performance(self, start_date, end_date):
        start = self.get_low_price_backward(start_date)
        end = self.get_high_price_backward(end_date - datetime.timedelta(1))
        if start is None or end is None:
            return 0
        return (end-start)/start

    def __fetch_data__(self, date, member, depth=0):
        if self.ipo is not None and date.year < self.ipo:
            return None
        if depth > 7:
            return None
        try:
            return float(self.price_map[date][member.value])
        except KeyError:
            tomorrow = date + datetime.timedelta(1)
            return self.__fetch_data__(tomorrow, member, depth + 1)

    def __fetch_backward__(self, date, member, depth=0):
        if self.ipo is not None and date.year < self.ipo:
            return None
        if depth > 7:
            return None
        try:
            return float(self.price_map[date][member.value])
        except KeyError:
            yesterday = date - datetime.timedelta(1)
            return self.__fetch_data__(yesterday, member, depth + 1)

    def set_start_end(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date

    def performance_key(self):
        return self.performance(self.start_date, self.end_date)

    def __repr__(self):
        return self.symbol

    def all_dates(self):
        return set(self.price_map.keys())

    def blacklist(self, date, duration):
        self.blacklist_date = date + datetime.timedelta(duration)

    def blacklisted(self, date):
        return date < self.blacklist_date