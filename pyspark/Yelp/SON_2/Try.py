from pyspark.sql import SparkSession
import Apriori as A
from functools import reduce

ss = SparkSession \
    .builder \
    .master("local[*]") \
    .appName('Try') \
    .getOrCreate()

sc = ss.sparkContext

path = "/Users/chengyinliu/D/2019_Spring/INF553_ Foundations and Applications of Data Mining/ASSIGNMENTS/WEEK_2/SON/task2_data.csv"
# path = "/Users/chengyinliu/D/2019_Spring/INF553_ Foundations and Applications of Data Mining/ASSIGNMENTS/WEEK_2/SON/Data/small2.csv"

userRDD = sc.textFile(path)
header = userRDD.first()

support = 50
threshold = 70

createCombiner = (lambda line: [line])
mergeValue = (lambda exist, new: exist + [new])
mergeCombiner = (lambda exist1, exist2: exist1 + exist2)

userRDD = userRDD.filter(lambda line: line != header) \
    .map(lambda line: (line.split(',')[0], line.split(',')[1])) \
    .combineByKey(createCombiner, mergeValue, mergeCombiner) \
    .filter(lambda line: len(line[1]) >= threshold)

# userRDD.foreach(print)

businessRDD = userRDD.flatMap(lambda line: A.convert(line)) \
    .groupByKey() \
    .mapValues(set)

business = businessRDD.collect()
businessdict = {item[0]: item[1] for item in business}

numOfPar = userRDD.getNumPartitions()

candidates = userRDD.mapPartitions(lambda partition: A.Apriori(partition, support / numOfPar)) \
    .reduceByKey(lambda a, b: a | b) \
    .collect()

candidates = sorted([(key, sorted([list(sets) for sets in value])) for key, value in candidates])

res = []
for cand in candidates:
    temp_1 = []

    if cand[0] == 1:
        for value in cand[1]:
            if len(businessdict[value[0]]) >= support:
                temp_1.append(value)
    else:
        for value in cand[1]:
            temp = reduce(lambda a, b: a & b, (businessdict[x] for x in value))
            if len(temp) >= support:
                temp_1.append(value)
    if len(temp_1) == 0:
        break
    res.append((cand[0], temp_1))

with open('Yelp.txt', 'w') as file:
    print('candidates')
    file.writelines("Candidates")
    file.writelines('\n')
    for key, can in candidates:
        file.writelines(str(can))
        file.writelines('\n')
        file.writelines('\n')
        print("Key", key)
        print(can)
        print()
    file.writelines('\n')
    file.writelines("Frequent:")
    file.writelines('\n')
    for key, can in res:
        file.writelines(str(can))
        file.writelines('\n')
        file.writelines('\n')
        print("Key", key)
        print(can)
        print()
