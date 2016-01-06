import datetime
import time

import trader
import grapher
from market import Market
from parser import DataOrder
import strategy_thief

START_TIME = time.time()
START_ERA = datetime.date(2005, 1, 1)
END_ERA = datetime.date(2015, 10, 30)
START_SIM = datetime.date(2005, 1, 1)
END_SIM = datetime.date(2015, 10, 30)

Market.initialize(START_ERA, END_ERA)
 
for portfolio_size in [2, 3, 5, 8]:
    for sell_point in [-.05, -.1, .05, .1, .2]:
        for blacklist_duration_days in [30]:
                Market.traders.append(trader.Trader(10000, "price_trigger", portfolio_size, 365, sell_point, blacklist_duration_days))

for portfolio_size in [2, 3, 5, 8]:
    Market.traders.append(trader.Trader(10000, "vanilla", portfolio_size, 365))

for horizon_days in [365]:
    Market.traders.append(strategy_thief.StrategyThief(10000, horizon_days))

while Market.date < END_SIM - datetime.timedelta(30):
    if Market.time in [DataOrder.open, DataOrder.close]:
        for trader in Market.traders:
            trader.trade()
    Market.tick()

for trader in Market.traders:
    grapher.graph(trader.all_net_worths, trader.portfolio.value() + trader.account.balance, trader.horizon, trader.portfolio_size, START_SIM, END_SIM, trader.price_change, trader.blacklist_duration, trader.strategy)

END_TIME = time.time()
minutes, seconds = divmod(END_TIME-START_TIME, 60)
print("total time elapsed: ", minutes, "m", seconds, "s")