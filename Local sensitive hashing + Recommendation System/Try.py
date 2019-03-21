from pyspark.sql import SparkSession
import random
import time
import os
from itertools import groupby
from itertools import combinations
import operator

os.environ['PYSPARK_PYTHON'] = '/anaconda3/envs/py36/bin/python3.6'
os.environ['PYSPARK_DRIVER_PYTHON'] = '/anaconda3/envs/py36/bin/python3.6'


def parse(line, unique_user):
    '''
    :param line: (business_id, list[user_id])
    :param unique_user: list[user_id]
    :return: (business_id, psrsed_list[user_id])
    '''
    return line[0], [unique_user.index(i) for i in line[1]]


def hashing_generate_signature(line, parameters, num_of_bins):
    '''
    :param line: (user_id, list[index])
    :param parameters: (tuples(a, b))
    :param num_of_bins: int
    :return: (user_id, parsed_list[index])
    '''
    res = []
    cal = lambda a, b, x, length: ((a * x + b) % length)
    for parameter in parameters:
        res.append(min([cal(parameter[0], parameter[1], index, num_of_bins) for index in line[1]]))
    return line[0], res


def chunks(list, length):
    """
    :param list: list[signatures]
    :param length: int
    """
    for i in range(0, len(list), length):
        yield list[i: i + length]


def hashing_generate_buckets(line, row_number):
    '''
    :param line: (user_id, list[signatures])
    :param row_number: int
    :return: list[tuple(signature, [business])]
    '''
    res = []
    for index, chunk in enumerate(chunks(line[1], row_number)):
        res.append((index, [(tuple(chunk), line[0])]))
    return res


def accumulate(l):
    '''
    :param l:
    '''
    it = groupby(l, operator.itemgetter(0))
    for key, subiter in it:
        yield key, [item[1] for item in subiter]


def groupby_chunk_num(line):
    '''
    :param line: list[tuples(chunk_index, [tuples(hash, budiness_id)])]
    :return:
    '''
    res = []
    for chunk in line:
        temp = list(accumulate(sorted(chunk[1])))
        res.append(temp)
    return res


def groupby_kvpairs_in_each_basket_and_genreate_candidates(chunks):
    '''
    :param chunks:
    :return:
    '''
    candidates = set()
    res = set()
    for chunk in chunks:
        for key, value in groupby(sorted(chunk[1]), lambda x: x[0]):
            vs = list(value)
            if len(vs) > 1:
                candidates.add(frozenset([v[1] for v in vs]))
    for cand in candidates:
        for c in combinations(cand, 2):
            res.add(frozenset(c))
    return res


def jar(l1, l2):
    '''
    :param l1: list
    :param l2: list
    :return: float
    '''
    res = [tp[0] == tp[1] for tp in zip(l1, l2)]
    return sum(res) / len(res)


def prim(max):
    res = set()
    res.add(2)
    for i in range(2, max):
        for j in range(2, max):
            if i % j == 0:
                break
            else:
                res.add(i)
    return res


########################  START  #####################
start = time.time()
random.seed(0)

# TODO: Setting files' paths
path = "Dataset/yelp_train.csv"
val_path = 'Dataset/pure_jaccard_similarity.csv'

# TODO: Seting Parameters for first hash
r = 4
b = 25
num_of_hash_func = r * b

# TODO: Start spark session and context
ss = SparkSession \
    .builder \
    .appName("LSH") \
    .master("local[*]") \
    .getOrCreate()
sc = ss.sparkContext

# TODO: Reading files
yelpRDD = sc.textFile(path)

# TODO: The header of the file
header = yelpRDD.first()

# TODO: Form the header of the overall matrix
yelpRDD = yelpRDD.filter(lambda line: line != header) \
    .map(lambda line: (line.split(',')[1], [line.split(',')[0]]))
# unique_users = sorted(list(set(yelpRDD.map(lambda line: line[1]).reduce(lambda a, b: a + b))))
unique_users = sorted(yelpRDD.map(lambda line: line[1][0]).distinct().collect())

# TODO: Form the RDD like [(Business_id, [User_id, User_id]), (Business_id, [User_id, User_id])]
yelpRDD = yelpRDD \
    .reduceByKey(lambda a, b: a + b)

# TODO: Convert the [User_id, User_id] part to [index, index], where the index is the index in the unique_users list
yelpRDD = yelpRDD.map(lambda line: parse(line, unique_users))  ## convert to index

# TODO: Generating the parameters of the hash functions
prim = list(prim(len(unique_users)))
parameters = [(random.choice(prim),
               random.choice(prim)) for _ in range(num_of_hash_func)]

# TODO: Minhash, the format returned is [Business_id, [reindex, reindex, reindex]], the length of the second list is num_of_hash_func
print('Minhash started')
yelpSigRDD = yelpRDD.map(
    lambda line: hashing_generate_signature(line, parameters, len(unique_users)))  ## permutations
print('Minhash completed')

# TODO: Forming the baskets, in the form of [(Basket_id, [Band of the Business_id, Business_id]), (Basked_id, [Band of the Business_id, Business_id])]
print('Forming the baskets')

basket_lists = yelpSigRDD.flatMap(lambda line: hashing_generate_buckets(line, r)) \
    .reduceByKey(lambda a, b: a + b) \
    .collect()

print('Forming baskets completed')

# TODO: Iter through every chunk, find the signature combinations that have more than 1 business_id and form combinations from such business_id list in each chunk
print('Generating candidates started')
candidates = groupby_kvpairs_in_each_basket_and_genreate_candidates(basket_lists)
print('Generating candidates completed')

# TODO: Second check on the candidates by calculating the Jaccard's Similarity of their signatures
signature = dict(yelpSigRDD.collect())
after_candidates = []
threshold = 0.45
for candidate in candidates:
    business_id_1, business_id_2 = tuple(candidate)[0], tuple(candidate)[1]
    if jar(signature[business_id_1], signature[business_id_2]) >= threshold:
        after_candidates.append(candidate)

after_candidates = set(after_candidates)
candidates = set(candidates)
end = time.time()
print()
print('time:', end - start)

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

print(f'Length of unique users: {len(unique_users)}')
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
print(f"r: {r}, b: {b}, threshold: {threshold}")
