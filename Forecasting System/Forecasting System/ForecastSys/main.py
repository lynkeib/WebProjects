from ForecastSys.Models import DR, FP, TM
import pandas as pd
import datetime
import numpy as np
from functools import reduce


class ForecastSys(object):

    def __init__(self, full_temp_path, orig_temp_path, holiday_path):
        # self.date = date
        self.real = pd.read_csv(full_temp_path)
        self.create_validation_df()
        self.orig_df = pd.read_excel(orig_temp_path, sheet_name='SCE Load Only', date_parser='Date')
        self.holiday = pd.read_csv(holiday_path)
        self.model_DR = DR.DR(self.real)
        self.model_FP = FP.FP(self.orig_df, self.holiday)
        self.model_TM = TM.TM(self.real)

    def create_validation_df(self):
        self.validation_df = self.real.copy()
        DateTime = pd.DataFrame(
            self.validation_df.apply(lambda line: pd.to_datetime(line['Date']) + datetime.timedelta(hours=line['Hour']),
                                     axis=1))
        DateTime.columns = ['DateTime']

        self.validation_df = pd.concat([DateTime, self.real], axis=1)
        self.validation_df = self.validation_df[['DateTime', 'Load']]
        self.validation_df.set_index('DateTime', inplace=True)

    def run_DR(self, date):
        self.model_DR.model_selection_mape_rmse(date)
        self.model_DR.predict_next_40hours()

    def run_FP(self, date):
        self.model_FP.predict_next_40hours(date)

    def run_TM(self, date):
        pass

    def return_result(self, date):
        self.date = date
        self.run_DR(date)
        self.run_FP(date)
        self.run_TM(date)
        self.result_DR, self.DR_MAPE, self.DR_RMSE = self.model_DR.forecast, self.model_DR.train_mape, self.model_DR.train_rmse
        self.result_FP, self.FP_MAPE, self.FP_RMSE = self.model_FP.forecast, self.model_FP.MAPE, self.model_FP.RMSE
        self.result_TM, self.TM_MAPE, self.TM_RMSE = 0, 0, 0

    def combine_result(self):
        pass

    def get_error(self):
        def mape(y_true, y_pred):
            y_true, y_pred = np.array(y_true), np.array(y_pred)
            return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

        def rmse(y_true, y_pred):
            y_true, y_pred = np.array(y_true), np.array(y_pred)
            return np.sqrt(np.mean((y_true - y_pred) ** 2))

        start = pd.to_datetime(self.date) + datetime.timedelta(hours=8)
        end = pd.to_datetime(self.date) + datetime.timedelta(hours=47)
        validation_list = self.validation_df[start:end]['Load'].tolist()
        predicts = [self.result_DR, self.result_FP]
        errors = [self.DR_MAPE, self.FP_MAPE]
        res = self.ensemble(errors, predicts)
        print(res)
        # this_mape = mape(validation_list, self.result_DR)
        # this_rmse = rmse(validation_list, self.result_DR)
        this_mape = mape(validation_list, res)
        this_rmse = rmse(validation_list, res)
        print(start, end)
        print(f'future mape: {this_mape}')
        print(f'future rmse: {this_rmse}')

    def ensemble(self, error_list, result_list):
        weight = list(map(lambda a: 1.0 / a, error_list))
        weight = [error / sum(weight) for error in weight]
        result_list = [np.array(result) for result in result_list]
        print(weight)
        for index in range(len(result_list)):
            result_list[index] = result_list[index] * weight[index]
        res = sum(result_list)
        return res


if __name__ == '__main__':
    full_temp_path = '../../Data/Hourly_Temp_Humi_Load-6.csv'
    orig_temp_path = '../../Data/20140101-20190901 SCE & CAISO Actual Load  9 27 2019.xlsx'
    holiday = '../../Data/holiday.csv'
    FS = ForecastSys(full_temp_path, orig_temp_path, holiday)

    datelist = list(map(str, pd.date_range(pd.to_datetime('2019-01-01'), periods=10).tolist()))

    for date in datelist:
        FS.return_result(date)
        FS.get_error()

    # date = '2019-01-16'
    #
    # FS.return_result(date)
    # FS.get_error()
    # # date = '2019-05-03'
    # FS.return_result(date)
    # FS.get_error()
