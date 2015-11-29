import data_warehouse
import parser
from dateutil.rrule import DAILY, rrule, MO, TU, WE, TH, FR
import datetime


def date_range(start_date, end_date):
    return rrule(DAILY, dtstart=start_date, until=end_date, byweekday=(MO, TU, WE, TH, FR))


class Stock:

    def __init__(self, symbol, cap, ipo, sector, industry, start_date, end_date, validate):
        data = data_warehouse.fetch(symbol, start_date, end_date)
        if data is not None:
            self.symbol = symbol
            self.data = data
            self.price_map = parser.parse(self.data)
            self.clean()
            self.cap = cap
            self.ipo = ipo
            self.sector = sector
            self.industry = industry
            self.start_date = start_date
            self.end_date = end_date
            self.blacklist_date = datetime.date(1900, 1, 1)
            if validate and not self.valid(start_date, end_date):
                self.data = None
        else:
            self.data = None

    def clean(self):
        for date in list(self.price_map.keys()):
            if date in self.price_map:
                data = self.price_map[date]
                if data[0] == data[1] == data[2] == data[3]:
                    del(self.price_map[date])

    def valid(self, start_date, end_date):
        failures = 0
        started = False
        for day in date_range(start_date, end_date):
            date = day.date()
            if not started:
                if date in self.all_dates():
                    started = True
            else:
                if date in self.all_dates():
                    failures = 0
                else:
                    failures += 1
            if failures > 3:
                print("Invalid data found. Blacklisting", self.symbol)
                return False
        return True

    def get_open_price(self, date):
        return self.__fetch_data__(date, parser.DataOrder.opens)

    def get_high_price(self, date):
        return self.__fetch_data__(date, parser.DataOrder.highs)

    def get_low_price(self, date):
        return self.__fetch_data__(date, parser.DataOrder.lows)

    def get_close_price(self, date):
        return self.__fetch_data__(date, parser.DataOrder.closes)

    def get_volume(self, date):
        return self.__fetch_data__(date, parser.DataOrder.volumes)

    def get_open_price_backward(self, date):
        return self.__fetch_backward__(date, parser.DataOrder.opens)

    def get_high_price_backward(self, date):
        return self.__fetch_backward__(date, parser.DataOrder.highs)

    def get_low_price_backward(self, date):
        return self.__fetch_backward__(date, parser.DataOrder.lows)

    def get_close_price_backward(self, date):
        return self.__fetch_backward__(date, parser.DataOrder.closes)

    def get_volume_backward(self, date):
        return self.__fetch_backward__(date, parser.DataOrder.volumes)

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