from Temperature_Prediction.predict import *
import time

start = time.time()
temp = TempPred('../Data/Hourly_Temp_Humi_Load-6.csv', '2018-04-02')
pred = temp.return_result("RIV")
end = time.time()
print(f'HW_RMSE: {temp.model_HW.RMSE}, HW_MAPE: {temp.model_HW.MAPE}')
print(f"NN_RMSE: {temp.model_NN.train_rmse}, NN_MAPE: {temp.model_NN.train_mape}")
print(f'time: {end - start}')
print(pred)
