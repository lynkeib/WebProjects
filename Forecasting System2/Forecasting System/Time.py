from helper import *
import pandas as pd
import datetime
import os

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

print(tf.__version__)

data = pd.read_csv('../Data/Hourly_Temp_Humi_Load-6.csv')
DateTime = pd.DataFrame(
    data.apply(lambda line: pd.to_datetime(line['Date']) + datetime.timedelta(hours=line['Hour']), axis=1))
DateTime.columns = ['DateTime']
temp = pd.concat([DateTime, data.iloc[:, 2], data.loc[:, data.columns.str.contains("Temp")]], axis=1)

temp.set_index('DateTime', inplace=True)
x_train = temp['2014-01-01 07:00':'2016-11-30 23:00']['RIV_Temp'].tolist()
# x_valid = temp['2017-12-01 00:00':'2018-01-01 00:00']['RIV_Temp'].tolist()

# window_size = 96
# batch_size = 10
# shuffle_buffer_size = 1000
window_size = 337 + 40
batch_size = 10
shuffle_buffer_size = 1000

dataset = windowed_dataset(x_train, window_size, batch_size, shuffle_buffer_size)

# l_1 = tf.keras.layers.Lambda(lambda x: tf.expand_dims(x, axis=-1), input_shape=[None])
l0 = tf.keras.layers.Dense(100)
l1 = tf.keras.layers.Dense(70)
l2 = tf.keras.layers.Dense(40)
model = tf.keras.models.Sequential([l0, l1, l2])
# model = tf.keras.models.Sequential([l0])

model.compile(loss='mean_absolute_percentage_error', optimizer=tf.keras.optimizers.SGD(lr=1e-6, momentum=0.9))
model.fit(dataset, epochs=100, verbose=0)

# print()

# print(f"Layer weights {l0.get_weights()}")
#


series = np.array(temp['2016-11-17 07:00:00':'2016-12-31 23:00']['RIV_Temp'].tolist())
#
forecast = []
# # total = (len(series) - 96) / 24
x_test = []
for time in range(0, len(series) - window_size, 24):
    #     print(len(series[time:time+60]))
    # print('train', len(series[time:time + window_size]))
    # print('test', len(series[time + window_size - 40:time + window_size]))
    forecast.append(model.predict(series[time:time + window_size - 40][np.newaxis]))
    x_test.append(series[time + window_size - 40:time + window_size])
    # print(forecast[-1])
    # print(total - 1, 'left')
    # total -= 1


# #     print(len(series[time:time+40]))
# #     print(len(series[time+40:time+50]))
#
# print('length of forecast', len(forecast))
#
# for line in forecast:
#     print(len(line[0]))
#
# for line in x_test:
#     print(line)
#
#
def mape(y_true, y_pred):
    return np.mean(np.abs((y_pred - y_true) / y_true)) * 100


def rmse(y_true, y_pred):
    return np.sqrt(np.mean((y_true - y_pred) ** 2))


result_mape = []
result_rmse = []
for index in range(len(forecast)):
    # print(len(forecast[index][0]))
    # print(len(x_test[index]))
    result_mape.append(mape(np.array(x_test[index]), np.array(forecast[index][0])))
    result_rmse.append(rmse(np.array(x_test[index]), np.array(forecast[index][0])))

#
print(len(result_mape))
print(np.mean(result_mape))
print(len(result_rmse))
print(np.mean(result_rmse))

# for line in forecast:
#     print(line)

#
# time = np.arange(1000, dtype='float32')
# baseline = 10
# series = trend(time, 0.1)
# amplitude = 40
# slope = 0.05
# noise_level = 5
#
# series = baseline + trend(time, slope) + seasonality(time, period=365, amplitude=amplitude)
# series += noise(time, noise_level, seed=42)
#
# split_time = 700
# time_train = time[:split_time]
# x_train = series[:split_time]
# time_valid = time[split_time:]
# x_valid = series[split_time:]
#
# window_size = 50
# batch_size = 10
# shuffle_buffer_size = 1000
#
# print(x_train)
#
# plot_series(time, series)
# plt.show()
#
# dataset = windowed_dataset(x_train, window_size, batch_size, shuffle_buffer_size)
#
# l0 = tf.keras.layers.Dense(10)
# model = tf.keras.models.Sequential([l0])
#
# model.compile(loss='mse', optimizer=tf.keras.optimizers.SGD(lr=1e-6, momentum=0.9))
# model.fit(dataset, epochs=100, verbose=1)
#
