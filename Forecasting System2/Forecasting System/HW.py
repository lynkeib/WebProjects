from datetime import timedelta
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import pandas as pd
import numpy as np


class HW(object):

    def __init__(self, path, date):
        self.data = pd.read_csv(path)
        self.date = date

    def predict_next_40hours(self):
        # import data file
        data = self.data  # change to version 6
        date = self.date
        # creat timestamp
        DateTime = pd.DataFrame(
            data.apply(lambda line: pd.to_datetime(line['Date']) + timedelta(hours=line['Hour']), axis=1))
        DateTime.columns = ['DateTime']
        temp = pd.concat(
            [DateTime, data.iloc[:, 2], data.loc[:, data.columns.str.contains("Temp")]], axis=1)
        temp.set_index('DateTime', inplace=True)

        datetime = pd.to_datetime(date) - timedelta(days=2)
        train_end = datetime + timedelta(hours=7)
        test_start = datetime + timedelta(hours=8)
        test_end = datetime + timedelta(days=1) + timedelta(hours=23)

        train = temp['Mean_Temp'].loc[:train_end]
        test = temp['Mean_Temp'].loc[test_start:test_end]

        train_end2 = pd.to_datetime(date) + timedelta(hours=7)
        train2 = temp['Mean_Temp'].loc[:train_end2]
        # model for training and testing
        model = ExponentialSmoothing(train, seasonal='add', seasonal_periods=24 * 365)
        model_fit = model.fit()
        yhat = model_fit.forecast(40)
        yhat.index = test.index

        MAPE = abs((yhat - test) / test).mean()
        RMSE = np.sqrt(((yhat - test) ** 2).mean())

        # model for prediction
        model2 = ExponentialSmoothing(train2, seasonal='add', seasonal_periods=24 * 365)
        model_fit2 = model2.fit()
        y_predict = model_fit2.forecast(40)

        self.MAPE = MAPE
        self.RMSE = RMSE
        self.prediction = y_predict

        return MAPE, RMSE, y_predict


if __name__ == '__main__':
    path = "../Data/Hourly_Temp_Humi_Load-6.csv"
    model_HW = HW(path, '2018-03-24')
    MAPE, RMSE, y_predict = model_HW.predict_next_40hours()
    print('MAPE', MAPE)
    print("RMSE", RMSE)
    print(y_predict)
