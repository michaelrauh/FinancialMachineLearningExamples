import matplotlib.pyplot as plt
import os


def graph(balances, balance, horizon, x, start_sim, end_sim):
    plt.plot(balances)
    plt.title("x=" + str(x) + ", horizon=" + str(horizon) + ", balance=" + str(round(balance, 2)))
    plt.xlabel("number of days after Jan. 1, 2005")
    plt.ylabel("Portfolio value (USD)")
    os.makedirs('output', exist_ok=True)
    plt.savefig('output/' + str(start_sim) + "_" + str(end_sim) + "_" + str(x) + "_" + str(horizon) + '.png',
                bbox_inches='tight')
    plt.gcf().clear()