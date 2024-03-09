from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd
import pickle
from imblearn.over_sampling import SMOTE

data = pd.read_csv('scaled_data.csv')

#extract relevant features
selected_features = ['@attribute SMA numeric', '@attribute MeanMag numeric', '@attribute RMS numeric','@attribute Pt80 numeric','@attribute StdevZ numeric','@attribute Pt50 numeric','@attribute MedianMag numeric','@attribute RangeZ numeric','@attribute Pt_90 numeric','@attribute Pt20 numeric']  
X = data[selected_features]

target_variable = 'activity' 
y = data[target_variable]

#applying smote to oversample minority classes
smote = SMOTE()

X_resampled, y_resampled = smote.fit_resample(X, y)

#split the dataset into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=42)

knn_model = KNeighborsClassifier(n_neighbors=1, metric='minkowski', p=2 )  
knn_model.fit(X_train, y_train)

y_pred = knn_model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

with open('knn_model.pkl', 'wb') as file:
    pickle.dump(knn_model, file)