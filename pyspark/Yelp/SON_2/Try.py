from pyspark.sql import SparkSession

ss = SparkSession \
    .builder \
    .master("local[*]") \
    .appName('Try') \
    .getOrCreate()

sc = ss.sparkContext

path = "/Users/chengyinliu/D/2019_Spring/INF553_ Foundations and Applications of Data Mining/ASSIGNMENTS/WEEK_2/SON/Data/small2.csv"

smallRDD = sc.textFile(path)
header = smallRDD.first()

createCombiner = (lambda line: [line])
mergeValue = (lambda exist, new: exist + [new])
mergeCombiner = (lambda exist1, exist2: exist1 + exist2)

smallRDD = smallRDD.filter(lambda line: line != header) \
    .map(lambda line: (line.split(',')[0], line.split(',')[1])) \
    .combineByKey(createCombiner, mergeValue, mergeCombiner)

smallRDD.foreach(print)


