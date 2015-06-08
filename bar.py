class Bar():
    def __init__(self):
        self.contents = []

    def add(self, symbol):
        self.contents.append(symbol)

    def size(self):
        return len(self.contents)

    def __str__(self):
        print self.size()