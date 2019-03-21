from pyspark.sql import SparkSession
import os
import numpy as np
from math import sqrt
import time
from collections import Counter

os.environ['PYSPARK_PYTHON'] = '/anaconda3/envs/py36/bin/python3.6'
os.environ['PYSPARK_DRIVER_PYTHON'] = '/anaconda3/envs/py36/bin/python3.6'

start = time.time()

ss = SparkSession \
    .builder \
    .getOrCreate()

sc = ss.sparkContext

path = 'Dataset/yelp_train.csv'
test = 'Dataset/yelp_val.csv'


def main():
    # -------------------------------------- MAIN START  --------------------------------------

    yelpRDD = sc.textFile(path)

    header = yelpRDD.first()

    yelpRDD = yelpRDD.filter(lambda line: line != header) \
        .map(lambda line: line.split(','))

    user_business_rating = yelpRDD.map(lambda line: (line[0], [(line[1], float(line[2]))])) \
        .reduceByKey(lambda a, b: a + b) \
        .mapValues(dict) \
        .collect()
    user_business_rating = dict(user_business_rating)

    business_user_rating = yelpRDD.map(lambda line: (line[1], [(line[0], float(line[2]))])) \
        .reduceByKey(lambda a, b: a + b) \
        .mapValues(dict) \
        .collect()
    business_user_rating = dict(business_user_rating)

    validation_RDD = sc.textFile(test)

    header = validation_RDD.first()

    validation = validation_RDD.filter(lambda line: line != header) \
        .map(lambda line: line.split(',')) \
        .map(lambda line: ((line[0], line[1]), [float(line[2])])) \
        .collect()
    validation = dict(validation)

    ss.stop()

    N = 50

    similarities_dict = {}

    all_rating_average = np.mean(
        [value_b for key, value in user_business_rating.items() for key_b, value_b in value.items()])

    for key, value in validation.items():
        validation[key].append(
            Predict_rating(key[0], key[1], user_business_rating, business_user_rating, N, similarities_dict,
                           all_rating_average))

    RMSE = sqrt(np.mean([(value[0] - value[1]) ** 2 for key, value in validation.items()]))
    differences = [int(abs(value[0] - value[1])) for key, value in validation.items()]
    end = time.time()

    # -------------------------------------- MAIN END  --------------------------------------

    print(f'RMSE: {RMSE}')
    print(f'time: {end - start}')
    print(f'5 levels: {Counter(differences)}')


# -------------------------------------- HELPER START --------------------------------------

def Pearson_similarity(business1, business2, business_user_rating):
    '''
    :param business1: string
    :param business2: string
    :param business_user_rating: {business: {user: rating, user:rating}, business: {user:rating, user: rating}}
    :return: float
    '''
    business1_users = set(business_user_rating[business1].keys())
    business2_users = set(business_user_rating[business2].keys())
    both_users = business1_users & business2_users
    if len(both_users) == 0:
        return 0.0
    all_ratings_business1 = np.array([business_user_rating[business1][user] for user in both_users])
    all_ratings_business2 = np.array([business_user_rating[business2][user] for user in both_users])
    average_rating_business1 = np.mean(all_ratings_business1)
    average_rating_business2 = np.mean(all_ratings_business2)
    denominator = sqrt(np.sum((all_ratings_business1 - average_rating_business1) ** 2)) * sqrt(
        np.sum((all_ratings_business2 - average_rating_business2) ** 2))
    if denominator == 0:
        return 0.0
    numerator = np.sum(
        (all_ratings_business1 - average_rating_business1) * (all_ratings_business2 - average_rating_business2))
    return abs(numerator / denominator)


def Predict_rating(user, business, user_business_rating, business_user_rating, N, similarities_dict,
                   all_rating_average):
    '''
    :param user: string
    :param business: string
    :param user_business_rating: {user: {business: rating, business:rating}, user: {business:rating, business: rating}}
    :param business_user_rating: {business: {user: rating, user:rating}, business: {user:rating, user: rating}}}
    :param N: int
    :param similarities_dict: {(business_1, business_2): s, (business_1, business_3): s}
    :param all_rating_average: float
    :return: float
    '''
    if business not in business_user_rating and user not in user_business_rating:
        return all_rating_average
    if business not in business_user_rating:
        all_user_rating = [value for key, value in user_business_rating[user].items()]
        return np.mean(all_user_rating)
    if user not in user_business_rating:
        all_business_rating = [value for key, value in business_user_rating[business].items()]
        return np.mean(all_business_rating)
    user_rated_business = []
    for key, value in user_business_rating[user].items():
        if (min(key, business), max(key, business)) not in similarities_dict:
            similarity = Pearson_similarity(key, business, business_user_rating)
            similarities_dict[(min(key, business), max(key, business))] = similarity
            user_rated_business.append((similarity, value))
        else:
            user_rated_business.append((similarities_dict[(min(key, business), max(key, business))], value))

    if len(user_rated_business) > N:
        user_rated_business = sorted(user_rated_business, key=lambda item: item[0], reverse=True)
        numerator = 0
        denominator = 0
        for i in range(N):
            numerator += user_rated_business[i][0] * user_rated_business[i][1]
            denominator += user_rated_business[i][0]
        if denominator == 0:
            return all_rating_average
        return numerator / denominator
    numerator = np.sum([s * r for s, r in user_rated_business])
    denominator = np.sum([s for s, r in user_rated_business])
    if denominator == 0:
        return all_rating_average
    return numerator / denominator


# -------------------------------------- HELPER END --------------------------------------

if __name__ == '__main__':
    main()
