class Portfolio:
    def __init__(self):
        self.register = dict()
        self.events = dict()

    def quantity(self, stock):
        try:
            return self.register[stock]
        except KeyError:
            return 0

    def buy(self, stock, quantity):
        try:
            self.register[stock] += quantity
        except KeyError:
            self.register[stock] = quantity

    def buy_with_trigger(self, stock, quantity, event):
        self.buy(stock, quantity)
        self.events[stock] = event

    def sell(self, stock):
        del(self.register[stock])
        del(self.events[stock])

    def stocks(self):
        return list(self.register.keys())

    def try_all_events(self, date):
        iter_events = dict(self.events)
        for event in iter_events.values():
            event.fire_if_applicable(date)