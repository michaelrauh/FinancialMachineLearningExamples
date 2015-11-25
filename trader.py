import datetime
import market as m
import portfolio as p
import broker as b
import account as a
from dateutil.rrule import DAILY, rrule, MO, TU, WE, TH, FR


class Trader:

    def __init__(self, starting_money, start_date, end_date):
        self.starting_money = starting_money
        self.market = m.Market(start_date, end_date)
        self.account = a.Account(starting_money)
        self.portfolio = p.Portfolio()
        self.broker = b.Broker(self.market)

    def reset(self):
        self.account = a.Account(self.starting_money)
        self.portfolio = p.Portfolio()

    @staticmethod
    def date_range(start_date, end_date):
        return rrule(DAILY, dtstart=start_date, until=end_date, byweekday=(MO, TU, WE, TH, FR))

    def top_x(self, x, start_date, end_date, horizon, balances):
        for day in self.date_range(start_date, end_date - datetime.timedelta(30)):
            day = day.date()
            if self.market.open_on(day):
                time_ago = day - datetime.timedelta(days=horizon)
                desired_stocks = set(self.market.get_top_x(x, time_ago, day))
                current_stocks = set(self.portfolio.stocks())
                missing_stocks = desired_stocks.difference(current_stocks)
                extra_stocks = current_stocks.difference(desired_stocks)
                self.broker.sell(extra_stocks, self.account, self.portfolio, day)
                balances.append(self.net_worth(day))
                self.broker.buy_even_weight(missing_stocks, self.account, self.portfolio, day)
        self.broker.sell(self.portfolio.stocks(), self.account, self.portfolio, (end_date - datetime.timedelta(30)))

    def balance(self):
        return self.account.balance

    def net_worth(self, today):
        worth = 0
        for stock in self.portfolio.stocks():
            q = self.portfolio.quantity(stock)
            price = stock.get_open_price(today)
            worth += q * price
        return worth + self.account.balance