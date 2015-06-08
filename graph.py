import bar


class Graph():
    def __init__(self, sector):
        self.sector = sector
        self.symbols = []
        self.bars = dict()

    def add(self, symbol, current_high):
        if current_high not in self.bars:
            self.bars[current_high] = bar.Bar()
        self.bars[current_high].add(symbol)

    def __str__(self):
        for current_bar in self.bars:
            print current_bar