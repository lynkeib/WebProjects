import pandas as pd
import numpy as np

from sklearn.ensemble import GradientBoostingRegressor
import datetime
import tensorflow
from Temperature_Prediction.predict import *


class TM(object):

    def __init__(self, data):
        self.df = data.copy()
        self.create_dateframe()

    def create_dateframe(self):
        df = self.df[['Date', 'Hour', 'Load', 'Mean_Temp']]
        df['Date'] = pd.to_datetime(df['Date'])
        df['new_date'] = df.apply(lambda a: a['Date'] + datetime.timedelta(hours=int(a['Hour'])), axis=1)

        df['Weekday'] = df['new_date'].dt.weekday_name
        df['Month'] = df['new_date'].dt.month
        df['Hour'] = df['new_date'].dt.hour
        Weekday_Dummies = pd.get_dummies(df['Weekday'])
        Month_Dummies = pd.get_dummies(df['Month'])
        self.df2 = pd.concat([df.drop(columns=['Weekday', 'Month']), Weekday_Dummies, Month_Dummies], axis=1)

    def predict_Temp_next_40hours(self):
        # self.date = date
        date = self.date
        self.date_hour = pd.to_datetime(date) + datetime.timedelta(hours=7)
        test_start_date = self.date_hour - datetime.timedelta(days=2)
        train_end_date = test_start_date - datetime.timedelta(hours=8)
        test_end_date = self.date_hour - datetime.timedelta(hours=8)
        self.date_for_test = pd.to_datetime(date) - datetime.timedelta(days=1)
        self.prediction_end = self.date_hour + datetime.timedelta(hours=40)

        x_train = self.df2[self.df2['new_date'] <= train_end_date].drop(columns='Load')
        x_test = self.df2[(self.df2['new_date'] > test_start_date) & (self.df2['new_date'] <= test_end_date)].drop(
            columns='Load')
        self.y_train = self.df2[self.df2['new_date'] <= train_end_date]['Load']
        self.y_test = self.df2[(self.df2['new_date'] > test_start_date) & (self.df2['new_date'] <= test_end_date)][
            'Load']

        # temp = TempPred('Hourly_Temp_Humi_Load-6.csv', self.date_for_test)
        temp = TempPred(self.df, self.date_for_test)
        pred = temp.return_result('Mean')

        x_test['Mean_Temp'] = pred

        self.x_train2 = x_train.drop(columns=['Date', 'new_date'])
        self.x_test2 = x_test.drop(columns=['Date', 'new_date'])

    def predict_next_40hours(self, date):
        self.date = date
        self.predict_Temp_next_40hours()

        # def XGBLoadPred(self, data, date):
        # Split train and test
        # Output: a new dataframe, with testing period temerature prediction replaced by NN/HW prediction

        # Model Building & Prediction#
        params = {'n_estimators': 300, 'max_depth': 6, 'min_samples_split': 20, 'learning_rate': .2,
                  'loss': 'ls'}
        GB = GradientBoostingRegressor(**params)
        GB.fit(self.x_train2, self.y_train)
        predict_GB = GB.predict(self.x_test2)

        # MAPE & RMSE
        self.mape = np.mean(np.abs((predict_GB - self.y_test) / self.y_test)) * 100
        self.rmse = np.sqrt(np.mean((self.y_test - predict_GB) ** 2))

        # Predict Next 40 hours
        temp = TempPred(self.df, date)
        pred = temp.return_result('Mean')

        x_next40 = self.df2[(self.df2['new_date'] > self.date_hour) & (self.df2['new_date'] <= self.prediction_end)]
        x_next40_new = x_next40.drop(columns=['Date', 'new_date', 'Load'])

        x_next40_new['Mean_Temp'] = pred

        x_train_new = self.df2[(self.df2['new_date'] < self.date_hour)].drop(columns=['Date', 'new_date', 'Load'])
        y_train_new = self.df2[(self.df2['new_date'] < self.date_hour)]['Load']
        params = {'n_estimators': 300, 'max_depth': 6, 'min_samples_split': 20, 'learning_rate': .2,
                  'loss': 'ls'}
        GB_40 = GradientBoostingRegressor(**params)
        GB_40.fit(x_train_new, y_train_new)
        self.predict_next40 = GB_40.predict(x_next40_new).tolist()

        return self.mape, self.rmse, self.predict_next40
