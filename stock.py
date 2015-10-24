import data_warehouse
import datetime
import util


class Stock:

    def __init__(self, symbol, cap, ipo, sector, industry, start_date=datetime.date(1950, 1, 1), end_date=datetime.date.today()):
        data = data_warehouse.fetch(symbol, start_date, end_date)
        if data is not None:
            self.symbol = symbol
            self.data = data
            self.price_map = util.parse(self.data)
            self.cap = cap
            self.ipo = ipo
            self.sector = sector
            self.industry = industry
            self.start_date = start_date
            self.end_date = end_date
        else:
            self.data = None

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
        try:
            start = self.get_open_price(start_date)
            end = self.get_open_price(end_date)
            return (end-start)/start
        except KeyError:
            return 0

    def set_start_end(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date

    def performance_key(self):
        if self.data is not None:
            return self.performance(self.start_date, self.end_date)
        else:
            return -1

    def __repr__(self):
        return self.symbol

    def all_dates(self):
        return set(self.price_map.keys())