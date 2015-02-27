import pickle

f = open('raw_stocks.txt','rb')
stocks = pickle.load(f)

all_clusters = []

def find_highs(stock):
    """find all 52 week highs for a stock"""

def find_groups(highs, threshold):
    """given a stock, find groups that agglomerate at a given threshold"""

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
    def __str__(self):
    """print all cluster data"""
        
for stock in stocks:
    groups = find_groups(stock, threshold)
    for group in groups:
        cluster = Cluster(group, stock)
        all_clusters.append(cluster)
        
out = open(str(threshold) + '_size_clusters.txt', 'wb')
pickle.dump(all_clusters, out)
