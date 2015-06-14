# import user_input
# import loader
# import hasher
# import rule_engine
#
# pickle.load(hashes)
#
# rules = user_input.get_rules()
# graphs = loader.load_todays_graphs()
#
# response = []
# for graph in graphs:
#     similars = hashes[hasher.hash(graph)]
#     for similar in similars:
#         response.push(rule_engine.run_rules(rules, similar))
#
# print response
#
