from pyspark.sql import SparkSession
from itertools import combinations

path = 'Data/ub_sample_data.csv'

spark = SparkSession.builder \
    .appName("Assignment4") \
    .getOrCreate()

sc = spark.sparkContext
rdd = sc.textFile(path)
rddHeader = rdd.first()

data = rdd.filter(lambda row: row != rddHeader).map(lambda x: x.split(",")) \
    .map(lambda x: ((x[0], [x[1]]))) \
    .reduceByKey(lambda a, b: a + b) \
    .mapValues(set) \
    .collect()

user_business = dict(data)
all_users = user_business.keys()
edges = {}
for user1, user2 in combinations(all_users, 2):
    if len(user_business[user1] & user_business[user2]) >= 7:
        try:
            edges[user1].append(user2)
        except:
            edges[user1] = [user2]
        try:
            edges[user2].append(user1)
        except:
            edges[user2] = [user1]
# edges = {node : [node, node], node: [node, node] ...}

betweenness = {}

for node in edges:
    head = node
    bfsTraversal = [head]
    nodes = set(bfsTraversal)
    treeLevel = {head:0}
    dicParent = {}
    index = 0
    while index < len(bfsTraversal):
        head = bfsTraversal[index]
        children = edges[head]
        for child in children:
            if child not in nodes:
                bfsTraversal.append(child)
                nodes.add(child)
                treeLevel[child] = treeLevel[head] + 1
                dicParent[child] = [head]
            else:
                if treeLevel[child] == treeLevel[head] + 1:
                    dicParent[child] += [head]
    print(bfsTraversal)
# find bfs