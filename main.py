import datetime as d
import time

import trader as t
import grapher as g
from market import Market
from parser import DataOrder
import strategy_thief as s


start_time = time.time()

START_ERA = d.date(2005, 1, 1)
END_ERA = d.date(2015, 10, 30)
START_SIM = d.date(2005, 1, 1)
END_SIM = d.date(2015, 10, 30)

Market.initialize(START_ERA, END_ERA)
traders = []

for portfolio_size in [2, 3, 5, 8]:
    for price_change in [-.05, -.1, .05, .1, .2]:
        for blacklist_duration in [30]:
                traders.append(t.Trader(10000, "price_trigger", portfolio_size, 365, price_change, blacklist_duration))

for portfolio_size in [2, 3, 5, 8]:
    traders.append(t.Trader(10000, "vanilla", portfolio_size, 365))

for horizon in [1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 150, 270, 365]:
    traders.append(s.StrategyThief(10000, horizon))

Market.traders = traders

while Market.date < END_SIM - d.timedelta(30):
    if Market.time in [DataOrder.open, DataOrder.close]:
        for trader, i in zip(traders, range(len(traders))):
            trader.trade()
    Market.tick()

balances = [trader.all_net_worths for trader in traders]
for trader, i in zip(traders, range(len(traders))):
    g.graph(balances[i], trader.portfolio.value() + trader.account.balance, trader.horizon, trader.portfolio_size,
            START_SIM, END_SIM, trader.price_change, trader.blacklist_duration, trader.strategy)

end_time = time.time()

print("total time elapsed:", (end_time - start_time)/60, "minutes")