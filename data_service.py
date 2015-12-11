import data_cache
import static_data
import parser
from dateutil.rrule import DAILY, rrule, MO, TU, WE, TH, FR


class DataService:

    @staticmethod
    def date_range(start_date, end_date):
        return rrule(DAILY, dtstart=start_date, until=end_date, byweekday=(MO, TU, WE, TH, FR))

    @staticmethod
    def clean(dirty):
        for date in list(dirty.keys()):
            if date in dirty:
                data = dirty[date]
                if data[0] == data[1] == data[2] == data[3]:
                    del(dirty[date])
        return dirty

    def valid(self, data):
        failures = 0
        started = False
        for day in self.date_range(self.start_date, self.end_date):
            date = day.date()
            if not started:
                if date in set(data.keys()):
                    started = True
            else:
                if date in set(data.keys()):
                    failures = 0
                else:
                    failures += 1
            if failures > 3:
                return False
        return True

    def next_valid_price(self, data, start_date):
        for day in self.date_range(start_date, self.end_date):
            date = day.date()
            if date in set(data.keys()):
                return data[date]

    def __init__(self, start_date, end_date):
        self.data_map = {}
        self.start_date = start_date
        self.end_date = end_date

    def fill_in(self, clean):
        final = dict()
        started = False
        for day in self.date_range(self.start_date, self.end_date):
            date = day.date()
            if date not in set(clean.keys()):
                if not started:
                    final[date] = [None for i in range(5)]
                else:
                    final[date] = self.next_valid_price(clean, date)
            else:
                started = True
        return final

    def load(self):
        for symbol in static_data.symbols():
            raw = data_cache.fetch(symbol, self.start_date, self.end_date)
            if raw is not None:
                dirty = parser.parse(raw)
                clean = self.clean(dirty)
                if self.valid(clean):
                    final = self.fill_in(clean)
                    self.data_map[symbol] = final