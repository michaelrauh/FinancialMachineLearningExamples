import time
import datetime


def get_column(index, data):
    return list(reversed(data[index::7]))


def parse_date(raw_date):
    date = time.strptime(raw_date, "%Y-%m-%d")
    return datetime.date(date.tm_year, date.tm_mon, date.tm_mday)


def parse_dates(raw_dates):
    return [parse_date(raw_date) for raw_date in raw_dates]


def parse(data):
    price_map = {}
    raw_dates = get_column(0, data)
    dates = parse_dates(raw_dates)
    opens = get_column(1, data)
    highs = get_column(2, data)
    lows = get_column(3, data)
    closes = get_column(4, data)
    volumes = get_column(5, data)
    for i in range(len(dates)):
        price_map[dates[i]] = (opens[i], highs[i], lows[i], closes[i], volumes[i])
    return price_map
