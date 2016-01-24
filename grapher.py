import os

import matplotlib.pyplot as plt


def graph(name, balances, balance, horizon, x, start_sim, end_sim, price_change, blacklist_duration, strategy):
    plt.plot(balances)
    plt.title(str(name))
    plt.xlabel("number of ticks after Jan. 1, 2005")
    plt.ylabel("Portfolio value (USD)")
    os.makedirs('output', exist_ok=True)
    plt.savefig('output/' + str(round(balance, 2)) + str(start_sim) + "_" + str(end_sim) + "_" + str(x) + "_" +
                str(horizon) + "_" + str(price_change) + "_" + str(blacklist_duration) + "_" + strategy
                + '.png', bbox_inches='tight')
    plt.gcf().clear()