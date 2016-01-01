import account as a
import portfolio as p
import broker as b
from market import Market
import trader


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
        best_trader = Market.get_highest_performing_trader(self.horizon)
        desired_stocks = set(best_trader.current_stocks())
        self.strategy = best_trader.strategy
        self.price_change = best_trader.price_change
        self.blacklist_duration = best_trader.blacklist_duration
        self.banned_stocks = best_trader.banned_stocks
        self.optimize_even_weight(desired_stocks)