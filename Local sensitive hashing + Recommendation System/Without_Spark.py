from pyspark.sql import SparkSession
import random
import time
import os
from itertools import combinations

start = time.time()
random.seed(0)

os.environ['PYSPARK_PYTHON'] = '/anaconda3/envs/py36/bin/python3.6'
os.environ['PYSPARK_DRIVER_PYTHON'] = '/anaconda3/envs/py36/bin/python3.6'

path = "Dataset/yelp_train.csv"
val_path = 'Dataset/pure_jaccard_similarity.csv'

r = 3
b = 50
num_of_hash_func = r * b

ss = SparkSession \
    .builder \
    .appName("LSH") \
    .master("local[*]") \
    .getOrCreate()
sc = ss.sparkContext

yelpRDD = sc.textFile(path)

header = yelpRDD.first()

yelpRDD = yelpRDD.filter(lambda line: line != header) \
    .map(lambda line: line.split(','))
users = sorted(yelpRDD.map(lambda line: line[0]).distinct().collect())
m = len(users)

yelp = yelpRDD.map(lambda line: (line[1], [line[0]])).reduceByKey(lambda a, b: a + b).collect()
yelp = dict(yelp)

parameters = [(random.choice(range(1, 1001)), random.choice(range(1, 1001))) for _ in range(num_of_hash_func)]

print('Generating signatures started')
signatures = {}
for key, value in yelp.items():
    signatures[key] = []
    temp = [users.index(v) for v in value]
    for para in parameters:
        signatures[key].append(min([(para[0] * x + para[1]) % m for x in temp]))
print('Generating signatures completed')

print('Generating bands started')
bands = {}
for i in range(b):
    bands[i] = {}

for key_s, value_s in signatures.items():
    for key_b, value_b in bands.items():
        try:
            bands[key_b][tuple(value_s[key_b * r: key_b * r + r])].append(key_s)
        except:
            bands[key_b][tuple(value_s[key_b * r: key_b * r + r])] = [key_s]
print('Generating bands completed')

print('Generating candidates started')
candidates = set()
for key_b, value_b in bands.items():
    for key_r, value_r in value_b.items():
        if len(value_r) > 1:
            for comb in combinations(value_r, 2):
                candidates.add(frozenset(comb))
print('Generating candidates completed')


def j(business_1, business_2, dataset):
    '''
    :param l1:
    :param l2:
    :return:
    '''
    business_temp_1 = set(dataset[business_1])
    business_temp_2 = set(dataset[business_2])
    inter = business_temp_1 & business_temp_2
    union = business_temp_1 | business_temp_2
    return len(inter) / len(union)


print('Generating after_candidates started')
after_candidates = set()
for cand in candidates:
    temp = tuple(cand)
    # print(f'{temp}: {j(temp[0], temp[1], signatures)}')
    if j(temp[0], temp[1], yelp) >= 0.5:
        after_candidates.add(cand)
print('Generating after_candidates completed')

end = time.time()
print(f'time: {end - start}')

# TODO: Validation with the result file
validationRDD = sc.textFile(val_path)

validation = validationRDD.filter(lambda line: line != header) \
    .map(lambda line: frozenset((line.split(',')[0], line.split(',')[1]))) \
    .collect()

ss.stop()

validation = set(validation)

TP = after_candidates & validation
FP = after_candidates - TP
FN = validation - TP

print(f'Length of unique users: {len(users)}')
print()
print(f'Length of candidates: {len(after_candidates)}')
print(f'Length of validation: {len(validation)}')
print()
print(f'TP: {len(TP)}')
print(f'FP: {len(FP)}')
print(f'FN: {len(FN)}')
print()
print(f'Precision: {len(TP) / (len(TP) + len(FP))}')
print(f'Recall: {len(TP) / (len(TP) + len(FN))}')
print()
print(f"r: {r}, b: {b}, threshold: {0.5}")
