import bar


class Graph():
    def __init__(self, sector, symbol):
        self.sector = sector
        self.symbols = [symbol]
        self.bars = [bar.Bar(symbol)]