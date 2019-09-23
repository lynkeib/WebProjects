import random
from itertools import combinations
from collections import defaultdict
import sys
import heapq


# -------------------------------------- USER BASED HELPER FUNCTIONS START -------------------------------------- #
def Calculate_Pearson_Similarity_User(user1, user2, user_business_rating):
    """
    :param user1: string
    :param user2: string
    :param user_business_rating:  {user1: {business_id1: rating1, business_id2: rating2}, user2: {business_id1: rating1, business_id2: rating2}...}
    :return: float
    """
    # sys.stdout.write(f"Calculating Pearson Similarity for user {user1} and user {user2}\n")
    # Step 1: find co-rated businesses
    user1_rated_businesses = set(user_business_rating[user1].keys())
    user2_rated_businesses = set(user_business_rating[user2].keys())
    co_rated_businesses = user1_rated_businesses & user2_rated_businesses
    ## if do not have co_rated_businesses, then the Similarity is 0
    if len(co_rated_businesses) == 0:
        return 0.0

    # Step 2: calculate the average rating on co_rated_business
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
    if Denominator == 0 or Numerator == 0:
        return 1.0
    else:
        return Numerator / Denominator


def Predict_User_Rating_On_a_Business(user, business, TOP_N, user_business_rating, business_user_rating,
                                      user_average_rating):
    """
    :param user: string
    :param business: string
    :param TOP_N: int
    :param user_business_rating: {user1: {business_id1: rating1, business_id2: rating2}, user2: {business_id1: rating1, business_id2: rating2}...}
    :param business_user_rating: {business_id1: {user1: rating1, user2: rating2}, business_id2: {user1: rating1, user2: rating2}...}
    :param user_average_rating: {user1: rating1, user2: rating2...}
    :return: float
    """
    # sys.stdout.write(f"Predicting ratings for user {user} on business {business}\n")
    # Step 1: find users who rated this business
    ## if this business never showed up, then use the user average rating
    if business not in business_user_rating:
        return user_average_rating[user]
    users_rated_this_business = set(business_user_rating[business].keys())
    ## if no users rated this business, then use the user average as an estimation
    if len(users_rated_this_business) == 0:
        return user_average_rating[user]

    # Step 2: calculate the Pearson Correlation Coefficient between them (Using heap)
    # sorted_users = []
    # for other_user in users_rated_this_business:
    #     pearson_correlation_value = Calculate_Pearson_Similarity_User(user, other_user, user_business_rating)
    #     sorted_users.append((pearson_correlation_value, other_user))
    heap = []
    # heap structure: (abs(pearson_correlation_value), pearson_correlation_value, other_user)
    for other_user in users_rated_this_business:
        pearson_correlation_value = Calculate_Pearson_Similarity_User(user, other_user, user_business_rating)
        if not heap or len(heap) < TOP_N:
            heapq.heappush(heap, (abs(pearson_correlation_value), pearson_correlation_value, other_user))
        else:
            if abs(pearson_correlation_value) > heap[0][0]:
                heapq.heappushpop(heap, (abs(pearson_correlation_value), pearson_correlation_value, other_user))

    # Step 3: Select Top N Users (Neighborhood)
    # sorted_users.sort(key=lambda pair: abs(pair[0]), reverse=True)
    # Top_N_users = sorted_users[:TOP_N]
    Top_N_users = [(pearson_correlation_value, other_user) for absolute, pearson_correlation_value, other_user in heap]

    # Step 4: Calculate Numerator and Denominator
    Numerator = sum(
        (user_business_rating[other_user][business] - user_average_rating[other_user]) * pearson_correlation_value
        for pearson_correlation_value, other_user in Top_N_users)

    Denominator = sum(abs(pearson_correlation_value) for pearson_correlation_value, other_user in Top_N_users)

    ## if Denominator is 0, then the best estimation is the average of this user
    if Denominator == 0:
        return user_average_rating[user]
    else:
        return user_average_rating[user] + (float(Numerator) / Denominator)


# -------------------------------------- USER BASED HELPER FUNCTIONS END -------------------------------------- #

# -------------------------------------- ITEM BASED HELPER FUNCTIONS START -------------------------------------- #

