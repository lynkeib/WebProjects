from pyspark.sql import SparkSession
import random
import time
import os

os.environ['PYSPARK_PYTHON'] = '/anaconda3/envs/py36/bin/python3.6'
os.environ['PYSPARK_DRIVER_PYTHON'] = '/anaconda3/envs/py36/bin/python3.6'

ss = SparkSession \
    .builder \
    .getOrCreate()

sc = ss.sparkContext

path = 'Dataset/yelp_train.csv'
test = 'Dataset/yelp_val.csv'

yelpRDD = sc.textFile(path)
header = yelpRDD.first()

data = yelpRDD.filter(lambda row: row != header).map(lambda x: x.split(","))

mov = data.map(lambda x: (x[1], 1)).reduceByKey(lambda x, y: x).map(lambda x: x[0])
movies = list(mov.collect())
movies.sort()
dicM = {}
for i, e in enumerate(movies):
    dicM[e] = i

usr = data.map(lambda x: (x[0], 1)).reduceByKey(lambda x, y: x).map(lambda x: x[0])
users = list(usr.collect())
users.sort()
dicU = {}
for i, e in enumerate(users):
    dicU[e] = i
vu = sc.broadcast(dicU)

mat = data.map(lambda x: (x[1], [vu.value[x[0]]])).reduceByKey(lambda x, y: x + y).sortBy(lambda x: x[0])
matrix = mat.collect()

m = len(users)  # m: the number of the bins


# hash function:
def f(x, has):
    a = has[0]
    b = has[1]
    p = has[2]
    # return ((a * x + b) % p) % m
    return min([((a * e + b) % p) % m for e in x[1]])


# TODO: more hash functions (or less?)
# hash parameters [a, b, p]
hashes = [[913, 901, 24593], [14, 23, 769], [1, 101, 193], [17, 91, 1543], \
          [387, 552, 98317], [11, 37, 3079], [2, 63, 97], [41, 67, 6151], \
          [91, 29, 12289], [3, 79, 53], [73, 803, 49157], [8, 119, 389]]
# good hash table primes: http://planetmath.org/goodhashtableprimes

# def hashMatrix(x):
#     return [f(x, has) for has in hashes]

# print(matrix[0])
# print(matrix[0][0], matrix[1][0], matrix[2][0], matrix[100][0])
# print(movies[0], movies[1], movies[2], movies[100])

signatures = mat.map(lambda x: (x[0], [f(x, has) for has in hashes]))
# print(signatures.collect()[:10])

n = len(hashes)  # the size of the signature column
b = 6
r = int(n / b)


def sig(x):
    # for e in x:
    res = []
    for i in range(b):
        res.append(((i, tuple(x[1][i * r:(i + 1) * r])), [x[0]]))
    return res


def pairs(x):
    res = []
    length = len(x[1])
    whole = list(x[1])
    whole.sort()
    for i in range(length):
        for j in range(i + 1, length):
            res.append(((whole[i], whole[j]), 1))
    return res


# cand = signatures.flatMap(sig)
cand = signatures.flatMap(sig).reduceByKey(lambda x, y: x + y).filter(lambda x: len(x[1]) > 1).flatMap(pairs) \
    .reduceByKey(lambda x, y: x).map(lambda x: x[0])


def jaccard(x):
    a = set(matrix[dicM[x[0]]][1])
    b = set(matrix[dicM[x[1]]][1])
    inter = a & b
    union = a | b
    jacc = len(inter) / len(union)
    return (x[0], x[1], jacc)


simiMovie = cand.map(jaccard).filter(lambda x: x[2] >= 0.5) \
    .map(lambda x: ((min(x[0], x[1]), max(x[0], x[1])), x[2]))

dataAll = data
data = dataAll.map(lambda x: ((x[0], x[1]), float(x[2])))
testRdd = sc.textFile(test).map(lambda x: x.split(","))
testHeader = testRdd.first()
testKey = testRdd.filter(lambda row: row != testHeader).map(lambda x: (x[0], x[1]))
testData = testKey.map(lambda x: (x, None))

# ((user_id, movie_id), rating)
trainData = data.subtractByKey(testData)
# print(trainData.take(10))
dicTrain = {}
for e in trainData.collect():
    dicTrain[e[0]] = e[1]

# (movie_id, average_rating)
movieAvg = trainData.map(lambda x: (x[0][1], [x[1]])).reduceByKey(lambda x, y: x + y).map(
    lambda x: (x[0], sum(x[1]) / len(x[1])))
dicAvg = {}
for e in movieAvg.collect():
    dicAvg[e[0]] = e[1]
# print(movieAvg.take(10))

# (user_id, [(movie_id, rating)])
userToMovie = trainData.map(lambda x: (x[0][0], [(x[0][1], x[1])])).reduceByKey(lambda x, y: x + y)

# print(userToMovie.collect())

from itertools import combinations


def movieRatingComb(x):
    for y in combinations(x[1], 2):
        a, b = min(y[0], y[1]), max(y[0], y[1])
        yield ((a[0], b[0]), [(a[1], b[1])])


movieToRating = userToMovie.flatMap(movieRatingComb).reduceByKey(lambda x, y: x + y)
print(movieToRating.collect())
