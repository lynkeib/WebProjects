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


# -------------------------------------- MAIN START  --------------------------------------

def main():
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

    user_average = {key: np.mean([value_b for key_b, value_b in value.items()]) for key, value in
                    user_business_rating.items()}

    validation_RDD = sc.textFile(test)

    header = validation_RDD.first()

    validation = validation_RDD.filter(lambda line: line != header) \
        .map(lambda line: line.split(',')) \
        .map(lambda line: ((line[0], line[1]), [float(line[2])])) \
        .collect()
    validation = dict(validation)

    ss.stop()

    N = 10

    similarities_dict = {}

    all_rating_average = np.mean(
        [value_b for key, value in user_business_rating.items() for key_b, value_b in value.items()])

    for key, value in validation.items():
        validation[key].append(
            Predict_rating(key[0], key[1], user_business_rating, business_user_rating, N, similarities_dict,
                           all_rating_average, user_average))

    RMSE = sqrt(np.mean([(value[0] - value[1]) ** 2 for key, value in validation.items()]))

    differences = [int(abs(value[0] - value[1])) for key, value in validation.items()]
    end = time.time()

    print(f'RMSE: {RMSE}')
    print(f'time: {end - start}')
    print(f'5 levels: {Counter(differences)}')


# -------------------------------------- MAIN END  --------------------------------------


# -------------------------------------- HELPER START --------------------------------------

def Pearson_similarity(user1, user2, user_business_rating):
    '''
    :param user1: string
    :param user2: string
    :param user_business_rating: {user: {business: rating, business:rating}, user: {business:rating, business: rating}}
    :return: float
    '''
    user1_businesses = set(user_business_rating[user1].keys())
    user2_businesses = set(user_business_rating[user2].keys())
    both_businesses = user1_businesses & user2_businesses
    if len(both_businesses) == 0:
        return 0.0
    all_ratings_user1 = np.array([user_business_rating[user1][business] for business in both_businesses])
    all_ratings_user2 = np.array([user_business_rating[user2][business] for business in both_businesses])
    average_rating_user1 = np.mean(all_ratings_user1)
    average_rating_user2 = np.mean(all_ratings_user2)
    denominator = sqrt(np.sum((all_ratings_user1 - average_rating_user1) ** 2)) * sqrt(
        np.sum((all_ratings_user2 - average_rating_user2) ** 2))
    if denominator == 0:
        return 0.0
    numerator = np.sum(
        (all_ratings_user1 - average_rating_user1) * (all_ratings_user2 - average_rating_user2))
    return abs(numerator / denominator)


def Predict_rating(user, business, user_business_rating, business_user_rating, N, similarities_dict,
                   all_rating_average, user_average):
    '''
    :param user: string
    :param business: string
    :param user_business_rating: {user: {business: rating, business:rating}, user: {business:rating, business: rating}}
    :param business_user_rating: {business: {user: rating, user:rating}, business: {user:rating, user: rating}}}
    :param N: int
    :param similarities_dict: {(business_1, business_2): s, (business_1, business_3): s}
    :param all_rating_average: float
    :param user_average: {user: avg_rating, user: avg_rating}
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
    user_predict_business = set(key for key, value in user_business_rating[user].items())
    for key, value in business_user_rating[business].items():
        if (min(key, user), max(key, user)) not in similarities_dict:
            user_comparison_business = set(key for key, value in user_business_rating[key].items())
            common_rated_business = user_predict_business & user_comparison_business
            if len(common_rated_business) == 0:
                similarities_dict[(min(key, user), max(key, user))] = (0, 0)
                user_rated_business.append(((0, 0), value))
            else:
                similarity = Pearson_similarity(key, user, user_business_rating)
                user_comparison_avg_rating = np.mean(
                    [user_business_rating[key][business] for business in common_rated_business])
                similarities_dict[(min(key, user), max(key, user))] = (similarity, user_comparison_avg_rating)
                user_rated_business.append(((similarity, user_comparison_avg_rating), value))
        else:
            # ((similarity, user_comparison_avg_rating), rating)
            user_rated_business.append((similarities_dict[(min(key, user), max(key, user))], value))

    if len(user_rated_business) > N:
        user_rated_business = sorted(user_rated_business, key=lambda item: item[0][0], reverse=True)
        numerator = 0
        denominator = 0
        for i in range(N):
            numerator += (user_rated_business[i][1] - user_rated_business[i][0][1]) * user_rated_business[i][0][0]
            denominator += user_rated_business[i][0][0]
        if denominator == 0:
            return all_rating_average
        if user not in user_average:
            return all_rating_average + numerator / denominator
        return user_average[user] + numerator / denominator
    numerator = np.sum([s[0] * (r - s[1]) for s, r in user_rated_business])
    denominator = np.sum([s[0] for s, r in user_rated_business])
    if denominator == 0:
        return all_rating_average
    if user not in user_average:
        return all_rating_average + numerator / denominator
    return user_average[user] + numerator / denominator


# -------------------------------------- HELPER END --------------------------------------

if __name__ == '__main__':
    main()
