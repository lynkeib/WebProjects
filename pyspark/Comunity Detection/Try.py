from pyspark.sql import SparkSession
from itertools import combinations
import Helper as H

import os

os.environ['PYSPARK_PYTHON'] = '/anaconda3/envs/py36/bin/python3.6'
os.environ['PYSPARK_DRIVER_PYTHON'] = '/anaconda3/envs/py36/bin/python3.6'

ss = SparkSession.builder.getOrCreate()

sc = ss.sparkContext

path = 'Data/ub_sample_data.csv'

threshold = 7

graphRDD = sc.textFile(path)

header = graphRDD.first()

graphRDD = graphRDD.filter(lambda line: line != header) \
    .map(lambda line: line.split(',')) \
    .map(lambda line: (line[0], [line[1]])) \
    .reduceByKey(lambda a, b: a + b)

graph_dic = dict(graphRDD.mapValues(set).collect())

all_users = graph_dic.keys()

all_users_len = len(all_users)

res = []

for comb in combinations(all_users, 2):
    if len(graph_dic[comb[0]] & graph_dic[comb[1]]) >= threshold:
        res.append(comb)

m = len(res)

graph = H.form_dict_graph(res)

degree = {key: len(value) for key, value in graph.items()}

all_edges = H.compute_betweeness(graph)

all_edges = sorted(all_edges.items(), key=lambda a: -a[1])

for value in all_edges:
    print(value)

modularities = []

new_graph = graph.copy()

counter = 0

while True:
    counter += 1
    all_edges = H.compute_betweeness(new_graph)

    if not all_edges:
        break

    all_edges = sorted(all_edges.items(), key=lambda a: -a[1])

    highest_betweeness = all_edges[0][0]

    new_graph[highest_betweeness[0]].remove(highest_betweeness[1])
    new_graph[highest_betweeness[1]].remove(highest_betweeness[0])

    partitions = H.partition(new_graph)

    modularity = H.modulatiry(partitions, graph, new_graph, m)

    modularities.append(sum(modularity) / (2*m))

    print(counter)

print(modularities)

with open('modularities.txt', 'w') as file:
    for i in modularities:
        file.write('{}\n'.format(i))

