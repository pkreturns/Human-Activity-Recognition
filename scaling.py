import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import pickle

data = pd.read_csv('hardata.csv')

X = data.drop('activity', axis=1)
y = data['activity']

scaler = MinMaxScaler()
scaler.fit(X)
scaled_data = scaler.transform(X)

scaled_df = pd.DataFrame(scaled_data, columns=X.columns)
scaled_df['activity'] = y
scaled_df.to_csv('scaled_data.csv', index=False)

with open('scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)