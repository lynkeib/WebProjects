from datetime import timedelta
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import pandas as pd
import numpy as np


class HW(object):

    def __init__(self, dataframe):
        df = dataframe.copy()

    def set_date(self, date):
        self.date = date

    def model_building(self, training_data, station):
        pass

    def model_selection_mape_rmse(self, station):
        pass

    def predict_next_40hours_temp(self, station):
        pass
