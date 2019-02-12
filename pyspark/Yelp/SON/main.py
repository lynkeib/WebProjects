from pyspark.sql import SparkSession
import Apriori as A
import json

sample_path = "Data/small2.csv"

ss = SparkSession \
    .builder \
    .appName('Son') \
    .master('local[*]') \
    .getOrCreate()

sc = ss.sparkContext

smallRDD = sc.textFile(sample_path)
header = smallRDD.first()

small1RDD = smallRDD.filter(lambda row: row != header) \
    .map(lambda line: (line.split(',')[0], line.split(',')[1])) \
    .combineByKey(lambda line: [line],
                  lambda exit, new: exit + [new],
                  lambda exit1, exit2: exit1 + exit2)

candidates = {}
frequent = {}
num_partitions = small1RDD.getNumPartitions()
print(num_partitions)
support = 20

candidates[1] = small1RDD.flatMap(lambda line: line[1]).distinct().collect()


candidates[1] = [set([y]) for y in candidates[1]]


freq = small1RDD.mapPartitions(lambda data: A.frequent_items(candidates[1], data, support / num_partitions)) \
    .map(lambda x: (tuple(x), 1)) \
    .reduceByKey(lambda a, b: a + b) \
    .filter(lambda a: a[1] >= num_partitions) \
    .map(lambda a: set(a[0])) \
    .cache()


frequent[1] = freq.collect()
k = 2

while 1:
    candidate_temp = A.create_candidates(frequent[k - 1], k)
    freq = small1RDD.mapPartitions(lambda data: A.frequent_items(candidate_temp, data, support / num_partitions)) \
        .map(lambda x: (tuple(x), 1)) \
        .reduceByKey(lambda a, b: a + b) \
        .filter(lambda a: a[1] >= num_partitions) \
        .map(lambda a: set(a[0])) \
        .cache()
    fr = freq.collect()
    if len(fr) == 0:
        break
    else:
        candidates[k] = candidate_temp
        frequent[k] = fr
        k += 1

for key, value in candidates.items():
    candidates[key] = sorted([tuple(item) for item in value])
print(candidates)
for key, value in frequent.items():
    frequent[key] = sorted([tuple(item) for item in value])
print(frequent)

# with open("candidates.json", "w") as file:
#     json.dump(candidates, file, indent=1)

# with open('frequent.json', 'w') as file:
#     json.dump(frequent, file, indent=1)