def hash_generator(num):
    # sys.stdout.write("generating hash functions\n")
    hash_functions = [(random.choice(range(1, 1001)), random.choice(range(1, 1001))) for _ in range(num)]
    return hash_functions


def buildMinHashMatrix(business_user_rating, user_order, numer_of_hashfunc):
    """
    :param business_user_rating: {business_id1: {user1: rating1, user2: rating2}, business_id2: {user1: rating1, user2: rating2}...}
    :param user_order: {user1: order1, user2: order2...}
    :param numer_of_hashfunc: int
    :return: {user1: [order3, order2...], user2: [order4, order15...]}
    """
    # sys.stdout.write("Building MinHash Matrix\n")
    hash_functions = hash_generator(numer_of_hashfunc)
    MinHashMatrix = dict()
    number_of_total_users = len(user_order)
    count = 1
    total_business = len(business_user_rating)
    for business in business_user_rating.keys():
        # print(f"building {business}'s signature, left {total_business - count}")
        MinHashMatrix[business] = list()
        for hash in hash_functions:
            MinHashMatrix[business].append(
                min((hash[0] * user_order[user] + hash[1]) % number_of_total_users for user in
                    business_user_rating[business].keys()))
        count += 1
    return MinHashMatrix


def JaccardSimilarity(business1, business2, business_user_rating):
    """
    :param business1: string
    :param business2: string
    :param business_user_rating: {business_id1: {user1: rating1, user2: rating2}, business_id2: {user1: rating1, user2: rating2}...}
    :return: float
    """
    # sys.stdout.write(f"Calculating Jaccard Similarity for business {business1} and business {business2}\n")
    user_set_buisness1 = set(business_user_rating[business1].keys())
    user_set_buisness2 = set(business_user_rating[business2].keys())
    return len((user_set_buisness1 & user_set_buisness2)) / float(len(user_set_buisness1 | user_set_buisness2))


def findCandidates_LSH(business_user_rating, MinHashMatrix, b, r):
    """
    :param business_user_rating: {business_id1: {user1: rating1, user2: rating2}, business_id2: {user1: rating1, user2: rating2}...}
    :param MinHashMatrix: {business1: [signature1, signature2...], business2: [signature1, signature2...]}
    :param b: int
    :param r: int
    :return: {business1: {business2, business4}, business2: {business13}...}
    """
    # sys.stdout.write("Using Jaccard based LSH to find candidates\n")
    ## since we only consider two business ids who have at least one identical signature in on band
    ## therefore, we first create all the bands, then, create hash busket for each band

    # Step 1: Create bands
    print('Creating bands')
    bands = dict()
    for band_index in range(b):
        bands[band_index] = defaultdict(list)

    # Step 2: In each band, collect the business ids who's signatures are identical
    print('hashing signatures in each bands')
    for band_index in range(b):
        # print(f'----hashing band {band_index}, left {b - band_index - 1}')
        for business in business_user_rating.keys():
            business_signature_in_this_band = tuple(MinHashMatrix[business][band_index:band_index + r])
            bands[band_index][business_signature_in_this_band].append(business)

    # Step 3: Collect candidates in each band who hashed into the same basket
    print('Creating candidates')
    candidates_LSH = set()
    for band_index in range(b):
        # print(f'----creating candidates in band {band_index}, left {b - band_index - 1}')
        for band_signature in bands[band_index]:
            bands_candidates = bands[band_index][band_signature]
            if len(bands_candidates) > 1:
                for comb in combinations(bands_candidates, 2):
                    candidates_LSH.add(frozenset(comb))

    # Step 4: Use Jaccard Similarity to do the further filter
    candidates_Jaccard = []
    for candidate in candidates_LSH:
        candidate = tuple(candidate)
        if JaccardSimilarity(candidate[0], candidate[1], business_user_rating) >= 0.5:
            candidates_Jaccard.append(candidate)

    # Step 5: Integrate the result into a dictionary
    candidates = defaultdict(set)
    for candidate in candidates_Jaccard:
        business1 = candidate[0]
        business2 = candidate[1]
        candidates[business1].add(business2)
        candidates[business2].add(business1)

    return candidates


