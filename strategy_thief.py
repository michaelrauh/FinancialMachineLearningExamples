import account as a
import portfolio as p
import broker as b
from market import Market
import trader
import datetime


class StrategyThief(trader.Trader):

    def __init__(self, starting_money, horizon):
        self.starting_money = starting_money
        self.account = a.Account(starting_money)
        self.portfolio = p.Portfolio()
        self.broker = b.Broker()
        self.horizon = horizon
        self.name = hash(self)
        self.all_net_worths = list()
        self.price_change = None
        self.blacklist_duration = None
        self.portfolio_size = None

    def trade(self):
        if Market.date > Market.start + datetime.timedelta(365 * 2):
            best_traders = Market.sort_traders_by_performance(self.horizon)
            if len(best_traders) > 0:
                best_trader = best_traders[0]
                desired_stocks = set(best_trader.current_stocks())
                self.strategy = best_trader.strategy
                self.price_change = best_trader.price_change
                self.blacklist_duration = best_trader.blacklist_duration
                self.banned_stocks = best_trader.banned_stocks
                self.optimize_even_weight(desired_stocks)