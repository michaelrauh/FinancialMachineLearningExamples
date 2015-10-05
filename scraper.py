import urllib.request
import datetime


def scrape(symbol, start_time=datetime.date(1950, 1, 1), end_time=datetime.date.today()):
    end_year = str(end_time.year)
    end_month = str(end_time.month - 1)
    end_day = str(end_time.day)
    start_year = str(start_time.year)
    start_month = str(start_time.month - 1)
    start_day = str(start_time.day)
    
    url = 'http://ichart.finance.yahoo.com/table.csv?s=' + symbol + '&d=' + end_month + '&e=' + end_day + '&f=' + \
          end_year + '&g=d&a=' + start_month + '&b=' + start_day + '&c=' + start_year + '&ignore=.csv'

    with urllib.request.urlopen(url) as f:
        return f.read().decode('utf-8')
