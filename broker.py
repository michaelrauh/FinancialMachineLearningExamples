import math
import event_factory as e


class Broker:

    def __init__(self, market):
        self.fees = 9
        self.market = market
        self.ef = e.EventFactory(self)

    def sell(self, stock, account, portfolio):
        price = stock.current_price
        quantity = portfolio.quantity(stock)
        value = price * quantity
        value -= self.fees
        portfolio.sell(stock)
        account.credit(value)
        self.market.delete_event(stock)
        print("selling", quantity, "shares of", stock, "at", value, "that's", price, "per share")

    def buy(self, strategy, budget, stock, account, portfolio, loss, blacklist_duration):
        self.strategy_mapping[strategy](self, budget, stock, account, portfolio, loss, blacklist_duration)

    def sell_stop_loss(self, portfolio, account, stock, date, blacklist_duration):
        self.sell(stock, account, portfolio)
        stock.blacklist(date, blacklist_duration)

    def buy_stop_loss(self, budget, stock, account, portfolio, loss, blacklist_duration):
        purchase_price = stock.current_price
        if purchase_price < budget:
            stop_loss = self.ef.stop_loss(self.market, portfolio, account, stock, purchase_price, loss, blacklist_duration)
            self.market.register_event(stock, stop_loss)
            self.buy_vanilla(budget, stock, account, portfolio)

    def buy_vanilla(self, budget, stock, account, portfolio, loss=None, duration=None):
        price = stock.current_price
        quantity = math.floor(budget/price)
        if quantity > 0:
            purchase_price = (price * quantity) + self.fees
            account.debit(purchase_price)
            portfolio.buy(stock, quantity)
            print("buying", quantity, "shares of", stock, "at", purchase_price, "that's", price,
                  "per share")

    strategy_mapping = {'stop_loss': buy_stop_loss, 'vanilla': buy_vanilla}