from pyspark.sql import SparkSession
from itertools import combinations

ss = SparkSession.builder.getOrCreate()
sc = ss.sparkContext

data = sc.textFile('Data/ub_sample_data.csv')

user_business = data.map(lambda line: line.split(',')) \
    .map(lambda line: (line[0], [line[1]])) \
    .reduceByKey(lambda a, b: a + b) \
    .mapValues(set) \
    .collect()

user_business = dict(user_business)

# check all users

all_users = user_business.keys()
E = dict()
for user_1, user_2 in combinations(all_users, 2):
    if len(user_business[user_1] & user_business[user_2]) >= 7:
        try:
            E[user_1].add(user_2)
        except:
            E[user_1] = {user_2}
        try:
            E[user_2].add(user_1)
        except:
            E[user_2] = {user_1}
print(E)

# E = {'A': {'B', "C"},
#      'B': {'A', 'C', 'D'},
#      'C': {'A', 'B'},
#      'D': {'B', 'G', 'F', 'E'},
#      'E': {'D', 'F'},
#      'F': {'E', 'D', 'G'},
#      'G': {'D', 'F'}}

parents = dict()
for key, value in E.items():
    for child in value:
        try:
            parents[child].add(key)
        except:
            parents[child] = {key}


# perform BFS

def bfs(graph, start_node, parents):
    # Example: '39FT2Ui8KUXwmUt6hnwy-g'
    bfs = []
    # stack = ['39FT2Ui8KUXwmUt6hnwy-g']
    visited = set()
    stack = [start_node]
    levels = {}
    i = 0
    while stack:
        for node in stack:
            levels['Level' + str(i)] = set(stack)
            visited.add(node)
        i += 1
        # collect their children that not be visited
        children = set()
        for node in stack:
            for child in graph[node]:
                if child not in visited:
                    children.add(child)
        stack = list(children)

    # for key, value in levels.items():
    #     print(key, value)

    # Based on Level, go from bottom to top

    last_level = i - 1
    total_level = last_level

    degree = dict()

    ## Init value for each node
    # degree['39FT2Ui8KUXwmUt6hnwy-g'] = 1
    # while last_level >= 1:
    #     nodes_this_level = levels['Level' + str(last_level)]
    #     for node in nodes_this_level:
    #         degree[node] = len(levels['Level' + str(last_level - 1)] & parents[node])
    #     last_level -= 1
    #
    # print(degree)
    #
    #
    betweenness = dict()
    #
    # last_level = i - 1
    # while last_level >= 1:
    #     nodes_this_level = levels['Level' + str(last_level)]

    # bottom level all 1

    for node in levels['Level' + str(last_level)]:
        degree[node] = 1

    credits = {start_node: 1}
    level = 1
    while level <= total_level:
        node_in_level = levels['Level' + str(level)]
        node_in_last_level = levels['Level' + str(level - 1)]
        for node in node_in_level:
            par = parents[node]
            over_lap = node_in_last_level & par
            for n in over_lap:
                try:
                    credits[node] += credits[n]
                except:
                    credits[node] = credits[n]
        level += 1

    # print(credits)

    last_level -= 1
    # print(last_level)
    while last_level >= 0:
        # print(last_level)
        node = levels['Level' + str(last_level)]
        for this_level_node in node:
            degree[this_level_node] = 1
            child = E[this_level_node]
            overlap = child & levels['Level' + str(last_level + 1)]
            for child in overlap:
                # How much?
                par = parents[child]
                # upper level
                upper_level = levels['Level' + str(last_level)]
                total_par = par & upper_level
                tot_credit = sum(credits[n] for n in total_par)
                # degree[this_level_node] += degree[child] / float(
                #     len(parents[child] & levels['Level' + str(last_level)]))
                degree[this_level_node] += degree[child] * (credits[this_level_node] / float(tot_credit))

                # try:
                #     betweenness[(max(this_level_node, child), min(this_level_node, child))] += degree[child] / float(
                #         len(parents[child] & levels['Level' + str(last_level)]))
                # except:
                #     betweenness[(max(this_level_node, child), min(this_level_node, child))] = degree[child] / float(
                #         len(parents[child] & levels['Level' + str(last_level)]))
                try:
                    betweenness[(max(this_level_node, child), min(this_level_node, child))] += degree[child] * (
                            credits[this_level_node] / float(tot_credit))
                except:
                    betweenness[(max(this_level_node, child), min(this_level_node, child))] = degree[child] * (
                            credits[this_level_node] / float(tot_credit))
        last_level -= 1

    return betweenness


all_between = {}

for node in E.keys():
    betweeness = bfs(E, node, parents)
    for key, value in betweeness.items():
        try:
            all_between[key] += value / 2.0
        except:
            all_between[key] = value / 2.0

# degree, betweenness = bfs(E, 'E', parents)

# print(degree)
# print(betweenness)

print(all_between)
