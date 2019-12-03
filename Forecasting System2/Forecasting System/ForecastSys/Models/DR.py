import pandas as pd
import numpy as np
import holidays
from pandas.tseries.holiday import USFederalHolidayCalendar
import datetime
import statsmodels.formula.api as sm
import time


class DR(object):

    def __init__(self, data_df):
        # df = pd.read_csv(path, date_parser='Date')
        df = data_df.copy()
        test = df[['Date', 'Hour', 'Weekday', 'Month', 'Load', 'Mean_Temp', 'Mean_Humi']]

        test.loc[:, 'Load_Log'] = np.log(df['Load'])

        test['Load_Lag_48'] = test['Load_Log'].shift(48, axis=0)
        test['Temp_Lag_48'] = test['Mean_Temp'].shift(48, axis=0)
        test['Humi_Lag_48'] = test['Mean_Humi'].shift(48, axis=0)

        cal = USFederalHolidayCalendar()

        holidays = cal.holidays(start='2014-01-01', end=str(datetime.datetime.now()), return_name=True)

        holidays = pd.DataFrame(holidays)

        holidays = holidays.reset_index()
        holidays = holidays.rename(columns={'index': "Date", 0: 'Holiday'})
        holidays['Date'] = pd.to_datetime(holidays['Date'])
        holidays.head(2)

        test['Date'] = pd.to_datetime(test['Date'])
        lm_data = test.loc[49:len(test), ].merge(holidays, how='left', on='Date')
        lm_data['Holiday'] = lm_data['Holiday'].fillna("Not Holiday")

        lm_data[["Hour", "Weekday", "Month", "Holiday"]] = lm_data[["Hour", "Weekday", "Month", "Holiday"]].astype(
            'category')

        DateTime = pd.DataFrame(
            lm_data.apply(lambda line: pd.to_datetime(line['Date']) + datetime.timedelta(hours=line['Hour']), axis=1))
        DateTime.columns = ['DateTime']

        self.lm_data = pd.concat([DateTime, lm_data], axis=1)
        self.lm_data.set_index('DateTime', inplace=True)

    def model_building(self, x_train):
        ml = sm.ols(formula="Load_Log~Temp_Lag_48+Humi_Lag_48+I(Temp_Lag_48**2)+I(Humi_Lag_48**2)+\
                           Hour+Weekday+Month+Holiday+\
                               Month:Temp_Lag_48+Month:Humi_Lag_48+\
                               Hour:Temp_Lag_48+Hour:Humi_Lag_48+\
                               Holiday:Temp_Lag_48+Holiday:Humi_Lag_48", data=x_train).fit()
        return ml

    def model_selection_mape_rmse(self, date):
        def mape(y_true, y_pred):
            y_true, y_pred = np.array(y_true), np.array(y_pred)
            return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

        def rmse(y_true, y_pred):
            y_true, y_pred = np.array(y_true), np.array(y_pred)
            return np.sqrt(np.mean((y_true - y_pred) ** 2))

        self.training_days = 30

        self.datetime = pd.to_datetime(date) + datetime.timedelta(hours=7)
        self.test_start_date = self.datetime - datetime.timedelta(days=self.training_days + 1)
        self.train_end_date = self.test_start_date - datetime.timedelta(hours=8)
        self.test_end_date = self.datetime - datetime.timedelta(hours=8)

        forecast = []
        x_test = []
        this_date = self.test_start_date
        for counter in range(self.training_days):
            self.train_end_date = this_date
            # print('days', counter)
            # print('now', this_date)

            # print('train time', '2014-01-01 07:00', str(self.train_end_date))
            Y_start, Y_end = this_date + datetime.timedelta(hours=1), this_date + datetime.timedelta(hours=40)
            # print('predict', Y_start, Y_end)

            start = time.time()

            x_train = self.lm_data['2014-01-03 01:00':str(self.train_end_date)]

            ml = self.model_building(x_train)
            test = self.lm_data[str(Y_start):str(Y_end)]
            p = ml.predict(test)
            p = pd.DataFrame(p)
            forecast.append(np.array(np.exp(p[0])))
            x_test.append(np.array(test['Load']))

            # print(p)

            # print('mape', mean_absolute_percentage_error(test['Load'], np.exp(p[0])))
            # t = np.exp(p[0])

            # print('rmse', rmse(test['Load'], np.exp(p[0])))
            # print('mape', mape(test['Load'], np.exp(p[0])))

            end = time.time()
            # print('using', end - start)
            this_date = this_date + datetime.timedelta(hours=24)
            # print()

        self.result_mape = []
        self.result_rmse = []

        # print('forecast', forecast)
        # print('x_test', x_test)

        for index in range(len(forecast)):
            self.result_mape.append(
                mape(np.array(x_test[index]), np.array(forecast[index])))
            self.result_rmse.append(rmse(np.array(x_test[index]), np.array(forecast[index])))

        self.train_mape = np.mean(self.result_mape)
        self.train_rmse = np.mean(self.result_rmse)

        return self.train_mape, self.train_rmse

    def predict_next_40hours(self):
        today = self.datetime

        self.train_end_date = self.datetime - datetime.timedelta(hours=1)

        x_train = self.lm_data['2014-01-03 01:00':str(self.train_end_date)]

        # self.dataset = windowed_dataset(x_train, self.window_size, self.batch_size, self.shuffle_buffer_size)

        print('building the latest model')
        # self.model_building()
        ml = self.model_building(x_train)
        print('building process complete')

        Y_start, Y_end = today + datetime.timedelta(hours=1), today + datetime.timedelta(hours=40)
        X = self.lm_data[str(Y_start):str(Y_end)]
        p = ml.predict(X)
        p = pd.DataFrame(p)
        p = np.exp(p[0])
        self.forecast = p.tolist()
        return p


if __name__ == "__main__":
    path = '../../../Data/Hourly_Temp_Humi_Load-6.csv'
    model = DR(path)
    mape, rmse = model.model_selection_mape_rmse('2018-03-04')
    # model.model_building()
    # mape, rmse = model.model_selection_mape_rmse()
    print(f'mape: {mape}, rmse: {rmse}')
    forecast = model.predict_next_40hours()
    print(forecast)
