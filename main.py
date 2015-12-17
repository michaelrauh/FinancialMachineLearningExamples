import trader as t
import datetime as d
import grapher as g
import market as m

START_ERA = d.date(2005, 1, 1)
END_ERA = d.date(2015, 10, 30)
START_SIM = d.date(2005, 1, 1)
END_SIM = d.date(2015, 10, 30)

market = m.Market(START_ERA, END_ERA)
x = 3
horizon = 365
loss = -.1
blacklist_duration = 30
current_date = START_SIM
trader = t.Trader(1000000, market)
balances = []

while current_date < END_SIM:
    trader.top_x(x, horizon, loss, blacklist_duration)
    balances.append(trader.portfolio.value() + trader.account.balance)
    market.tick()
    current_date = market.date

g.graph(balances, trader.portfolio.value() + trader.account.balance, horizon, x, START_SIM, END_SIM, loss,
        blacklist_duration)