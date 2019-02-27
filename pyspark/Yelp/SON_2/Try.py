from pyspark.sql import SparkSession
import Apriori as A

ss = SparkSession \
    .builder \
    .master("local[*]") \
    .appName('Try') \
    .getOrCreate()

sc = ss.sparkContext

path = "/Users/chengyinliu/D/2019_Spring/INF553_ Foundations and Applications of Data Mining/ASSIGNMENTS/WEEK_2/SON/task2_data.csv"
# path = "/Users/chengyinliu/D/2019_Spring/INF553_ Foundations and Applications of Data Mining/ASSIGNMENTS/WEEK_2/SON/Data/small2.csv"
smallRDD = sc.textFile(path)
header = smallRDD.first()

# smallRDD.foreach(print)

support = 50
threshold = 70

createCombiner = (lambda line: [line])
mergeValue = (lambda exist, new: exist + [new])
mergeCombiner = (lambda exist1, exist2: exist1 + exist2)

def convert(line):
    res = []
    for business in line[1]:
        res.append((business, line[0]))
    return res

businessRDD = smallRDD.filter(lambda line: line != header) \
    .map(lambda line: (line.split(',')[0], line.split(',')[1])) \
    .combineByKey(createCombiner, mergeValue, mergeCombiner) \
    .filter(lambda line: len(line[1]) >= threshold) \
    .flatMap(lambda line: convert(line)) \
    .groupByKey() \
    .mapValues(list)

# business = businessRDD.filter(lambda line: len(line[1]) > support).collect()

businessdict = {item[0]:item[1] for item in business}




# businessRDD = smallRDD.filter(lambda line: line != header) \
#     .map(lambda line: (line.split(',')[1], line.split(',')[0])) \
#     .combineByKey(createCombiner, mergeValue, mergeCombiner) \
#     .filter(lambda line: len(line[1]) >= threshold)


#
numOfPar = smallRDD.getNumPartitions()
#
candidates = smallRDD.mapPartitions(lambda partition: A.Apriori(partition, support / numOfPar)) \
    .reduceByKey(lambda a, b: a + b) \
    .map(lambda line: (line[0], set(frozenset(item) for item in line[1]))) \
    .map(lambda line: (line[0], [tuple(item) for item in line[1]])) \
    .collect()
#
# # print([item for item in candidates if item[0] == 1])
#
# # print("candidates", candidates)
#
# # sc.broadcast(candidates)
#
# # A = smallRDD.flatMap(lambda line: line[1]).collect()
#
# # print(A)
#
# frequent = smallRDD.flatMap(lambda line: A.global_frequent(line[1], candidates)) \
#     .reduceByKey(
#     lambda exist1, exist2: {key: exist1.get(key, 0) + exist2.get(key, 0) for key in set(exist1) | set(exist2)}) \
#     .collect()
# #
# # for i in sorted(frequent):
# #     print(sorted(map(sorted, list(i[1].keys()))))
# #     print()
# #
# A = {item[0]: [key for key, value in item[1].items() if value >= support] for item in frequent}
#
# print(A)
