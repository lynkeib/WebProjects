# 4.1 Task1: Data Exploration (3 points)

from pyspark.sql import SparkSession
import os
import sys
import json

# Make sure keep the same python version for driver and worker
# os.environ['PYSPARK_PYTHON'] = '/usr/local/bin/python3.7'
# os.environ['PYSPARK_DRIVER_PYTHON'] = '/usr/local/bin/python3.7'

# You will explore the dataset, review.json, containing review information for this task, and you need to write a program to automatically answer the following questions:

# TODO: Read In Data

ss = SparkSession \
    .builder \
    .master("local[*]") \
    .appName("task1") \
    .getOrCreate()

sc = ss.sparkContext

## read_path = "yelp_dataset/review.json"

read_path = sys.argv[1]

temp = sc.textFile(read_path)
review = temp.map(lambda line: json.loads(line))

# TODO: A. The total number of reviews (0.5 point)

n_review = review.count()

# TODO: B. The number of reviews in 2018 (0.5 point)

n_review_2018 = review.map(lambda x: x['date'][:4] == '2018').sum()

# TODO: C. The number of distinct users who wrote reviews (0.5 point)

n_user = review.map(lambda x: x['user_id']).distinct().count()

# TODO: D. The top 10 users who wrote the largest numbers of reviews and the number of reviews they wrote (0.5 point)

top10_user = review.map(lambda x: (x['user_id'], 1)).reduceByKey(lambda a, b: a + b).sortBy(
    lambda record: -record[1]).take(10)

# TODO: E. The number of distinct businesses that have been reviewed (0.5 point)

n_business = review.map(lambda x: x['business_id']).distinct().count()

# TODO: F. The top 10 businesses that had the largest numbers of reviews and the number of reviews they had (0.5 point)

top10_business = review.map(lambda x: (x['business_id'], 1)).reduceByKey(lambda a, b: a + b).sortBy(
    lambda record: -record[1]).take(10)

# TODO: Write Files

write_path = sys.argv[2]

return_ = {'n_review': n_review,
           'n_review_2018': n_review_2018,
           'n_user': n_user,
           'top10_user': top10_user,
           'n_business': n_business,
           'top10_business': top10_business}

with open(write_path, 'w') as file:
    json.dump(return_, file, indent=1)
