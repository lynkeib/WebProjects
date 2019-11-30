from ForecastSys.Models import DR, FP


class ForecastSys(object):

    def __init__(self, full_temp_path, orig_temp_path, holiday_path, date, station='Mean'):
        self.date = date
        self.model_DR = DR.DR(full_temp_path)
        self.model_FP = FP.FP(orig_temp_path, holiday_path, self.date)

    def run_DR(self):
        self.model_DR.model_selection_mape_rmse(self.date)
        self.model_DR.predict_next_40hours()

    def run_FP(self):
        self.model_FP.predict_next_40hours()

    def run_TM(self):
        pass

    def return_result(self):
        self.run_DR()
        self.run_FP()
        self.run_TM()
        self.result_DR, self.DR_MAPE, self.DR_RMSE = self.model_DR.forecast, self.model_DR.train_mape, self.model_DR.train_rmse
        self.result_FP, self.FP_MAPE, self.FP_RMSE = self.model_FP.forecast, self.model_FP.MAPE, self.model_FP.RMSE
        self.result_TM, self.TM_MAPE, self.TM_RMSE = 0, 0, 0

    def combine_result(self):
        pass


if __name__ == '__main__':
    full_temp_path = '../../Data/Hourly_Temp_Humi_Load-6.csv'
    orig_temp_path = '../../Data/20140101-20190901 SCE & CAISO Actual Load  9 27 2019.xlsx'
    holiday = '../../Data/holiday.csv'

    FS = ForecastSys(full_temp_path, orig_temp_path, holiday, '2019-01-16')
    FS.return_result()
