import event as e
from parser import DataOrder


class EventFactory:
    def __init__(self, broker):
        self.broker = broker

    def stop_loss(self, market, portfolio, account, stock, purchase_price, loss, blacklist_duration):

        def stop_loss_trigger():
            return ((stock.current_price - purchase_price)/purchase_price) < loss

        def sell_stop_loss():
            if market.time == DataOrder.open:
                price = stock.current_price
            else:
                price = purchase_price + (purchase_price * loss)
            self.broker.sell_stop_loss(portfolio, account, stock, price, market.date, blacklist_duration)

        return e.Event(stop_loss_trigger, sell_stop_loss)