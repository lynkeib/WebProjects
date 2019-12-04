from Models import NN, DR, TM
from Helper import helper

import pandas as pd
import datetime
import time
import numpy as np


class LoadPred(object):

    def __init__(self, dataframe):
        self.data = dataframe.copy()
        self.NN = NN.NN(self.data)
        self.DR = DR.DR(self.data)
        self.TM = TM.TM(self.data)
        self.models = [self.NN, self.DR, self.TM]

    def create_validation_df(self):
        self.validation_df = helper.validation_dataframe_cleaning(self.data)

    def model_building(self, date):
        self.date = date
        self.MAPE = []
        self.RMSE = []
        exclude_mode = [self.NN.name, self.TM.name]
        for model in self.models:
            print(f'-----------------------Running {model.name}-----------------------')
            print(f'Date is {date}')
            if model.name in exclude_mode:
                self.MAPE.append(float('inf'))
                self.RMSE.append(float('inf'))
                print(f'-----------------------{model.name} Complete-----------------------')
                continue
            start = time.time()
            model.set_date(date)
            model.model_selection_mape_rmse()
            model.predict_next_40hours()
            self.MAPE.append(model.mape)
            self.RMSE.append(model.rmse)
            end = time.time()
            print(f'-----------------------{model.name} Complete-----------------------')
            print(f'Status report: using {end - start} seconds')
            print('************************************************************************************')

    def ensemble_models(self):
        index = self.MAPE.index(min(self.MAPE))
        self.model = self.models[index]

    def return_result(self):
        self.forecast = self.model.predict_next_40hours()
        return self.forecast

    def get_error(self):
        start = pd.to_datetime(self.date) + datetime.timedelta(hours=8)
        end = pd.to_datetime(self.date) + datetime.timedelta(hours=47)
        validation_list = self.validation_df[start:end]['Load'].tolist()
        predict = self.forecast
        res = predict
        print(f'predict result: \n {predict}')
        this_mape = helper.mape(validation_list, res)
        this_rmse = helper.rmse(validation_list, res)
        print(f'satrt time: {start}, end time: {end}')
        print(f'future mape: {this_mape}')
        print(f'future rmse: {this_rmse}')

    def peakhour(self):
        start = pd.to_datetime(self.date) + datetime.timedelta(hours=8)
        end = pd.to_datetime(self.date) + datetime.timedelta(hours=47)
        validation_list = self.validation_df[start:end]['Load'].tolist()
        predict = self.forecast
        validation_list = validation_list[-24:]
        predict = predict[-24:]
        validation_peak_index = validation_list.index(max(validation_list))
        predict_peak_index = predict.index(max(predict))
        if validation_peak_index == predict_peak_index:
            return 1
        else:
            return 0


def main():
    pass


if __name__ == '__main__':
    path = 'Data/Hourly_Temp_Humi_Load-6.csv'
    df = pd.read_csv(path)
    LP = LoadPred(df)
    start = time.time()

    datelist = list(map(str, pd.date_range(pd.to_datetime('2019-03-07'), periods=10).tolist()))

    for date in datelist:
        print('####################################################################################################')
        print(f'Making prediction for {date}')
        start = time.time()
        LP.model_building(date)
        LP.create_validation_df()
        LP.ensemble_models()
        LP.return_result()
        LP.get_error()
        print(f'peak hour: {LP.peakhour()}')
        end = time.time()
        print(f'used {end - start}')
        print('####################################################################################################')
