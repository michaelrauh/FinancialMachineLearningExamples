class Portfolio:
    def __init__(self):
        self.register = {}

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

    def sell(self, stock):
        del(self.register[stock])

    def stocks(self):
        return list(self.register.keys())