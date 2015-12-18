import event as e


class EventFactory:
    def __init__(self, broker):
        self.broker = broker

    def stop_loss(self, market, portfolio, account, stock, purchase_price, loss, blacklist_duration):

        def stop_loss_trigger():
            trigger_price = purchase_price + (purchase_price * loss)
            if stock.current_price < trigger_price:
                print("stop loss triggered on", stock, stock.current_price, "is less than", trigger_price)
                return True
            else:
                return False

        def sell_stop_loss():
            self.broker.sell_stop_loss(portfolio, account, stock, market.date, blacklist_duration)

        return e.Event(stop_loss_trigger, sell_stop_loss)