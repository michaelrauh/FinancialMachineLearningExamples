class Portfolio:
    def __init__(self):
        self.register = {}

    def quantity(self, symbol):
        try:
            return self.register[symbol]
        except KeyError:
            return 0

    def buy(self, symbol, quantity):
        try:
            self.register[symbol] += quantity
        except KeyError:
            self.register[symbol] = quantity

    def sell(self, symbol):
        del(self.register[symbol])

    def symbols(self):
        return list(self.register.keys())