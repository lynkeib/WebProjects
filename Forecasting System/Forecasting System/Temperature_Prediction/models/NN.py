__author__ = 'Connor'

'''
things can be improved:
1. if using LSTM, then we should use the lasted data to train our model and use that RMSE and MAPE as the model 
    selection criteria
2. However, LSTM is a kind of a slow model to use
3. Learning Rate can be further tuned 
'''

# from helper import *
import pandas as pd
import datetime
import os
import time
import tensorflow as tf
import numpy as np

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

tensorflow_version = tf.__version__

if int(tensorflow_version.split('.')[0]) <= 1:
    raise RuntimeError('Version Error, need to be greater than 1')


def windowed_dataset(series, window_size, batch_size, shuffle_buffer):
    dataset = tf.data.Dataset.from_tensor_slices(series)
    dataset = dataset.window(window_size, shift=24, drop_remainder=True)
    dataset = dataset.flat_map(lambda window: window.batch(window_size))
    dataset = dataset.shuffle(shuffle_buffer).map(lambda window: (window[:-40], window[-40:]))
    dataset = dataset.batch(batch_size).prefetch(1)
    return dataset


class NN(object):

    def __init__(self, path, date):
        self.date = date

        self.data = pd.read_csv(path)
        DateTime = pd.DataFrame(
            self.data.apply(lambda line: pd.to_datetime(line['Date']) + datetime.timedelta(hours=line['Hour']), axis=1))
        DateTime.columns = ['DateTime']
        self.temp = pd.concat(
            [DateTime, self.data.iloc[:, 2], self.data.loc[:, self.data.columns.str.contains("Temp")]], axis=1)
        self.temp.set_index('DateTime', inplace=True)
        # x_train = self.temp['2014-01-01 07:00':'2016-11-30 23:00'][station + '_Temp'].tolist()

        self.window_size = 337 + 40
        self.batch_size = 30
        self.shuffle_buffer_size = 30

        # self.dataset = windowed_dataset(x_train, self.window_size, self.batch_size, self.shuffle_buffer_size)

    def model_building(self):
        l0 = tf.keras.layers.Dense(100)
        l1 = tf.keras.layers.Dense(40)
        self.model = tf.keras.models.Sequential([l0, l1])
        # self.model = tf.keras.models.Sequential([l1])
        # l0 = tf.keras.layers.Dense(40)
        # self.model = tf.keras.models.Sequential([l0])

        self.model.compile(loss='mean_absolute_percentage_error',
                           optimizer=tf.keras.optimizers.SGD(lr=1e-6, momentum=0.9))
        # self.model.compile(loss='mean_absolute_percentage_error',
        #                    optimizer=tf.keras.optimizers.Adam(lr=1e-6))
        self.model.fit(self.dataset, epochs=20, verbose=0)

    def predict_model_select(self, station='Mean'):
        # try:
        #     pd.to_datetime(date)
        # except:
        #     raise RuntimeError("Date is not correct")
        date = self.date
        self.station = station

        self.training_days = 1

        self.datetime = pd.to_datetime(date) + datetime.timedelta(hours=7)
        self.test_start_date = self.datetime - datetime.timedelta(days=self.training_days + 1)
        self.train_end_date = self.test_start_date - datetime.timedelta(hours=8)
        self.test_end_date = self.datetime - datetime.timedelta(hours=8)

        x_train = self.temp['2014-01-01 07:00':str(self.train_end_date)][self.station + '_Temp'].tolist()
        self.dataset = windowed_dataset(x_train, self.window_size, self.batch_size, self.shuffle_buffer_size)

    def model_selection_mape_rmse(self):
        def mape(y_true, y_pred):
            return np.mean(np.abs((y_pred - y_true) / y_true)) * 100

        def rmse(y_true, y_pred):
            return np.sqrt(np.mean((y_true - y_pred) ** 2))

        # series = np.array(self.temp['2016-11-17 07:00:00':'2016-12-31 23:00']['RIV_Temp'].tolist())
        series = np.array(self.temp[str(self.test_start_date):str(self.test_end_date)][self.station + '_Temp'].tolist())

        this_date = self.test_start_date
        forecast = []
        x_test = []
        for counter in range(self.training_days):
            print('days', counter)
            start = time.time()
            self.train_end_date = this_date - datetime.timedelta(hours=8)
            x_train = self.temp['2014-01-01 07:00':str(self.train_end_date)][self.station + '_Temp'].tolist()
            self.dataset = windowed_dataset(x_train, self.window_size, self.batch_size, self.shuffle_buffer_size)

            X_start, X_end = this_date - datetime.timedelta(days=14), this_date
            Y_start, Y_end = this_date + datetime.timedelta(hours=1), this_date + datetime.timedelta(hours=40)
            series = np.array(self.temp[str(X_start):str(Y_end)][self.station + '_Temp'].tolist())

            print('now', this_date)

            print('train time', '2014-01-01 07:00', str(self.train_end_date))

            print('predict', Y_start, Y_end)

            self.model_building()

            forecast.append(self.model.predict(series[0:0 + self.window_size - 40][np.newaxis]))
            x_test.append(series[0 + self.window_size - 40:0 + self.window_size])
            this_date = this_date + datetime.timedelta(hours=24)
            print('mape', mape(np.array(x_test[-1]), np.array(forecast[-1][0])))
            print('rmse', rmse(np.array(x_test[-1]), np.array(forecast[-1][0])))
            end = time.time()
            print('using', end - start)

        # for time in range(0, len(series) - self.window_size, 24):
        #     forecast.append(self.model.predict(series[time:time + self.window_size - 40][np.newaxis]))
        #     x_test.append(series[time + self.window_size - 40:time + self.window_size])
        #
        self.result_mape = []
        self.result_rmse = []

        for index in range(len(forecast)):
            self.result_mape.append(mape(np.array(x_test[index]), np.array(forecast[index][0])))
            self.result_rmse.append(rmse(np.array(x_test[index]), np.array(forecast[index][0])))

        self.train_mape = np.mean(self.result_mape)
        self.train_rmse = np.mean(self.result_rmse)

        return self.train_mape, self.train_rmse

    def predict_next_40hours(self):
        today = self.datetime

        self.train_end_date = self.datetime - datetime.timedelta(hours=8)

        x_train = self.temp['2014-01-01 07:00':str(self.train_end_date)][self.station + '_Temp'].tolist()

        self.dataset = windowed_dataset(x_train, self.window_size, self.batch_size, self.shuffle_buffer_size)

        print('building the latest model')
        self.model_building()
        print('building process complete')
        X_start = today - datetime.timedelta(days=14)
        X_end = today
        X = np.array(self.temp[str(X_start):str(X_end)][self.station + '_Temp'].tolist())

        self.forecast = self.model.predict(X[np.newaxis])
        return self.forecast


if __name__ == "__main__":
    # path = '../Data/Hourly_Temp_Humi_Load-6.csv'
    # model = NN(path, "Mean")
    # model.predict_model_select('2018-03-04')
    # # model.model_building()
    # mape, rmse = model.model_selection_mape_rmse()
    # print(f'mape: {mape}, rmse: {rmse}')
    # forecast = model.predict_next_40hours()
    # print(forecast)
    path = '../Data/Hourly_Temp_Humi_Load-6.csv'
    model = NN(path, '2018-03-04')
    model.predict_model_select('Mean')
    # model.model_building()
    mape, rmse = model.model_selection_mape_rmse()
    print(f'mape: {mape}, rmse: {rmse}')
    forecast = model.predict_next_40hours()
    print(forecast)
