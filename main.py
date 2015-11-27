import trader as t
import datetime as d
import grapher as g

START_ERA = d.date(2005, 1, 1)
END_ERA = d.date(2015, 10, 30)
START_SIM = d.date(2005, 1, 1)
END_SIM = d.date(2015, 10, 30)

trader = t.Trader(1000000, START_ERA, END_ERA)

for x in [1, 2, 3, 5, 8, 13, 21, 34, 55]:
    for horizon in [1, 30, 90, 180, 270, 365]:
        for loss in [-.01, -.05, -.1, -.15, -.2]:
            for blacklist_duration in [30, 60, 90, 365, 3650]:
                balances = []
                trader.reset()
                trader.top_x(x, START_SIM, END_SIM, horizon, balances, loss, blacklist_duration)
                g.graph(balances, trader.balance(), horizon, x, START_SIM, END_SIM, loss, blacklist_duration)
                print("x=", x, "horizon=", horizon, "balance=", (trader.balance()))