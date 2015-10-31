import datetime


class Account:

    def __init__(self, balance):
        self.balance = balance

    def credit(self, value, date):
        try:
            self.balance += value
        except KeyError:
            self.balance = value

    def debit(self, value, date):
        self.balance -= value