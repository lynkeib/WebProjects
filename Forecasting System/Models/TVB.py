import pandas as pd
from Helper import helper
import datetime
import time
import statsmodels.formula.api as sm
import numpy as np
from sklearn.linear_model import LinearRegression
import json

data = pd.read_csv('../Data/Hourly_Temp_Humi_Load-7.csv')

lm_data = helper.DR_Temp_data_cleaning(data)

temp = dict()
for date in pd.date_range('2017-01-01', '2019-08-30', freq='D'):
    start = time.time()
    this_date = date + datetime.timedelta(hours=7)
    training_data = lm_data[:this_date]
    station = 'Mean'
    ml = sm.ols(formula=station + "_Temp_Log~Load_Lag_48+Humi_Lag_48+I(Load_Lag_48**2)+I(Humi_Lag_48**2)+\
                                           Hour+Weekday+Month+Holiday+" + station + "_Temp_Log_Lag_48+I(" + station + "_Temp_Log_Lag_48**2)+\
                                               Month:Load_Lag_48+Month:Humi_Lag_48+\
                                               Hour:Load_Lag_48+Hour:Humi_Lag_48+\
                                               Holiday:Load_Lag_48+Holiday:Humi_Lag_48", data=training_data).fit()

    Y_start = this_date + datetime.timedelta(hours=1)
    Y_end = this_date + datetime.timedelta(hours=40)
    next_ = lm_data[Y_start:Y_end]
    pred = ml.predict(next_)
    temp[this_date] = np.exp(pred)
    end = time.time()
#     print(end - start)
#     print(np.exp(pred))

data = lm_data.reset_index()
data = data[['Load', 'DateTime', 'Mean_Temp']][:]
data.rename(columns={'Mean_Temp': "Temperature"}, inplace=True)

all_begin = pd.to_datetime('2014-01-03 01:00:00')

this_date = pd.to_datetime('2017-01-01 07:00:00')

end_of_running = pd.to_datetime('2017-12-31 07:00:00')

results = dict()

while this_date <= end_of_running:
    print(f'date is {this_date}')
    start = time.time()

    this_data = data.copy()
    this_data.set_index('DateTime', inplace=True)

    date = this_date - datetime.timedelta(hours=7)

    results[date] = dict()
    results[date]['error'] = dict()

    end_this_date = this_date + datetime.timedelta(hours=40)
    start_this_date = this_date + datetime.timedelta(hours=1)

    this_data = this_data[:end_this_date]
    this_data.loc[start_this_date:end_this_date, 'Temperature'] = temp[this_date]
    # print(this_data.loc[start_this_date:end_this_date, 'Temperature'].shape)
    this_data.reset_index(inplace=True)

    data_fofT = this_data.copy()
    data_fofT.drop(['Load'], inplace=True, axis=1)
    data_fofT['Month'] = data_fofT['DateTime'].dt.month
    data_fofT['Hour'] = data_fofT['DateTime'].dt.hour

    data_yt = this_data[['Load', 'Temperature', 'DateTime']][:]

    data_rolling = data_fofT.copy()
    data_rolling.head()

    data_rolling['Temperature_Rolling_last_24hour'] = data_rolling['Temperature'].shift(1).rolling(window=24).mean()
    data_rolling.drop('Temperature', inplace=True, axis=1)

    base_data = helper.yt(0, data_yt)
    X_build_model = base_data[:]

    for h in range(73):
        lag_h = helper.fofT('Temperature', h, data_fofT)
        X_build_model = pd.concat([X_build_model, lag_h], axis=1)

    for day in range(1, 8):
        lag_day = helper.fofT('Temperature_Rolling_last_24hour', (day - 1) * 24, data_rolling)
        X_build_model = pd.concat([X_build_model, lag_day], axis=1)

    X_build_model['DateTime'] = pd.date_range(all_begin, end_this_date, freq='H')
    X_build_model.set_index('DateTime', inplace=True)
    X_build_model.dropna(inplace=True)
    X_train, y_train = X_build_model[:this_date].drop(['Load'], axis=1), X_build_model[:this_date]['Load']
    X_predict, y_true = X_build_model[start_this_date:end_this_date].drop(['Load'], axis=1), \
                        X_build_model[start_this_date:end_this_date]['Load']
    model_capture_rencency = LinearRegression()
    model_capture_rencency.fit(X_train, y_train)

    y_true = y_true.tolist()
    prediction = model_capture_rencency.predict(X_predict).tolist()

    peak_detected = 0
    if y_true[:-24].index(max(y_true[:-24])) == prediction[:-24].index(max(prediction[:-24])):
        peak_detected = 1
    else:
        peak_detected = 0

    end = time.time()

    results[date]['prediction'] = prediction
    results[date]['error']['MAPE'] = helper.mape(y_true[-24:], prediction[-24:])
    results[date]['error']['RMSE'] = helper.rmse(y_true[-24:], prediction[-24:])
    results[date]['peak_detected'] = peak_detected
    results[date]['time'] = end - start

    this_date = this_date + datetime.timedelta(days=1)
    print(f'Used: {end - start}')

with open('predicted_results_TVB_2017Q3.json', 'w') as f:
    json.dump(results, f)
