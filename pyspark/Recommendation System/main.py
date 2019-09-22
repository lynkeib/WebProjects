from pyspark import SparkContext


def main():
    train_path = "./Data/yelp_train.csv"
    sc = SparkContext("local[*]", "RS")
    trainRDD = sc.textFile(train_path)
    header = trainRDD.first()
    trainRDD = trainRDD.filter(lambda x: x != header)
    trainRDD.map(lambda a: print(a))

if __name__ == "__main__":
    main()
