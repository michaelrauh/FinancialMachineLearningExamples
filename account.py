import datetime


class Account:

    def __init__(self, balance):
        self.balance = balance
        self.unsettled_funds = {}

    def settle_funds(self, date):
        for key in list(self.unsettled_funds.keys()):
            if key + datetime.timedelta(5) >= date:
                self.balance += self.unsettled_funds[key]
                del(self.unsettled_funds[key])

    def credit(self, value, date):
        try:
            self.unsettled_funds[date] += value
        except KeyError:
            self.unsettled_funds[date] = value
        self.settle_funds(date)

    def debit(self, value, date):
        self.settle_funds(date)
        self.balance -= value