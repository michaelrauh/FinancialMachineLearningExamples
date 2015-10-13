import scraper
import datetime
import pickle
import os


def hash_arguments(symbol, start_date, end_date):
    end_year = str(end_date.year)
    end_month = str(end_date.month - 1)
    end_day = str(end_date.day)
    start_year = str(start_date.year)
    start_month = str(start_date.month - 1)
    start_day = str(start_date.day)
    return 'data/' + symbol + end_year + end_month + end_day + start_year + start_month + start_day + '.p'


def fetch(symbol, start_date=datetime.date(1950, 1, 1), end_date=datetime.date.today()):
    print("fetching " + symbol)
    path = hash_arguments(symbol, start_date, end_date)
    if not os.path.exists(path):
        data = scraper.scrape(symbol, start_date, end_date)
        pickle.dump(data, open(path, 'wb'))
    else:
        data = pickle.load(open(path, 'rb'))
    if data is not None:
        rows = data.split('\n')
        rows.pop()
        rows.pop(0)
        data = ','.join(rows).split(',')
    else:
        print(symbol + " is garbage")
    return data