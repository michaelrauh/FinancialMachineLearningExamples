import pickle

f = open('raw_stocks.txt','rb')
stocks = pickle.load(f)

criteria = get_user_input()

class Cluster:
    def __init__(self, group, stock):
        self.dates = group
        self.beginning = group[0]
        self.end = group [-1]
        self.length = elapsed_time(beginning,end)
        self.size = len(group)
        self.price_map = make_price_map(group,stock)
        self.delta_plus = find_delta_plus(group, stock)
        self.delta_minus = find_delta_minus(group, stock)
        self.high_buckets = enumerate_highs(group)
    def merge_in(self,cluster):
        self.dates += cluster.dates
        self.beginning = find_earlier(self.beginning, cluster.beginning)
        self.end = find_later (self.end, cluster.end)
        self.length = elapsed_time(beginning,end)
        self.size += cluster.size
        self.price_map # merge maps
        self.delta_plus = max(self.delta_plus, cluster.delta_plus)
        self.delta_minus = min(self.delta_plus, cluster.delta_plus)
        self.high_buckets = merge_high_buckets(self.high_buckets, cluster.high_buckets)
        
for stock in stocks:
    groups = find_groups(stock)
    for group in groups:
        cluster = Cluster(group, stock)
        all_clusters.append(cluster)
        
out = open('clusters.txt', 'wb')
pickle.dump(all_clusters, out)
