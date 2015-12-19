import trader as t
import datetime as d
import grapher as g
import market as m

START_ERA = d.date(2005, 1, 1)
END_ERA = d.date(2015, 10, 30)
START_SIM = d.date(2005, 1, 1)
END_SIM = d.date(2015, 10, 30)

market = m.Market(START_ERA, END_ERA)
portfolio_size = 3
horizon = 365
loss = -.1
blacklist_duration = 30
current_date = START_SIM
traders = [t.Trader(10000, market, "vanilla", portfolio_size, horizon, loss, blacklist_duration),
           t.Trader(10000, market, "stop_loss", portfolio_size, horizon, loss, blacklist_duration)]
balances = [[] for i in range(len(traders))]

while current_date < END_SIM - d.timedelta(30):
    for trader, i in zip(traders, range(len(traders))):
        trader.trade()
        balances[i].append(trader.portfolio.value() + trader.account.balance)
    market.tick()
    current_date = market.date

for trader, i in zip(traders, range(len(traders))):
    g.graph(balances[i], trader.portfolio.value() + trader.account.balance, horizon, portfolio_size, START_SIM, END_SIM, loss,
        blacklist_duration, i)