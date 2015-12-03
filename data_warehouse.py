import scraper
import pickle
import os


class DataWarehouse:

    @staticmethod
    def hash_arguments(symbol, start_date, end_date):
        end_year = str(end_date.year)
        end_month = str(end_date.month - 1)
        end_day = str(end_date.day)
        start_year = str(start_date.year)
        start_month = str(start_date.month - 1)
        start_day = str(start_date.day)
        return 'data/' + symbol + end_year + end_month + end_day + start_year + start_month + start_day + '.p'

    def fetch(self, symbol, start_date, end_date):
        path = self.hash_arguments(symbol, start_date, end_date)
        if not os.path.exists(path):
            print("fetching", symbol, "from internet. Slow.")
            data = scraper.scrape(symbol, start_date, end_date)
            pickle.dump(data, open(path, 'wb'))
        else:
            data = pickle.load(open(path, 'rb'))
        if data is not None:
            rows = data.split('\n')
            rows.pop()
            rows.pop(0)
            data = ','.join(rows).split(',')
        return data

    def next_data_point(self):
        pass

    def next_time_point(self, time):
        pass