import pandas as pd
from datetime import timedelta
from statsmodels.tsa.holtwinters import ExponentialSmoothing


class HoltsWinter(object):

    def __init__(self, path):


def HoltsWinter(file, date):
    # import data file
    data = pd.read_csv(file)  # change to version 6

    # creat timestamp
    DateTime = pd.DataFrame(
        data.apply(lambda line: pd.to_datetime(line['Date']) + timedelta(hours=line['Hour']), axis=1))
    DateTime.columns = ['DateTime']
    temp = pd.concat(
        [DateTime, data.iloc[:, 2], data.loc[:, data.columns.str.contains("Temp")]], axis=1)
    temp.set_index('DateTime', inplace=True)

    datetime = pd.to_datetime(date)
    train_end = datetime + timedelta(hours=7)
    test_start = datetime + timedelta(hours=8)
    test_end = datetime + timedelta(days=1) + timedelta(hours=23)

    train = temp['Mean_Temp'].loc[:train_end]
    test = temp['Mean_Temp'].loc[test_start:test_end]

    # model
    model = ExponentialSmoothing(train, seasonal='add', seasonal_periods=24 * 365)

    # fit model
    model_fit = model.fit()

    yhat = model_fit.forecast(40)
    yhat.index = test.index

    MAPE = abs((yhat - test) / test).mean()
    RMSE = np.sqrt(((yhat - test) ** 2).mean())

    return MAPE, RMSE, yhat
