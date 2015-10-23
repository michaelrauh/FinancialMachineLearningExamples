import market as m
import portfolio as p
import broker as b
import account as a
import calendar


def top_x(x):
    market = m.Market()
    account = a.Account()
    portfolio = p.Portfolio()
    broker = b.Broker(account, portfolio)
    for day in calendar.week_days_over_range:
        if market.open_on(day):
            year_ago = day - year
            top_today = market.get_top_x(x, year_ago, day)
            current_stocks = set(portfolio.symbols)
            desired_stocks = set([stock.symbol for stock in top_today])
            missing_stocks = desired_stocks.difference(current_stocks)
            extra_stocks = current_stocks.difference(desired_stocks)
            broker.sell(extra_stocks)
            broker.buy_even_weight(missing_stocks) # consider cap weighted, or risk weighted