import urllib.request

class Scraper:

    def scrape(self, symbol, start_year = 1950, end_year = 2015):
        url = 'http://ichart.finance.yahoo.com/table.csv?s=' + symbol + '&d=12&e=31&f=' + \
              str(end_year) + '&g=d&a=1&b=00&c=' + str(start_year) + '&ignore=.csv'

        with urllib.request.urlopen(url) as f:
            return (f.read().decode('utf-8'))
