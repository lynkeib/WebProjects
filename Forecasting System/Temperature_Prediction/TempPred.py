from Temperature_Prediction.Models.DR import DR
from Temperature_Prediction.Models.HW import HW


class TempPred(object):

    def __init__(self, dataframe):
        self.DR = DR(dataframe)
        self.HW = HW(dataframe)
        self.models = [self.DR, self.HW]

    def model_building(self, date, station):
        self.MAPE = []
        self.RMSE = []
        for model in self.models:
            model.set_date(date)
            model.model_selection_mape_rmse(station)
            self.MAPE.append(model.mape)
            self.RMSE.append(model.rmse)

    def ensemble_models(self):
        index = self.MAPE.index(min(self.MAPE))
        self.model = self.models[index]

    def predict_next_40hours_temp(self, station):
        prediction = self.model.predict_next_40hours_temp(station)
        return prediction
