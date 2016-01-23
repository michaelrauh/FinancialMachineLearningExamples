from market import Market
import trader
import datetime

# TODO: Create trader that holds for window time


class ShiftTrader(trader.Trader):

    @staticmethod
    def flatten(l):
        return [item for sublist in l for item in sublist]

    def __init__(self, starting_money, strategy, portfolio_size, horizon, tolerance, window, match_size, price_change=None, blacklist_duration=None):
        super().__init__(starting_money, strategy, portfolio_size, horizon, price_change, blacklist_duration)
        self.tolerance = tolerance
        self.window = window
        self.match_size = match_size

    def trade(self):
        today = Market.date
        time_ago = today - datetime.timedelta(self.horizon)
        top_stocks = Market.sort_by_performance(time_ago)[0:self.match_size]
        top_stocks = set([i for i in top_stocks if not self.blacklisted(i)])

        desired_stocks = []
        for stock in top_stocks:
            desired_stocks.append(Market.find_correlated_stocks(stock, self.window, self.horizon, self.tolerance, self.portfolio_size))

        self.optimize_even_weight(set(self.flatten(desired_stocks)))