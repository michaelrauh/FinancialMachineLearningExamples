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
        return float(self.price_map[date][0])

    def get_high_price(self, date):
        return float(self.price_map[date][1])

    def get_low_price(self, date):
        return float(self.price_map[date][2])

    def get_close_price(self, date):
        return float(self.price_map[date][3])

    def get_volume(self, date):
        return int(self.price_map[date][4])

    def performance(self, start_date, end_date):
        start = self.get_price(start_date)
        end = self.get_price(end_date)
        if start is None or end is None:
            return 0
        return (end-start)/start

    def get_price(self, date, depth=0):
        if self.ipo is not None and date.year < self.ipo:
            return None
        if depth > 7:
            return None
        try:
            return self.get_open_price(date)
        except KeyError:
            tomorrow = date + datetime.timedelta(1)
            return self.get_price(tomorrow, depth + 1)

    def set_start_end(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date

    def performance_key(self):
        return self.performance(self.start_date, self.end_date)

    def __repr__(self):
        return self.symbol

    def all_dates(self):
        return set(self.price_map.keys())