"""Init will go by day and sweep through, building each graph in batch"""

all_stocks = pull_all_stocks()

for day in all_days:
    for graph in graph_types:
        graph.create()