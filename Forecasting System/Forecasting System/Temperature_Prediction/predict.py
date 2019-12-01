from Temperature_Prediction.models import NN, HW
import time


class TempPred(object):

    def __init__(self, file_path_df, date):
        # model initialize
        self.model_NN = NN.NN(file_path_df, date)
        self.model_HW = HW.HW(file_path_df, date)
        self.HWrun = False

    def predict_next_40hours_NN(self, station='Mean'):
        # path = '../Data/Hourly_Temp_Humi_Load-6.csv'
        # model = NN(path, '2018-03-04')
        self.model_NN.predict_model_select(station)
        # model.model_building()
        self.model_NN.model_selection_mape_rmse()

        self.model_NN.predict_next_40hours()
        # print(forecast)

    def predict_next_40hours_HW(self):
        self.HWrun = True
        self.model_HW.predict_next_40hours()

    def return_result(self, station='Mean'):
        if self.HWrun:
            self.predict_next_40hours_NN(station)
            RMSE_NN, MAPE_NN = self.model_NN.train_rmse, self.model_NN.train_mape
            RMSE_HW, MAPE_HW = self.model_HW.RMSE, self.model_HW.MAPE
            if RMSE_NN > RMSE_HW:
                return self.model_HW.prediction.tolist()
            else:
                return self.model_NN.forecast[0]
        else:
            self.predict_next_40hours_NN(station)
            self.predict_next_40hours_HW()
            RMSE_NN, MAPE_NN = self.model_NN.train_rmse, self.model_NN.train_mape
            RMSE_HW, MAPE_HW = self.model_HW.RMSE, self.model_HW.MAPE
            if MAPE_NN > MAPE_HW:
                return self.model_HW.prediction.tolist()
            else:
                return self.model_NN.forecast[0]


if __name__ == '__main__':
    start = time.time()
    this = TempPred('../../Data/Hourly_Temp_Humi_Load-6.csv', '2018-04-02')
    pred = this.return_result("RIV")
    end = time.time()
    print(f'HW_RMSE: {this.model_HW.RMSE}, HW_MAPE: {this.model_HW.MAPE}')
    print(f"NN_RMSE: {this.model_NN.train_rmse}, NN_MAPE: {this.model_NN.train_mape}")
    print(f'time: {end - start}')
    print(pred)
