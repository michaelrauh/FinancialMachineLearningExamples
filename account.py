class Account:

    def __init__(self, balance):
        self.balance = balance

    def credit(self, value):
        self.balance += value

    def debit(self, value):
        self.balance -= value