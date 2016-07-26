import os

import matplotlib.pyplot as plt


def graph(balances, balance, horizon, x, start_sim, end_sim, price_change, blacklist_duration, i, strategy):
    plt.plot(balances)
    plt.title("x=" + str(x) + ", horizon=" + str(horizon) + ", balance=" + str(round(balance, 2)) + " stop at " +
              str(price_change) + " " + "duration " + str(blacklist_duration) + " " + str(i) + " " + strategy)
    plt.xlabel("number of ticks after Jan. 1, 2005")
    plt.ylabel("Portfolio value (USD)")
    os.makedirs('output', exist_ok=True)
    plt.savefig('output/' + str(round(balance, 2)) + str(start_sim) + "_" + str(end_sim) + "_" + str(x) + "_" +
                str(horizon) + "_" + str(price_change) + "_" + str(blacklist_duration) + "_" + str(i) + "_" + strategy
                + '.png', bbox_inches='tight')
    plt.gcf().clear()