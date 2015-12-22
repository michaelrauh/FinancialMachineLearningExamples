import math
import event_factory as e
from event import Event
from market import Market


class Broker:

    def __init__(self):
        self.fees = 9
        self.ef = e.EventFactory(self)

    def sell(self, trader, stock, account, portfolio, price=None):
        if price is None:
            price = stock.current_price
        quantity = portfolio.quantity(stock)
        value = price * quantity
        value -= self.fees
        portfolio.sell(stock)
        account.credit(value)
        Event.delete_trigger(trader.name, stock.symbol)
        print("selling", quantity, "shares of", stock, "at", value, "that's", price, "per share")

    def buy(self, strategy, budget, stock, account, portfolio, trader, loss, blacklist_duration):
        self.strategy_mapping[strategy](self, budget, stock, account, portfolio, trader, loss, blacklist_duration)

    def sell_stop_loss(self, trader, portfolio, account, stock, date, blacklist_duration, price):
        self.sell(trader, stock, account, portfolio, price)
        trader.blacklist(stock, blacklist_duration)

    def buy_stop_loss(self, budget, stock, account, portfolio, trader, loss, blacklist_duration):
        purchase_price = stock.current_price
        if purchase_price < budget:
            self.ef.stop_loss(trader, portfolio, account, stock, purchase_price, loss, blacklist_duration)
            self.buy_vanilla(budget, stock, account, portfolio)

    def buy_vanilla(self, budget, stock, account, portfolio, trader=None, loss=None, duration=None):
        price = stock.current_price
        quantity = math.floor(budget/price)
        if quantity > 0:
            purchase_price = (price * quantity) + self.fees
            account.debit(purchase_price)
            portfolio.buy(stock, quantity)
            print("buying", quantity, "shares of", stock, "at", purchase_price, "that's", price,
                  "per share")

    strategy_mapping = {'stop_loss': buy_stop_loss, 'vanilla': buy_vanilla}