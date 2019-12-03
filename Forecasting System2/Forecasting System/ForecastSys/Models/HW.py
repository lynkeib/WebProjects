from datetime import timedelta
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
import datetime
from ForecastSys.Models.Temperature_Prediction.DR import *


class HW(object):

    def __init__(self, path_df, date):
        # self.data = pd.read_csv(path)
        self.data = path_df.copy()
        self.date = date
        df = self.data[
            ['Date', 'Hour', 'Load', 'RIV_Temp', 'LAX_Temp', 'USC_Temp', 'WJF_Temp', 'TRM_Temp', 'Weekday', 'Month']]
        df['Date'] = pd.to_datetime(df['Date'])
        df['new_date'] = df.apply(lambda a: a['Date'] + datetime.timedelta(hours=int(a['Hour'])), axis=1)

        Weekday_Dummies = pd.get_dummies(df['Weekday'])
        Month_Dummies = pd.get_dummies(df['Month'])
        df2 = pd.concat([df.drop(columns=['Weekday', 'Month']), Weekday_Dummies, Month_Dummies], axis=1)
        self.data = df2


    def predict_next_40hours(self):
        # import data file
        df2 = self.data  # change to version 6
        date = self.date
        # creat timestamp
        date_hour = pd.to_datetime(date) + datetime.timedelta(hours=7)
        test_start_date = date_hour - datetime.timedelta(days=2)
        train_end_date = test_start_date - datetime.timedelta(hours=8)
        test_end_date = date_hour - datetime.timedelta(hours=8)
        date_for_test = pd.to_datetime(date) - datetime.timedelta(days=1)
        prediction_end = date_hour + datetime.timedelta(hours=40)

        x_train = df2[df2['new_date'] <= train_end_date].drop(columns='Load')
        x_test = df2[(df2['new_date'] > test_start_date) & (df2['new_date'] <= test_end_date)].drop(columns='Load')
        y_train = df2[df2['new_date'] <= train_end_date]['Load']
        y_test = df2[(df2['new_date'] > test_start_date) & (df2['new_date'] <= test_end_date)]['Load']

        stations = ['RIV', 'LAX', 'USC', 'WJF', 'TRM']
        temp = DR(self.data, date_for_test)
        for station in stations:
            temp.model_building()
            # temp = TempPred('Hourly_Temp_Humi_Load-6.csv', date_for_test)
            pred = temp.return_result(station)
            x_test[station + '_Temp'] = pred

        x_train2 = x_train.drop(columns=['Date', 'new_date'])
        x_test2 = x_test.drop(columns=['Date', 'new_date'])

        # Model Building & Prediction#
        params = {'n_estimators': 300, 'max_depth': 6, 'min_samples_split': 20, 'learning_rate': .2,
                  'loss': 'ls'}
        GB = GradientBoostingRegressor(**params)
        GB.fit(x_train2, y_train)
        predict_GB = GB.predict(x_test2)

        # MAPE & RMSE
        mape = np.mean(np.abs((predict_GB - y_test) / y_test)) * 100
        rmse = np.sqrt(np.mean((y_test - predict_GB) ** 2))

        # Predict Next 40 hours
        x_next40 = df2[(df2['new_date'] > date_hour) & (df2['new_date'] <= prediction_end)]
        x_next40_new = x_next40.drop(columns=['Date', 'new_date', 'Load'])

        stations = ['RIV', 'LAX', 'USC', 'WJF', 'TRM']
        for station in stations:
            temp = TempPred('Hourly_Temp_Humi_Load-6.csv', date)
            pred = temp.return_result(station)
            x_next40_new[station + '_Temp'] = pred

        x_train_new = df2[(df2['new_date'] < date_hour)].drop(columns=['Date', 'new_date', 'Load'])
        y_train_new = df2[(df2['new_date'] < date_hour)]['Load']
        params = {'n_estimators': 300, 'max_depth': 6, 'min_samples_split': 20, 'learning_rate': .2,
                  'loss': 'ls'}
        GB_40 = GradientBoostingRegressor(**params)
        GB_40.fit(x_train_new, y_train_new)
        predict_next40 = GB_40.predict(x_next40_new)

        return mape, rmse, predict_next40


if __name__ == '__main__':
    path = "../../../Data/Hourly_Temp_Humi_Load-6.csv"
    model_HW = HW(path, '2018-03-24')
    MAPE, RMSE, y_predict = model_HW.predict_next_40hours()
    print('MAPE', MAPE)
    print("RMSE", RMSE)
    print(y_predict.tolist())
