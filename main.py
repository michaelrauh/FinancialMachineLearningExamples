import trader as t
import datetime as d
import matplotlib.pyplot as plt
import os

START_ERA = d.date(2005, 1, 1)
END_ERA = d.date(2015, 10, 30)
START_SIM = d.date(2005, 1, 1)
END_SIM = d.date(2015, 10, 30)

trader = t.Trader(1000000, START_ERA, END_ERA)

for x in [1,2,3,5,8,13,21,35,80,150,300,600]:
    for horizon in [1,2,3,5,8,13,21,35,80,150,300,600]:
        balances = []
        trader.reset()
        trader.top_x(x, START_SIM, END_SIM, horizon, balances)
        plt.plot(balances)
        os.makedirs('output', exist_ok=True)
        plt.savefig('output/' + str(START_SIM) + "_" + str(END_SIM) + "_" + str(x) + "_" + str(horizon) + '.png', bbox_inches='tight')
        # plt.show()
        plt.gcf().clear()
        print("x=", x, "horizon=", horizon, "balance=", (trader.balance()))