import pickle

class Stock:
    pass

f = open('data/raw_stocks.txt','rb')
stocks = pickle.load(f)

def get_all_dates(stocks):
    max_len = 0
    for stock in stocks:
        if len(stock.data) > max_len:
            max_len = len(stock.data)
            all_dates = list(reversed(stock.data[0:-1:6]))
    return all_dates

all_dates = get_all_dates(stocks)

all_clusters = []

def find_highs(stock):
    """find all 52 week highs for a stock if there is enough data"""
    high_dates = []
    try:
        FTW = 253 # fifty two weeks, with holidays
        dates = list(reversed(stock[0:-1:6]))
        dates.pop()
        highs = list(reversed(stock[2:-1:6]))
        highs.pop()
        for i in range(FTW,len(highs)):
            if max(highs[i-FTW:i-1]) < highs[i]:
                high_dates.append(dates[i])
    except:
        pass

    return high_dates

def elapsed_time(beginning, end, dates=all_dates):
    return dates.index(end) - dates.index(beginning)

def find_groups(highs, threshold):
    """given highs, find groups that agglomerate at a given threshold"""

    if len(highs) == 0:
        return []
    elif len(highs) == 1:
        return [highs]
    
    groups = []
    current_high = highs.pop()
    group = [current_high]

    while len(highs) > 0:
        next_high = highs.pop()
        if elapsed_time(current_high, next_high) <= threshold:
            group.append(next_high)
        else:
            groups.append(group)
            group = [next_high]
        current_high = next_high
        
    return groups

class Cluster:
    def __init__(self, group, stock):
        """make a cluster with default data"""
        self.beginning = find_earliest(group)
        self.end = find_latest(group)
        self.length = elapsed_time(beginning, end)
        self.size = len(group)
        self.delta_plus = find_delta_plus(group, stock, self.beginning)
        self.delta_minus = find_delta_minus(group, stock, self.beginning)
        self.high_buckets = [[1] for i in range (size)]
        self.symbols = [stock.symbol]
        self.cap_range_min = stock.cap
        self.cap_range_max = stock.cap
        self.sectors = [stock.sector]
        self.industries = [stock.industry]
    def merge_in(self, cluster):
        """make supercluster by merging clusters"""
        self.beginning = find_earliest([self.beginning, cluster.beginning])
        self.end = find_latest ([self.end, cluster.end])
        self.length = elapsed_time(self.beginning, self.end)
        self.size += cluster.size
        self.delta_plus = max(self.delta_plus, cluster.delta_plus)
        self.delta_minus = min(self.delta_minus, cluster.delta_minus)
        self.high_buckets = merge_high_buckets(self.high_buckets, cluster.high_buckets)
        self.symbols += cluster.symbols
        self.cap_range_min = min(self.cap_range_min, cluster.cap_range_min)
        self.cap_range_max = max(self.cap_range_max, cluster.cap_range_max)
        self.sectors += cluster.sectors
        self.industries += cluster.industries
    def graph(self):
        """graph deltas between buckets"""
        pass
    def __str__(self):
        """print all cluster data"""
        pass
    
##for stock in stocks:
##    groups = find_groups(stock, threshold)
##    for group in groups:
##        cluster = Cluster(group, stock)
##        all_clusters.append(cluster)
##        
##out = open(str(threshold) + '_size_clusters.txt', 'wb')
##pickle.dump(all_clusters, out)
