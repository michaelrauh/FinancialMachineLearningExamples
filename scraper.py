import urllib.request
import datetime


def scrape(symbol, start_date, end_date):
    end_year = str(end_date.year)
    end_month = str(end_date.month - 1)
    end_day = str(end_date.day)
    start_year = str(start_date.year)
    start_month = str(start_date.month - 1)
    start_day = str(start_date.day)
    
    url = 'http://ichart.finance.yahoo.com/table.csv?s=' + symbol + '&d=' + end_month + '&e=' + end_day + '&f=' + \
          end_year + '&g=d&a=' + start_month + '&b=' + start_day + '&c=' + start_year + '&ignore=.csv'

    try:
        with urllib.request.urlopen(url) as f:
            return f.read().decode('utf-8')
    except urllib.error.URLError:
        return None
