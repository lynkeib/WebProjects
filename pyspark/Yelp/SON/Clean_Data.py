from pyspark.sql import SparkSession
import json
import pandas as pd

review_path = "/Users/chengyinliu/D/2019_Spring/INF553_ Foundations and Applications of Data Mining/ASSIGNMENTS/WEEK_1/yelp_dataset/review.json"
business_path = '/Users/chengyinliu/D/2019_Spring/INF553_ Foundations and Applications of Data Mining/ASSIGNMENTS/WEEK_1/yelp_dataset/business.json'

ss = SparkSession \
    .builder \
    .appName('Son') \
    .master('local[*]') \
    .getOrCreate()

sc = ss.sparkContext

reviewRDD = sc.textFile(review_path)

review = reviewRDD.map(lambda line: json.loads(line)) \
    .map(lambda line: (line['user_id'], line['business_id'])) \
    .collect()

review_list = list(zip(*review))

businessRDD = sc.textFile(business_path)

business = businessRDD.map(lambda line: json.loads(line)) \
    .map(lambda line: (line['business_id'], line['state'])) \
    .collect()

business_list = list(zip(*business))

review_dict = {"user_id": review_list[0], "business_id": review_list[1]}
business_dict = {"business_id": business_list[0], "state": business_list[1]}

review_df = pd.DataFrame.from_dict(review_dict)
business_df = pd.DataFrame.from_dict(business_dict)

print(review_df.head())
print(business_df.head())

all_df = pd.merge(left=review_df, right=business_df, how='left', left_on=["business_id"], right_on=['business_id'])

print(all_df.head())

all_df_NV = all_df[all_df['state'] == 'NV']

print(all_df_NV.head())

del all_df_NV['state']

all_df_NV.to_csv('task2_data.csv', index=False)
