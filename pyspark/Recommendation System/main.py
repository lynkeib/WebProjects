from pyspark import SparkContext
from collections import namedtuple
from utils import *


def main():
    b = 50
    r = 3
    train_path = "./Data/yelp_train.csv"
    validation_path = "./Data/yelp_val.csv"

    sc = SparkContext("local[*]", "RS")

    trainRDD = sc.textFile(train_path)
    valRDD = sc.textFile(validation_path)

    header = trainRDD.first()
    user_business = trainRDD.filter(lambda x: x != header) \
        .map(lambda line: line.split(",")) \
        .map(lambda lst: (lst[0], [(lst[1], float(lst[2]))])) \
        .reduceByKey(lambda a, b: a + b) \
        .mapValues(dict)
    business_user = trainRDD.filter(lambda x: x != header) \
        .map(lambda line: line.split(",")) \
        .map(lambda lst: (lst[1], [(lst[0], float(lst[2]))])) \
        .reduceByKey(lambda a, b: a + b) \
        .mapValues(dict)

    header = valRDD.first()
    valRDD = valRDD.filter(lambda x: x != header) \
        .map(lambda line: line.split(",")) \
        .map(lambda lst: (lst[0], [(lst[1], float(lst[2]))])) \
        .reduceByKey(lambda a, b: a + b) \
        .mapValues(dict)
    # trainRDD.foreach(print)
    users_business_rating = dict(user_business.collect())
    business_user_rating = dict(business_user.collect())
    user_average_rating = {user: float(sum(business_rating.values())) / len(business_rating.values()) for
                           user, business_rating in users_business_rating.items()}
    for key, value in users_business_rating.items():
        print('key', key, 'value', value)
    for key, value in user_average_rating.items():
        print('key', key, 'value', value)
    print(Predict_User_Rating_On_a_Business("sdLns7062kz3Ur_b8wgeYw",
                                            "9S7RUjzkdpU4MDxUxkvLvg",
                                            users_business_rating,
                                            business_user_rating,
                                            user_average_rating))

    # all_business = list(set(key for value in users.values() for key in value.keys()))
    #
    #
    #
    # business_order = {all_business[index]: index for index in range(len(all_business))}
    # # print(business_order)
    # # print(users)
    # MinHashMatrix = buildMinHashMatrix(users, business_order, b * r)
    # for key, value in MinHashMatrix.items():
    #     print(key, value)
    # user_set = set(users.keys())
    # candidates = findCandidates(user_set, MinHashMatrix, b, r)
    # print(candidates)


if __name__ == "__main__":
    main()
