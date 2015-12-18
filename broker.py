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
        print("selling", quantity, "shares of", stock, "at", value, "that's", price, "per share")

    def buy(self, budget, stock, account, portfolio):
        price = stock.current_price
        quantity = math.floor(budget/price)
        if quantity > 0:
            purchase_price = (price * quantity) + self.fees
            account.debit(purchase_price)
            portfolio.buy(stock, quantity)
            print("buying", quantity, "shares of", stock, "at", purchase_price, "that's", price,
                  "per share")

    def sell_stop_loss(self, portfolio, account, stock, date, blacklist_duration):
        self.sell(stock, account, portfolio)
        stock.blacklist(date, blacklist_duration)
        self.market.delete_event(stock)

    def buy_stop_loss(self, budget, portfolio, account, stock, loss, blacklist_duration):
        stop_loss = self.ef.stop_loss(self.market, portfolio, account, stock, budget, loss, blacklist_duration)
        self.market.register_event(stock, stop_loss)
        self.buy(budget, stock, account, portfolio)