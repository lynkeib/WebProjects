import random
from itertools import combinations


def JaccardSimilarity(user1, user2):
    """
    :param user1: {business_id1: rating1, business_id2: rating2}
    :param user2: {business_id1: rating1, business_id2: rating2}
    :return: float
    """
    user1_set = set(user1.keys())
    user2_set = set(user2.keys())
    return len((user1_set & user2_set)) / float(len(user1_set | user2_set))


## User-Baesd
def Calculate_Pearson_Similarity(user1, user2, user_business_rating):
    """
    :param user1: string
    :param user2: string
    :param user_business_rating:  {user1: {business_id1: rating1, business_id2: rating2}, user2: {business_id1: rating1, business_id2: rating2}...}
    :return: float
    """
    # Step 1: find co-rated businesses
    user1_rated_businesses = set(user_business_rating[user1].keys())
    user2_rated_businesses = set(user_business_rating[user2].keys())
    co_rated_businesses = user1_rated_businesses & user2_rated_businesses
    ## if do not have co_rated_businesses, then the Similarity is 0
    if len(co_rated_businesses) == 0:
        return 0.0

    # Step 2: calculate the average rating on ro_rated_business
    user1_co_rated_average = float(sum(
        rating for business, rating in user_business_rating[user1].items() if business in co_rated_businesses)) / len(
        co_rated_businesses)
    user2_co_rated_average = float(sum(
        rating for business, rating in user_business_rating[user2].items() if business in co_rated_businesses)) / len(
        co_rated_businesses)

    # Step 3: calculate Numerator and Denominator
    Numerator = float(sum((user_business_rating[user1][business] - user1_co_rated_average) * (
            user_business_rating[user2][business] - user2_co_rated_average) for business in co_rated_businesses))
    Denominator = sum(
        (user_business_rating[user1][business] - user1_co_rated_average) ** 2 for business in co_rated_businesses) ** (
                          1.0 / 2) * sum(
        (user_business_rating[user2][business] - user2_co_rated_average) ** 2 for business in co_rated_businesses) ** (
                              1.0 / 2)
    ## if Denominator is 0
    if Denominator == 0:
        return 0.0
    else:
        return Numerator / Denominator


def Predict_User_Rating_On_a_Business(user, business, user_business_rating, business_user_rating, user_average_rating):
    """
    :param user: string
    :param business: string
    :param user_business_rating: {user1: {business_id1: rating1, business_id2: rating2}, user2: {business_id1: rating1, business_id2: rating2}...}
    :param business_user_rating: {business_id1: {user1: rating1, user2: rating2}, business_id2: {user1: rating1, user2: rating2}...}
    :param user_average_rating: {user1: rating1, user2: rating2...}
    :return: float
    """
    # Step 1: find users who rated this business
    users_rated_this_business = set(business_user_rating[business].keys())
    ## if not users rated this business, then use the user average as an estimation
    if len(users_rated_this_business) == 0:
        return user_average_rating[user]

    # Step 2: calculate the Pearson Correlation Coefficient between them
    pearson_correlation = dict()
    for other_user in users_rated_this_business:
        pearson_correlation[other_user] = Calculate_Pearson_Similarity(user, other_user, user_business_rating)
    print("pearson_correlation is")
    for key, value in pearson_correlation.items():
        print('key', key, 'value', value)

    # Step 3: Calculate Numerator and Denominator
    Numerator = sum(
        (user_business_rating[other_user][business] - user_average_rating[other_user]) * pearson_correlation[other_user]
        for other_user in users_rated_this_business)
    print('Numerator is', Numerator)
    Denominator = sum(abs(pearson_correlation[other_user]) for other_user in users_rated_this_business)
    ## if Denominator is 0, then the best estimation is the average of this user
    if Denominator == 0:
        return user_average_rating[user]
    else:
        return user_average_rating[user] + (float(Numerator) / Denominator)


def hash_generator(num):
    hash_functions = [(random.choice(range(1, 1001)), random.choice(range(1, 1001))) for _ in range(num)]
    return hash_functions


def buildMinHashMatrix(users, business_order, numer_of_hashfunc):
    """
    :param users: {user1: {business_id1: rating1, business_id2: rating2}, user2: {business_id1: rating1, business_id2: rating2}...}
    :param business_order: {business_id1: order1, business_id2: order2...}
    :param numer_of_hashfunc: int
    :return: {user1: [order3, order2...], user2: [order4, order15...]}
    """
    hash_functions = hash_generator(numer_of_hashfunc)
    MinHashMatrix = dict()
    business_number = len(business_order.keys())
    for user in users.keys():
        MinHashMatrix[user] = list()
        for hash in hash_functions:
            MinHashMatrix[user].append(
                min((hash[0] * business_order[business_id] + hash[1]) % business_number for business_id in
                    users[user].keys()))
    return MinHashMatrix


def findCandidates(users_set, MinHashMatrix, b, r):
    """
    :param users: {user1, user2, user3...}
    :param MinHashMatrix: {user1: [order3, order2...], user2: [order4, order15...]}
    :param b: int
    :param r: int
    :return: list
    """
    start = 0
    candidates = []
    for end in range(r, r * b, r):
        print(start, end)
        print(len(users_set))
        if not users_set:
            break
        remove_users = set()
        for comb in combinations(users_set, 2):
            user1, user2 = comb
            if MinHashMatrix[user1][start:end] == MinHashMatrix[user2][start:end]:
                candidates.append((user1, user2))
                remove_users.add(user1)
                remove_users.add(user2)
                print('cand', (user1, user2))
        users_set = users_set - remove_users
        start = end
    return candidates
