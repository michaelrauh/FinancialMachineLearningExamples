import stock
import data_warehouse
import static_data

class Market:
    def __init__(self):
        static = static_data.Static_data()
        self.symbols = static.symbols()
