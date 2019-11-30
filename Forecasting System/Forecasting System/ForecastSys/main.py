from ForecastSys.Models import DR, FP
import pandas as pd


class ForecastSys(object):

    def __init__(self, full_temp_path, orig_temp_path, holiday_path):
        # self.date = date
        self.real = pd.read_csv(full_temp_path)
        self.orig_df = pd.read_excel(orig_temp_path, sheet_name='SCE Load Only', date_parser='Date')
        self.holiday = pd.read_csv(holiday_path)
        self.model_DR = DR.DR(self.real)
        self.model_FP = FP.FP(self.orig_df, self.holiday)

    def run_DR(self, date):
        self.model_DR.model_selection_mape_rmse(date)
        self.model_DR.predict_next_40hours()

    def run_FP(self, date):
        self.model_FP.predict_next_40hours(date)

    def run_TM(self, date):
        pass

    def return_result(self, date):
        self.run_DR(date)
        self.run_FP(date)
        self.run_TM(date)
        self.result_DR, self.DR_MAPE, self.DR_RMSE = self.model_DR.forecast, self.model_DR.train_mape, self.model_DR.train_rmse
        self.result_FP, self.FP_MAPE, self.FP_RMSE = self.model_FP.forecast, self.model_FP.MAPE, self.model_FP.RMSE
        self.result_TM, self.TM_MAPE, self.TM_RMSE = 0, 0, 0

    def combine_result(self):
        pass


if __name__ == '__main__':
    full_temp_path = '../../Data/Hourly_Temp_Humi_Load-6.csv'
    orig_temp_path = '../../Data/20140101-20190901 SCE & CAISO Actual Load  9 27 2019.xlsx'
    holiday = '../../Data/holiday.csv'
    date = '2019-01-16'
    FS = ForecastSys(full_temp_path, orig_temp_path, holiday)
    FS.return_result(date)
    date = '2019-05-03'
    FS.return_result(date)
