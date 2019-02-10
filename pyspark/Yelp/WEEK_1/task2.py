from pyspark.sql import SparkSession
import os
import sys
import json
import time

# Make sure keep the same python version for driver and worker
os.environ['PYSPARK_PYTHON'] = '/usr/local/bin/python3.7'
os.environ['PYSPARK_DRIVER_PYTHON'] = '/usr/local/bin/python3.7'

# You will explore the dataset, review.json, containing review information for this task, and you need to write a program to automatically answer the following questions:

# TODO: Read In Data

ss = SparkSession \
    .builder \
    .master("local[*]") \
    .appName("task1") \
    .getOrCreate()

sc = ss.sparkContext

# read_path = "yelp_dataset/review.json"

read_path = sys.argv[1]

temp = sc.textFile(read_path)
review = temp.map(lambda line: json.loads(line))

n_partition_1 = review.getNumPartitions()
n_items_1 = review.glom().map(len).collect()

# TODO: F. The top 10 businesses that had the largest numbers of reviews and the number of reviews they had (0.5 point)

start1 = time.time()
top10_business = review.map(lambda x: (x['business_id'], 1)).reduceByKey(lambda a, b: a + b).sortBy(
    lambda record: -record[1]).take(10)
end1 = time.time()
exe_time_1 = end1 - start1

n = sys.argv[3]
# n = 400

review2 = review.repartition(int(n))
n_items_2 = review2.glom().map(len).collect()
n_partition_2 = review2.getNumPartitions()
start2 = time.time()
top10_business_2 = review2.map(lambda x: (x['business_id'], 1)).reduceByKey(lambda a, b: a + b).sortBy(
    lambda record: -record[1]).take(10)
end2 = time.time()
exe_time_2 = end2 - start2

# print(n_partition_1)
# print(n_items_1)
# print(exe_time_1)
# print(n_partition_2)
# print(n_items_2)
# print(exe_time_2)

return_ = {"default":
               {"n_partition": n_partition_1,
                "n_items": n_items_1,
                "exe_time": exe_time_1},
           "customized":
               {"n_partition": n_partition_2,
                "n_items": n_items_2,
                "exe_time": exe_time_2},
           "explanation": 1}

write_path = sys.argv[2]
with open(write_path, 'w') as file:
    json.dump(return_, file, indent=1)
