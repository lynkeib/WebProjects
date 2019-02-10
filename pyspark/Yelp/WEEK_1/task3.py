from pyspark.sql import SparkSession
import os
import sys
import json
import time

# Make sure keep the same python version for driver and worker
# os.environ['PYSPARK_PYTHON'] = '/usr/local/bin/python3.7'
# os.environ['PYSPARK_DRIVER_PYTHON'] = '/usr/local/bin/python3.7'

# You will explore the dataset, review.json, containing review information for this task, and you need to write a program to automatically answer the following questions:

ss = SparkSession \
    .builder \
    .master("local[*]") \
    .appName("task1") \
    .getOrCreate()

sc = ss.sparkContext



# TODO: Read In Data

# path_review = "yelp_dataset/review.json"
# path_business = "yelp_dataset/business.json"

path_review = sys.argv[1]
path_business = sys.argv[2]

reviewRDDtemp = sc.textFile(path_review)
reviewRDD = reviewRDDtemp.map(lambda line: json.loads(line))

businessRDDtemp = sc.textFile(path_business)
businessRDD = businessRDDtemp.map(lambda line: json.loads(line))

# TODO: A. What is the average stars for each city?
# (DO NOT use the stars information in the business file) (1 point)

reviewRDD_id_star = reviewRDD.map(lambda line: (line['business_id'], line['stars']))
businessRDD_state = businessRDD.map(lambda line: (line['business_id'], line['state']))

allRDD = reviewRDD_id_star.join(businessRDD_state)

average_star = allRDD.map(lambda line: (line[1][1], (line[1][0], 1))) \
    .reduceByKey(lambda a, b: (a[0] + b[0], a[1] + b[1])) \
    .map(lambda t: (t[0], t[1][1] / t[1][0]))

# average_star = allRDD.map(lambda line: (line['state'], (line["stars"], 1))) \
#     .reduceByKey(lambda a, b: (a[0] + b[0], a[1] + b[1])) \
#     .map(lambda t: (t[0], t[1][1] / t[1][0])) \
#     .take(10)
# print(average_star)

# TODO: B. You are required to use two ways to print top 10 cities with highest stars.
# You need to compare the time difference between two methods and explain the result
# within 1 or 2 sentences. (1 point)

average_star.sortBy(lambda line: -line[1])

start1 = time.time()
# print(average_star.collect()[:10])
end1 = time.time()
# print(end1 - start1)
start2 = time.time()
# print(average_star.take(10))
end2 = time.time()
# print(end2 - start2)


output_A_path = sys.argv[3]
outpit_B_path = sys.argv[4]

result__ = average_star.collect()

with open(output_A_path, 'w') as file:
    for line in result__:
        file.write(line[0] + ':' + str(line[1]) + '\n')

result_ = {
    "m1": end1 - start1,
    "m2": end2 - start2,
    "explaination": 1
}


with open(outpit_B_path, "w") as file:
    json.dump(result_, file, indent=1)


