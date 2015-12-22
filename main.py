import trader as t
import datetime as d
import grapher as g
from market import Market
import time

start_time = time.time()

START_ERA = d.date(2005, 1, 1)
END_ERA = d.date(2015, 10, 30)
START_SIM = d.date(2005, 1, 1)
END_SIM = d.date(2015, 10, 30)

Market.initialize(START_ERA, END_ERA)
traders = []

for portfolio_size in [2, 3, 5, 8]:
    for loss in [-.1, -.05]:
        for blacklist_duration in [30]:
            for strategy in ["vanilla", "stop_loss"]:
                traders.append(t.Trader(10000, strategy, portfolio_size, 365, loss, blacklist_duration))

for trader in traders:
    print(trader.portfolio_size, trader.loss, trader.blacklist_duration, trader.strategy)

balances = [[] for i in range(len(traders))]

while Market.date < END_SIM - d.timedelta(30):
    for trader, i in zip(traders, range(len(traders))):
        trader.trade()
        balances[i].append(trader.portfolio.value() + trader.account.balance)
    Market.tick()

for trader, i in zip(traders, range(len(traders))):
    g.graph(balances[i], trader.portfolio.value() + trader.account.balance, trader.horizon, trader.portfolio_size,
            START_SIM, END_SIM, trader.loss, trader.blacklist_duration, i, trader.strategy)

end_time = time.time()

print("total time elapsed:", (end_time - start_time)/60, "minutes")