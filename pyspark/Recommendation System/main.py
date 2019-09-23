from pyspark import SparkContext
from utils import *
import sys
import time

# train_path = "./Data/yelp_train.csv"
# validation_path = "./Data/yelp_val.csv"
# test_path = "./Data/test.csv"

train_path = sys.argv[1]
validation_path = sys.argv[2]
case_id = int(sys.argv[3])

sc = SparkContext("local[*]", "RS")

sys.stdout.write('Loading Data\n')
trainRDD = sc.textFile(train_path)
# trainRDD = sc.textFile(test_path)
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

# trainRDD.foreach(print)
users_business_rating = dict(user_business.collect())
business_user_rating = dict(business_user.collect())


def main():
    if case_id == 1:
        user_based_cf()
    elif case_id == 2:
        item_based_cf()
    else:
        pass


# -------------------------------------- USER BASED START -------------------------------------- #
def user_based_cf():
    sys.stdout.write('Runing user based CF Recommendation System\n')
    start = time.time()
    header = valRDD.first()
    val_User_RDD = valRDD.filter(lambda x: x != header) \
        .map(lambda line: line.split(",")) \
        .map(lambda lst: (lst[0], [(lst[1], float(lst[2]))])) \
        .reduceByKey(lambda a, b: a + b) \
        .mapValues(dict)
    val_user = dict(val_User_RDD.collect())
    user_average_rating = {user: float(sum(business_rating.values())) / len(business_rating.values()) for
                           user, business_rating in users_business_rating.items()}
    TOP_N = 10
    differences = []
    for user in val_user:
        for business in val_user[user]:
            prediction = Predict_User_Rating_On_a_Business(user,
                                                           business,
                                                           TOP_N,
                                                           users_business_rating,
                                                           business_user_rating,
                                                           user_average_rating)
            differences.append((val_user[user][business] - prediction) ** 2)
    end = time.time()
    sys.stdout.write(f'RMSE is {sum(differences) / len(differences)}\n')
    sys.stdout.write(f'using {round(end - start, 2)} seconds\n')


# -------------------------------------- USER BASED END -------------------------------------- #

# -------------------------------------- ITEM BASED START -------------------------------------- #
def item_based_cf():
    ## Jaccard Similarity based LSH to find candidates
    sys.stdout.write('Runing item based CF Recommendation System\n')
    start = time.time()
    b = 50
    r = 3
    h = b * r
    val_Business_RDD = valRDD.filter(lambda x: x != header) \
        .map(lambda line: line.split(",")) \
        .map(lambda lst: (lst[1], [(lst[0], float(lst[2]))])) \
        .reduceByKey(lambda a, b: a + b) \
        .mapValues(dict)
    val_business = dict(val_Business_RDD.collect())
    business_average_rating = {business: float(sum(user_rated.values())) / len(user_rated.values()) for
                               business, user_rated
                               in business_user_rating.items()}
    user_average_rating = {user: float(sum(business_rating.values())) / len(business_rating.values()) for
                           user, business_rating in users_business_rating.items()}
    user_order = {user: order for order, user in enumerate(users_business_rating.keys())}
    MinHashMatrix = buildMinHashMatrix(business_user_rating, user_order, h)
    candidates = findCandidates_LSH(business_user_rating, MinHashMatrix, b, r)
    TOP_N = 5
    differences = []
    for business in val_business:
        for user in val_business[business]:
            prediction = Predict_Business_Rating_by_a_User(business,
                                                           user,
                                                           candidates,
                                                           TOP_N,
                                                           users_business_rating,
                                                           business_user_rating,
                                                           business_average_rating,
                                                           user_average_rating)
            differences.append((val_business[business][user] - prediction) ** 2)
    end = time.time()
    sys.stdout.write(f'RMSE is {sum(differences) / len(differences)}\n')
    sys.stdout.write(f'using {round(end - start, 2)} seconds\n')


# -------------------------------------- ITEM BASED END -------------------------------------- #


if __name__ == "__main__":
    main()
