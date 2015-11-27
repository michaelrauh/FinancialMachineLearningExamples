import event as e


class EventFactory:
    def __init__(self, broker):
        self.broker = broker

    def stop_loss(self, portfolio, account, stock, purchase_price, loss, blacklist_duration):

        def stop_loss_trigger(date):
            return ((stock.get_low_price(date) - purchase_price)/purchase_price) < loss

        def sell_stop_loss(date):
            open_price = stock.get_open_price(date)
            trigger_price = purchase_price + (purchase_price * loss)
            if open_price < trigger_price:
                price = open_price
            else:
                price = trigger_price * .99
            return self.broker.sell_stop_loss(portfolio, account, stock, price, date, blacklist_duration)

        return e.Event(stop_loss_trigger, sell_stop_loss)