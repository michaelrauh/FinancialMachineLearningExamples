import datetime
import market as m
import portfolio as p
import broker as b
import account as a
import calendar as c


class Trader:

    def __init__(self, starting_money):
        self.market = m.Market()
        self.account = a.Account(starting_money)
        self.portfolio = p.Portfolio()
        self.broker = b.Broker()

    def top_x(self, x, start_date=datetime.date(1950, 1, 1), end_date=datetime.date.today()):
        for day in c.daterange(start_date, end_date):
            if self.market.open_on(day):
                year_ago = day - datetime.timedelta(days=365)
                top_today = self.market.get_top_x(x, year_ago, day)
                current_stocks = set(self.portfolio.symbols)
                desired_stocks = set([stock.symbol for stock in top_today])
                missing_stocks = desired_stocks.difference(current_stocks)
                extra_stocks = current_stocks.difference(desired_stocks)
                self.broker.sell(extra_stocks, self.account, self.portfolio, day)
                self.broker.buy_even_weight(missing_stocks, self.account, self.portfolio, day)

    def balance(self):
        return self.account.balance