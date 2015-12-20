import event as e
from parser import DataOrder


class EventFactory:
    def __init__(self, broker):
        self.broker = broker

    def stop_loss(self, market, portfolio, account, stock, purchase_price, loss, blacklist_duration):

        trigger_price = purchase_price + (purchase_price * loss)

        def stop_loss_trigger():
            if stock.current_price < trigger_price:
                print("stop loss triggered on", stock)
                return True
            else:
                return False

        def sell_stop_loss():
            if market.time == DataOrder.open:
                price = stock.current_price
            else:
                price = trigger_price
            self.broker.sell_stop_loss(portfolio, account, stock, market.date, blacklist_duration, price)

        return e.Event(stop_loss_trigger, sell_stop_loss)