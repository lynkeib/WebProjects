from pyspark.sql import SparkSession
import Apriori as A

ss = SparkSession \
    .builder \
    .master("local[*]") \
    .appName('Try') \
    .getOrCreate()

sc = ss.sparkContext

path = "/Users/chengyinliu/D/2019_Spring/INF553_ Foundations and Applications of Data Mining/ASSIGNMENTS/WEEK_2/SON/task2_data.csv"

smallRDD = sc.textFile(path)
header = smallRDD.first()

createCombiner = (lambda line: [line])
mergeValue = (lambda exist, new: exist + [new])
mergeCombiner = (lambda exist1, exist2: exist1 + exist2)

smallRDD = smallRDD.filter(lambda line: line != header) \
    .map(lambda line: (line.split(',')[0], line.split(',')[1])) \
    .combineByKey(createCombiner, mergeValue, mergeCombiner)

# smallRDD.foreach(print)

support = 7
threshold = 10
numOfPar = smallRDD.getNumPartitions()

candidates = smallRDD.mapPartitions(lambda partition: A.Apriori(partition, support / numOfPar, threshold / numOfPar)) \
    .reduceByKey(lambda a, b: a + b) \
    .map(lambda line: (line[0], {item for item in line[1]})) \
    .collect()

sc.broadcast(candidates)

frequent = smallRDD.flatMap(lambda line: A.global_frequent(line[1], candidates, support)) \
    .reduceByKey(
    lambda exist1, exist2: {key: exist1.get(key, 0) + exist2.get(key, 0) for key in set(exist1) | set(exist2)}) \
    .collect()

A = {item[0]: [key for key, value in item[1].items() if value >= support] for item in frequent}
print(A)
