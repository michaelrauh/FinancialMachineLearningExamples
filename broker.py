import math
import event_factory as e
from event import Event
import operator


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

    def buy(self, strategy, budget, stock, account, portfolio, trader, price_change, blacklist_duration):
        self.strategy_mapping[strategy](self, budget, stock, account, portfolio, trader, price_change, blacklist_duration)

    def sell_price_trigger(self, trader, portfolio, account, stock, date, blacklist_duration, price):
        self.sell(trader, stock, account, portfolio, price)
        trader.blacklist(stock, blacklist_duration)

    def buy_price_trigger(self, budget, stock, account, portfolio, trader, price_change, blacklist_duration):
        purchase_price = stock.current_price
        if purchase_price < budget:
            op = operator.gt if price_change > 0 else operator.lt # If price change is negative stop loss else profit exit
            self.ef.price_trigger(trader, portfolio, account, stock, purchase_price, price_change, blacklist_duration, op)
            self.buy_vanilla(budget, stock, account, portfolio)

    def buy_vanilla(self, budget, stock, account, portfolio, trader=None, price_change=None, duration=None):
        price = stock.current_price
        quantity = math.floor(budget/price)
        if quantity > 0:
            purchase_price = (price * quantity) + self.fees
            account.debit(purchase_price)
            portfolio.buy(stock, quantity)
            print("buying", quantity, "shares of", stock, "at", purchase_price, "that's", price,
                  "per share")

    strategy_mapping = {'price_trigger': buy_price_trigger, 'vanilla': buy_vanilla}