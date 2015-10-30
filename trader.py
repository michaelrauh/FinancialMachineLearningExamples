import datetime
import market as m
import portfolio as p
import broker as b
import account as a
import calendar as c


def top_x(x, start_date=datetime.date(1950, 1, 1), end_date=datetime.date.today()):
    market = m.Market()
    account = a.Account(10000)
    portfolio = p.Portfolio()
    broker = b.Broker()
    for day in c.daterange(start_date, end_date):
        if market.open_on(day):
            year_ago = day - datetime.timedelta(days=365)
            top_today = market.get_top_x(x, year_ago, day)
            current_stocks = set(portfolio.symbols)
            desired_stocks = set([stock.symbol for stock in top_today])
            missing_stocks = desired_stocks.difference(current_stocks)
            extra_stocks = current_stocks.difference(desired_stocks)
            broker.sell(extra_stocks, account, portfolio, day)
            broker.buy_even_weight(missing_stocks, account, portfolio, day)