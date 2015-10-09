import data_warehouse
import datetime


class Stock:

    def __init__(self, symbol, cap, ipo, sector, industry, start_date=datetime.date(1950, 1, 1), end_date=datetime.date.today()):
        self.data = data_warehouse.fetch(symbol, start_date, end_date)
        self.cap = cap
        self.ipo = ipo
        self.sector = sector
        self.industry = industry