def Calculate_Pearson_Similarity_Business(business1, business2, business_user_rating, candidates):
    """
    :param business1: string
    :param business2: string
    :param business_user_rating: {business_id1: {user1: rating1, user2: rating2}, business_id2: {user1: rating1, user2: rating2}...}
    :param candidates: {business1: {business2, business4}, business2: {business13}...}
    :return: float
    """
    # sys.stdout.write(f"Calculating Pearson Similarity for business {business1} and business {business2}\n")
    # Step 0: determine whether this two business is in our candidates
    if business2 not in candidates[business1]:
        return 0.0

    # Step 1: find co-rated users
    business1_rated_by_users = set(business_user_rating[business1].keys())
    business2_rated_by_users = set(business_user_rating[business2].keys())
    co_rated_users = business1_rated_by_users & business2_rated_by_users
    ## if we do not have co_rated_businesses, then the Similarity is 0 (should not happen)
    if len(co_rated_users) == 0:
        return 0.0

    # Step 2: calculate the average rating rated by co_rated_users
    business1_rated_by_co_users = float(sum(
        rating for user, rating in business_user_rating[business1].items() if user in co_rated_users)) / len(
        co_rated_users)
    business2_rated_by_co_users = float(sum(
        rating for user, rating in business_user_rating[business2].items() if user in co_rated_users)) / len(
        co_rated_users)

    # Step 3: calculate Numerator and Denominator
    Numerator = float(sum((business_user_rating[business1][user] - business1_rated_by_co_users) * (
            business_user_rating[business2][user] - business2_rated_by_co_users) for user in co_rated_users))
    Denominator = sum(
        (business_user_rating[business1][user] - business1_rated_by_co_users) ** 2 for user in co_rated_users) ** (
                          1.0 / 2) * sum(
        (business_user_rating[business2][user] - business2_rated_by_co_users) ** 2 for user in co_rated_users) ** (
                          1.0 / 2)
    ## if Denominator is 0
    if Denominator == 0 or Numerator == 0:
        return 1.0
    else:
        return Numerator / Denominator


def Predict_Business_Rating_by_a_User(business, user, candidates, TOP_N, user_business_rating, business_user_rating,
                                      business_average_rating, user_average_rating):
    """
    :param business: string
    :param user: string
    :param candidates: {business1: {business2, business4}, business2: {business13}...}
    :param TOP_N: int
    :param user_business_rating: {user1: {business_id1: rating1, business_id2: rating2}, user2: {business_id1: rating1, business_id2: rating2}...}
    :param business_user_rating: {business_id1: {user1: rating1, user2: rating2}, business_id2: {user1: rating1, user2: rating2}...}
    :param business_average_rating: {business1: rating1, business2: rating2...}
    :param user_average_rating: {user1: rating1, user2: rating2...}
    :return: float
    """
    # sys.stdout.write(f"Predicting ratings for user {user} on business {business}\n")
    # Step 1: find businesses this user rated
    ## if this business never showed up, then use the user average rating
    if business not in business_user_rating:
        return user_average_rating[user]
    ## if this user never showed up, then use the business average rating
    if user not in user_business_rating:
        return business_average_rating[business]
    businesses_rated_by_this_user = set(user_business_rating[user].keys())

    # Step 2: calculate the Pearson Correlation Coefficient between them (only consider the business in candidates)
    sorted_businesses = []
    for other_business in businesses_rated_by_this_user:
        pearson_correlation_value = Calculate_Pearson_Similarity_Business(business, other_business,
                                                                          business_user_rating, candidates)
        sorted_businesses.append((pearson_correlation_value, other_business))

    # Step 3: Select Top N Users (Neighborhood)
    sorted_businesses.sort(key=lambda pair: abs(pair[0]), reverse=True)
    Top_N_businesses = sorted_businesses[:TOP_N]

    # Step 4: Calculate Numerator and Denominator
    Numerator = sum(business_user_rating[other_business][user] * pearson_correlation_value for
                    pearson_correlation_value, other_business in Top_N_businesses)

    Denominator = sum(abs(pearson_correlation_value) for pearson_correlation_value, other_business in Top_N_businesses)

    ## if Denominator is 0, then the best estimation is the average of this user
    if Denominator == 0:
        return business_average_rating[business]
    else:
        return float(Numerator) / Denominator
