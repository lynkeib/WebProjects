from pyspark.sql import SparkSession
from pyspark.mllib.recommendation import ALS, MatrixFactorizationModel, Rating
import os

os.environ['PYSPARK_PYTHON'] = '/anaconda3/envs/py36/bin/python3.6'
os.environ['PYSPARK_DRIVER_PYTHON'] = '/anaconda3/envs/py36/bin/python3.6'

ss = SparkSession \
    .builder \
    .appName('Model_Based') \
    .config('local[*]') \
    .getOrCreate()

sc = ss.sparkContext

# Load and parse the data
data = sc.textFile("Dataset/yelp_train.csv")
header = data.first()
ratings = data.filter(lambda line: line != header) \
    .map(lambda l: l.split(','))\
    .map(lambda l: Rating(l[0], l[1], float(l[2])))

testRdd = sc.textFile('Dataset/yelp_val.csv').map(lambda x: x.split(","))
testHeader = testRdd.first()
testKey = testRdd.filter(lambda row: row != testHeader).map(lambda x: (int(x[0]), int(x[1])))

testData = testKey.map(lambda x: (x, None))

trainData = data.subtractByKey(testData)

ratings = trainData.map(lambda x: Rating(x[0][0], x[0][1], x[1]))


def cutPred(x):
    # rate = 0
    if x[2] > 5:
        rate = 5
    elif x[2] < 1:
        rate = 1
    else:
        rate = x[2]
    return ((x[0], x[1]), rate)



rank = 5
numIterations = 10
model = ALS.train(ratings, rank, numIterations)
preds = model.predictAll(testKey).map(cutPred)
noPred = testData.subtractByKey(preds).map(lambda x: (x[0], 3))
predictions = sc.union([preds, noPred]).sortBy(lambda x: x[0][1]).sortBy(lambda x: x[0][0])

print("result count: ")
print(predictions.count())
ratesAndPreds = data.join(testData).map(lambda x: (x[0], x[1][0])).join(predictions)
diff = ratesAndPreds.map(lambda r: abs(r[1][0] - r[1][1]))
diff01 = diff.filter(lambda x: 0 <= x < 1)
diff12 = diff.filter(lambda x: 1 <= x < 2)
diff23 = diff.filter(lambda x: 2 <= x < 3)
diff34 = diff.filter(lambda x: 3 <= x < 4)
diff4 = diff.filter(lambda x: 4 <= x)

MSE = diff.map(lambda x: x**2).mean()
RMSE = pow(MSE, 0.5)

ss.stop()

# Build the recommendation model using Alternating Least Squares
# rank = 10
# numIterations = 10
# model = ALS.train(ratings, rank, numIterations)

# Evaluate the model on training data
# testdata = ratings.map(lambda p: (p[0], p[1]))
# predictions = model.predictAll(testdata).map(lambda r: ((r[0], r[1]), r[2]))
# ratesAndPreds = ratings.map(lambda r: ((r[0], r[1]), r[2])).join(predictions)
# MSE = ratesAndPreds.map(lambda r: (r[1][0] - r[1][1])**2).mean()
# print("Mean Squared Error = " + str(MSE))

# Save and load model
# model.save(sc, "target/tmp/myCollaborativeFilter")
# sameModel = MatrixFactorizationModel.load(sc, "target/tmp/myCollaborativeFilter")



