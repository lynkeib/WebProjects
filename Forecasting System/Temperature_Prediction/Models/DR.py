import numpy as np


class DR(object):

    def __init__(self, dataframe):
        df = dataframe.copy()
        test = df[
            ['Date', 'Hour', 'Weekday', 'Month', 'Load', 'Mean_Temp', 'Mean_Humi', 'RIV_Temp', 'RIV_Humi', 'LAX_Temp',
             'LAX_Humi', 'USC_Temp', 'USC_Humi', 'WJF_Temp', 'WJF_Humi', 'TRM_Temp', 'TRM_Humi']]

        test.loc[:, 'RIV_Temp_Log'] = np.log(df['RIV_Temp'])

        test.loc[:, 'Load_Log'] = np.log(df['Load'])
        test['Load_Lag_48'] = test['Load_Log'].shift(48, axis=0)
        # test['Temp_Lag_48'] = test['Mean_Temp'].shift(48, axis=0)
        test['Humi_Lag_48'] = test['Mean_Humi'].shift(48, axis=0)
        test['RIV_Temp_Log_Lag_48'] = test['RIV_Temp_Log'].shift(48, axis=0)

        # test['RIV_Temp_Lag_48']= test['RIV_Temp'].shift(48, axis=0)

        cal = USFederalHolidayCalendar()

        holidays = cal.holidays(start='2014-01-01', end=str(datetime.datetime.now()), return_name=True)

        holidays = pd.DataFrame(holidays)

        holidays = holidays.reset_index()
        holidays = holidays.rename(columns={'index': "Date", 0: 'Holiday'})
        holidays['Date'] = pd.to_datetime(holidays['Date'])

        test['Date'] = pd.to_datetime(test['Date'])
        lm_data = test.loc[49:len(test), ].merge(holidays, how='left', on='Date')
        lm_data['Holiday'] = lm_data['Holiday'].fillna("Not Holiday")

        lm_data[["Hour", "Weekday", "Month", "Holiday"]] = lm_data[["Hour", "Weekday", "Month", "Holiday"]].astype(
            'category')

        DateTime = pd.DataFrame(
            lm_data.apply(lambda line: pd.to_datetime(line['Date']) + datetime.timedelta(hours=line['Hour']), axis=1))
        DateTime.columns = ['DateTime']

        self.lm_data = pd.concat([DateTime, lm_data], axis=1)
        self.lm_data.set_index('DateTime', inplace=True)

    def model_building(self, date, station):
        pass

    def predict_next_40hours_temp(self):
        pass
