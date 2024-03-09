import pickle
import subprocess
import pandas as pd
from datetime import datetime
import time
from sklearn.preprocessing import MinMaxScaler

import mysql.connector


# Load the saved model from file
with open('./models/knn_model.pkl', 'rb') as file:
    knn_model = pickle.load(file)

data = pd.read_csv('hardata.csv')
selected_features = ['@attribute SMA numeric', '@attribute MeanMag numeric', '@attribute RMS numeric','@attribute Pt80 numeric','@attribute StdevZ numeric','@attribute Pt50 numeric','@attribute MedianMag numeric','@attribute RangeZ numeric','@attribute Pt_90 numeric','@attribute Pt20 numeric']
sc=  data[selected_features]

scaler = MinMaxScaler() 
scaler.fit(sc)
#export accl data from database 
subprocess.run(['python', 'data_export.py'],check=True)

subprocess.run(["C:\\Program Files\\Polyspace\\R2020a\\bin\\matlab", "-nosplash", "-nodesktop", "-r", f"run('{'Extract'}');exit;"],check=True)

time.sleep(13)

teset = pd.read_csv('activityoutput.csv',header=None)
scaled_data = scaler.transform(teset)
#print(scaled_data)
y_pred = knn_model.predict(scaled_data)

print("Predicted labels:", y_pred)

acts = pd.read_csv('adls.csv')
for i in range(24):
    if (y_pred[0]) == acts['no'][i]:
        result = acts['activity'][i]
print(result)


cnx = mysql.connector.connect(
  host='localhost',
  user='root',
  password='',
  database='activity'
)

current_time = datetime.now()
cursor = cnx.cursor()
query = "Insert into activity_log(time,activity) values(%s,%s) "
cursor.execute(query,(current_time,result))
cnx.commit()


cursor.close()
cnx.close()
