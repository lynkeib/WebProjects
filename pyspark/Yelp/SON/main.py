from pyspark.sql import SparkSession
import Apriori as A
import json
import time

sample_path = "/Users/chengyinliu/D/2019_Spring/INF553_ Foundations and Applications of Data Mining/ASSIGNMENTS/WEEK_2/SON/task2_data.csv"

ss = SparkSession \
    .builder \
    .appName('SON') \
    .master('local[*]') \
    .getOrCreate()

sc = ss.sparkContext

start1 = time.time()
smallRDD = sc.textFile(sample_path)
header = smallRDD.first()

support = 50
th = 70

small2RDD = smallRDD.filter(lambda row: row != header) \
    .map(lambda line: (line.split(',')[0], line.split(',')[1])) \
    .combineByKey(lambda line: [line],
                  lambda exit, new: exit + [new],
                  lambda exit1, exit2: exit1 + exit2)

small1RDD = small2RDD.filter(lambda record: len(record[1]) > th)

candidates = {}
frequent = {}

num_partitions = small1RDD.getNumPartitions()
print(num_partitions)


temp = small1RDD.mapPartitions(lambda data: A.makedic(data)).reduceByKey(lambda a, b: a + b).collect()
temp_1 = {tup[0]: tup[1] for tup in temp}
candidates[1] = [{item} for item in list(temp_1.values())]
frequent[1] = [{key} for key, value in temp_1.items() if value >= support]
freq = sc.parallelize(frequent[1]).persist()

k = 2

while 1:
    print(k)
    candidate_temp = A.create_candidates(freq.collect(), k)
    print('finished candidates creating')
    freq.unpersist()
    print('freq unpersist')
    freq = small1RDD.mapPartitions(lambda data: A.frequent_items(candidate_temp, data, support / num_partitions)) \
        .map(lambda x: (tuple(x), 1)) \
        .reduceByKey(lambda a, b: a + b) \
        .filter(lambda a: a[1] >= num_partitions) \
        .map(lambda a: set(a[0])) \
        .cache()
    print('finished frequent creating')
    fr = freq.collect()
    if len(fr) == 0:
        break
    else:
        candidates[k] = candidate_temp
        frequent[k] = fr
        k += 1

for key, value in candidates.items():
    candidates[key] = sorted([tuple(item) for item in value])
# print(candidates)
with open("candidates.json", "w") as file:
    json.dump(candidates, file, indent=1)
for key, value in frequent.items():
    frequent[key] = sorted([tuple(item) for item in value])
# print(frequent)
with open('frequent.json', 'w') as file:
    json.dump(frequent, file, indent=1)

end1 = time.time()
print(end1 - start1)
