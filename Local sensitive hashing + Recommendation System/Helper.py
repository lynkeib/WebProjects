from math import sqrt
import numpy as np


def j(business_1, business_2, dataset):
    '''
    :param business_1: string
    :param business_2: string
    :param dataset: dict
    :return: float
    '''
    business_temp_1 = set(dataset[business_1])
    business_temp_2 = set(dataset[business_2])
    inter = business_temp_1 & business_temp_2
    union = business_temp_1 | business_temp_2
    return len(inter) / len(union)


def Consine_S(business_1, business_2, business_dict):
    '''
    :param business_1: stirng
    :param business_2: string
    :param business_dict: dict
    :return: float
    '''
    numerator = len(business_dict[business_1][0] & business_dict[business_2][0]) + business_dict[business_1][1] * \
                business_dict[business_2][1]
    denominator = sqrt(len(business_dict[business_1][0]) + business_dict[business_1][1] ** 2) * sqrt(
        len(business_dict[business_2][0]) + business_dict[business_2][1] ** 2)
    return numerator / denominator


def Pearson_similarity(business1, business2, business_user_rating):
    '''
    :param business1: string
    :param business2: string
    :param {business_user_rating: {business: {user: rating, user:rating}, business: {user:rating, user: rating}}}
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


def Predict_rating_LSH(user, business, user_business_rating, business_user_rating, candidates_pearson_similarities,
                       all_rating_average):
    '''
    :param user: string
    :param business: string
    :param user_business_rating: {user: {business: rating, business:rating}, user: {business:rating, business: rating}}
    :param business_user_rating: {business: {user: rating, user:rating}, business: {user:rating, user: rating}}}
    :param candidates_pearson_similarities: {(business_1, business_2): s, (business_1, business_3): s}
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
        pair = tuple({key, business})
        if pair in candidates_pearson_similarities:
            user_rated_business.append((candidates_pearson_similarities[pair], value))
    if len(user_rated_business) == 0:
        return all_rating_average
    numerator = np.sum([s * r for s, r in user_rated_business])
    denominator = np.sum([s for s, r in user_rated_business])
    if denominator == 0:
        return all_rating_average
    return numerator / denominator
