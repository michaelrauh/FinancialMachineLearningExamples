import data_cache
import static_data
import parser
from dateutil.rrule import DAILY, rrule, MO, TU, WE, TH, FR
import os
import pickle


class DataService:
    @staticmethod
    def __hash_arguments__(start_date, end_date):
        end_year = str(end_date.year)
        end_month = str(end_date.month - 1)
        end_day = str(end_date.day)
        start_year = str(start_date.year)
        start_month = str(start_date.month - 1)
        start_day = str(start_date.day)
        return 'data/' + 'whole_market' + end_year + end_month + end_day + start_year + start_month + start_day + '.p'

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
        started = False
        for day in self.date_range(self.start_date, self.end_date):
            date = day.date()
            if date not in set(clean.keys()):
                if not started:
                    clean[date] = [None for i in range(5)]
                else:
                    clean[date] = self.next_valid_price(clean, date)
            else:
                started = True
        return clean

    def load(self):
        path = self.__hash_arguments__(self.start_date, self.end_date)
        if not os.path.exists(path):
            print("load must clean all data.")
            for symbol in static_data.symbols()[0]:
                print("loading", symbol)
                raw = data_cache.fetch(symbol, self.start_date, self.end_date)
                print("there", len(raw))
                if raw is not None:
                    dirty = parser.parse(raw)
                    print("here", len(dirty))
                    clean = self.clean(dirty)
                    print("go", len(clean))
                    if self.valid(clean):
                        print("one", len(clean))
                        final = self.fill_in(clean)
                        print("this", len(final))
                        self.data_map[symbol] = final
                        print("that", len(self.data_map[symbol]))
                    else:
                        print("blacklisting", str(symbol))
            pickle.dump(self.data_map, open(path, 'wb'))
        else:
            print("fast load - loading whole market at once")
            self.data_map = pickle.load(open(path, 'rb'))

    def symbols(self):
        return list(self.data_map.keys())

    def next_valid_date(self, date):
        return self.date_range(date, self.end_date)[1]

    def round_from_weekend(self, date):
        return self.date_range(date, self.end_date)[0].date()