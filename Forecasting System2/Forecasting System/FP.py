import pandas as pd
from fbprophet import Prophet
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error
import datetime


class FP(object):

    def __init__(self, path, holiday_path, date):
        self.df = pd.read_excel(path, sheet_name='SCE Load Only', date_parser='Date')
        self.date = date
        holidey = pd.read_csv(holiday_path)
        holidey = holidey.query('Holiday ==True')
        holidey.rename(columns={'Date': 'ds', 'Holiday': 'holiday'}, inplace=True)
        holidey = holidey.drop(['riv - low', 'Load'], axis=1)
        holidey['holiday'] = 'gen_holidays'
        holidey = holidey.reset_index()
        holidey = holidey.drop(['index'], axis=1)
        holidey['lower_window'] = 0
        holidey['upper_window'] = 1
        # Added Hong's holidays
        playoffs = pd.DataFrame({
            'holiday': 'playoff',
            'ds': pd.to_datetime(['2013-01-12', '2013-07-12', '2013-12-24', '2014-01-12', '2014-07-12', '2014-07-19',
                                  '2014-07-02', '2014-12-24', '2015-07-11', '2015-12-24', '2016-07-17',
                                  '2016-07-24', '2016-07-07', '2016-07-24', '2016-12-24', '2017-07-17', '2017-07-24',
                                  '2017-07-07', '2017-12-24']),
            'lower_window': 0,
            'upper_window': 2}
        )
        superbowls = pd.DataFrame({
            'holiday': 'superbowl',
            'ds': pd.to_datetime(['2013-01-01', '2013-01-21', '2013-02-14', '2013-02-18',
                                  '2013-05-27', '2013-07-04', '2013-09-02', '2013-10-14', '2013-11-11', '2013-11-28',
                                  '2013-12-25', '2014-01-01', '2014-01-20', '2014-02-14', '2014-02-17',
                                  '2014-05-26', '2014-07-04', '2014-09-01', '2014-10-13', '2014-11-11', '2014-11-27',
                                  '2014-12-25', '2015-01-01', '2015-01-19', '2015-02-14', '2015-02-16',
                                  '2015-05-25', '2015-07-03', '2015-09-07', '2015-10-12', '2015-11-11', '2015-11-26',
                                  '2015-12-25', '2016-01-01', '2016-01-18', '2016-02-14', '2016-02-15',
                                  '2016-05-30', '2016-07-04', '2016-09-05', '2016-10-10', '2016-11-11', '2016-11-24',
                                  '2016-12-25', '2017-01-02', '2017-01-16', '2017-02-14', '2017-02-20',
                                  '2017-05-29', '2017-07-04', '2017-09-04', '2017-10-09', '2017-11-10', '2017-11-23',
                                  '2017-12-25', '2018-01-01', '2018-01-15', '2018-02-14', '2018-02-19'
                                  ]),
            'lower_window': 0,
            'upper_window': 3,
        })

        holidays = pd.concat((playoffs, superbowls, holidey), sort=True)
        # holidays.tail()
        self.holidays = holidays
        self.prediction_period = 40

    def make_comparison_dataframe(self, historical, fcst):
        """
        Join the history with the forecast
        The resulting dataset will contain columns 'yhat', 'yhat_lower', 'yhat_upper' and 'y'.
        """
        return fcst.set_index('ds')[['yhat', 'yhat_lower', 'yhat_upper']].join(historical.set_index('ds'))

    def calculate_forecast_errors(self, data, prediction_size):
        """Calculate MAPE and MAE of the forecast.

           Args:
               df: joined dataset with 'y' and 'yhat' columns.
               prediction_size: number of days at the end to predict.
        """

        # Make a copy
        df = data.copy()

        # Now we calculate the values of e_i and p_i according to the formulas given in the article above.
        df['e'] = df['y'] - df['yhat']
        df['p'] = 100 * df['e'] / df['y']
        RMSE = np.sqrt((((df['yhat'] - df['y']) ** 2).mean()))
        # Recall that we held out the values of the last `prediction_size` days
        # in order to predict them and measure the quality of the model.

        # Now cut out the part of the data which we made our prediction for.
        predicted_part = df[-prediction_size:]

        # Define the function that averages absolute error values over the predicted part.
        error_mean = lambda error_name: np.mean(np.abs(predicted_part[error_name]))

        # Now we can calculate MAPE and MAE and return the resulting dictionary of errors.
        return {'MAPE': error_mean('p'), 'MAE': error_mean('e'), 'RMSE': RMSE}

    def predict_next_40hours(self):
        # date_str = self.date + datetime.timedelta(hours=)
        prediction_period = self.prediction_period
        holidays = self.holidays
        date_str = self.date
        dataframe = self.df
        dataframe = dataframe[['Date', 'load']].copy()
        dataframe = dataframe.rename(columns={'Date': 'ds', "load": "y"})
        date_str = pd.to_datetime(date_str)
        df_c = dataframe.copy()
        train_df = df_c[df_c['ds'] < date_str]  # .values[0]
        train_df['y'] = np.log(train_df['y'])
        prediction_size = prediction_period
        m_holi = Prophet(yearly_seasonality=False, weekly_seasonality=False, daily_seasonality=False, holidays=holidays,
                         changepoint_range=.999,
                         changepoint_prior_scale=38, seasonality_prior_scale=38,
                         holidays_prior_scale=17, seasonality_mode='additive') \
            .add_seasonality(name='monthly', period=30.5, fourier_order=7) \
            .add_seasonality(name='daily', period=1, fourier_order=3) \
            .add_seasonality(name='weekly', period=7, fourier_order=3) \
            .add_seasonality(name='yearly', period=24, fourier_order=5) \
            .add_seasonality(name='quarterly', period=365.25 / 4, prior_scale=35, fourier_order=2)
        m_holi.fit(train_df[['ds', 'y']])
        future_holi = m_holi.make_future_dataframe(periods=prediction_size, freq='H')
        forecast_holi = m_holi.predict(future_holi)
        m_holi.plot(forecast_holi)
        m_holi.plot_components(forecast_holi)
        cmp_df = self.make_comparison_dataframe(df_c, forecast_holi)
        cmp_df['yhat'] = np.exp(cmp_df['yhat'])
        error_name = []
        error_value = []
        for err_name, err_value in self.calculate_forecast_errors(cmp_df, prediction_size).items():
            error_name.append(err_name)
            error_value.append(err_value)

        # 2nd model
        # date_str= pd.to_datetime(date_str)
        df_c = dataframe.copy()
        this_date = pd.to_datetime(date_str) + datetime.timedelta(hours=7)
        train_df = df_c[df_c['ds'] <= this_date]  # .values[0]
        #     train_df = train_df[:-prediction_size]
        train_df['y'] = np.log(train_df['y'])
        prediction_size = prediction_period
        m_holi = Prophet(yearly_seasonality=False, weekly_seasonality=False, daily_seasonality=False, holidays=holidays,
                         changepoint_range=.999,
                         changepoint_prior_scale=38, seasonality_prior_scale=38,
                         holidays_prior_scale=17, seasonality_mode='additive') \
            .add_seasonality(name='monthly', period=30.5, fourier_order=7) \
            .add_seasonality(name='daily', period=1, fourier_order=3) \
            .add_seasonality(name='weekly', period=7, fourier_order=3) \
            .add_seasonality(name='yearly', period=24, fourier_order=5) \
            .add_seasonality(name='quarterly', period=365.25 / 4, prior_scale=35, fourier_order=2)
        m_holi.fit(train_df[['ds', 'y']])
        future_holi = m_holi.make_future_dataframe(periods=prediction_size, freq='H')
        forecast_holi = m_holi.predict(future_holi)
        #     m_holi.plot(forecast_holi)
        #     m_holi.plot_components(forecast_holi)
        #     cmp_df = make_comparison_dataframe(df_c, forecast_holi)
        #     cmp_df['yhat']=np.exp(cmp_df['yhat'])
        #     for err_name, err_value in calculate_forecast_errors(cmp_df, prediction_size).items():
        #         error_name.append(err_name)
        #         error_value.append(err_value)
        #     this_date = pd.to_datetime(date_str) + datetime.timedelta(hours = 7)
        forecast_holi = forecast_holi[forecast_holi['ds'] > this_date]
        #     forecast_holi = np.exp(forecast_holi['yhat'])
        res = np.exp(forecast_holi['yhat'])
        # forecast_holi['aa'] = res
        return error_name, error_value, res


if __name__ == '__main__':
    path = '../Data/20140101-20190901 SCE & CAISO Actual Load  9 27 2019.xlsx'
    holiday_path = '../Data/holiday.csv'

    model_FP = FP(path, holiday_path, '2018-01-15')
    error_name, error_values, res = model_FP.predict_next_40hours()
    print(error_name)
    print(error_values)
    print(res)
