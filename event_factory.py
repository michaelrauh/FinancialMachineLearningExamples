import event as e
from parser import DataOrder
from market import Market


class EventFactory:
    def __init__(self, broker):
        self.broker = broker

    def price_trigger(self, trader, portfolio, account, stock, purchase_price, loss, blacklist_duration, op):

        trigger_price = purchase_price + (purchase_price * loss)

        def price_change_trigger():
            if op(stock.current_price, trigger_price):
                print("price change triggered on", stock)
                return True
            else:
                return False

        def sell_price_trigger():
            if Market.time == DataOrder.open:
                price = stock.current_price
            else:
                price = trigger_price
            self.broker.sell_price_trigger(trader, portfolio, account, stock, Market.date, blacklist_duration, price)

        return e.Event(price_change_trigger, sell_price_trigger, trader.name, stock.symbol)