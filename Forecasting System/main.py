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
        for model in self.models:
            print(f'-----------------------Running {model.name}-----------------------')
            print(f'Date is {date}')
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

        # predicts = [self.result_DR, self.result_FP]
        # predicts = [self.result_FP, self.result_DR, self.result_TM]
        predict = self.forecast
        # errors = [self.DR_MAPE, self.FP_MAPE]
        # errors = [self.FP_MAPE, self.DR_MAPE, self.TM_MAPE]
        # res = self.ensemble(errors, predicts)
        res = predict
        print(f'predict result: /n {predict}')
        # this_mape = mape(validation_list, self.result_DR)
        # this_rmse = rmse(validation_list, self.result_DR)
        this_mape = helper.mape(validation_list, res)
        this_rmse = helper.rmse(validation_list, res)
        print(f'satrt time: {start}, end time: {end}')
        print(f'future mape: {this_mape}')
        print(f'future rmse: {this_rmse}')


if __name__ == '__main__':
    path = 'Data/Hourly_Temp_Humi_Load-6.csv'
    df = pd.read_csv(path)
    LP = LoadPred(df)
    date = '2018-07-15'
    LP.model_building(date)
    LP.ensemble_models()
    LP.return_result()
    print()
