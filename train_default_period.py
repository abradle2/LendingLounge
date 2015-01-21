import pandas as pd
import numpy as np
import glob, sys
from datetime import date
import pickle
from random import randint
import time
import json
import os
from datetime import datetime

from pandas.io import sql
import pymysql as mdb
import mysql_connector

from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor 
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

from sklearn.tree import export_graphviz 
from sklearn.decomposition import PCA
from sklearn.metrics import recall_score

from scipy.stats import randint as sp_randint
import matplotlib.pyplot as plt

f = open('pred_defaults.pickle', 'rb')
loanData = pickle.load(f)

loanData = pd.DataFrame(loanData)

loanData = loanData.drop(['Any',
						  'title_length',
						  'out_prncp',
						  'out_prncp_inv',
						  'unemp_rate_12mths',
						  'unemp_rate_6mths',
						  'unemp_rate_3mths'], 1)

loanData = loanData[loanData['annual_inc'] > 0]

#loanData = loanData.drop(['days_active'], 1)

loanData = loanData.dropna()

#loanData = loanData[loanData['last_pymnt_d'] != 'NaT']
#loanData.index = range(len(loanData))

#loanData['issue_d'] = [datetime.strptime(str(x), '%Y-%m-%d %H:%M:%S') for x in loanData['issue_d']]
#loanData['last_pymnt_d'] = [datetime.strptime(str(x), '%Y-%m-%d %H:%M:%S') for x in loanData['last_pymnt_d']]

#days_active = [(loanData['last_pymnt_d'][i] - loanData['issue_d'][i]).days for i in range(len(loanData))]

#loanData['days_active'] = days_active

loanData = loanData.drop(['issue_d', 'last_pymnt_d'], 1)

loanData = loanData[loanData['term'] == 0]

loanData.index = range(len(loanData))
loanData['days_to_default'] = 1056
for i, val in enumerate(loanData['days_active']):
    if loanData['loan_status'][i] == 0:
        loanData['days_to_default'].iloc[i] = loanData['days_active'].iloc[i]

features = loanData.drop(['loan_status', 'days_active', 'days_to_default'], 1)
for col in features.columns:
	print col

fatures = features.values
targets = loanData['days_active'].values

X_train, X_test, y_train, y_test = train_test_split(features, 
															targets, 
															test_size=0.1)

X_train = X_train.astype(float)
y_train = y_train.astype(float)
X_test = X_test.astype(float)
y_test = y_test.astype(float)

scalerX = StandardScaler().fit(X_train)

X_train, X_test = scalerX.transform(X_train), scalerX.transform(X_test)

clf = LinearRegression()

clf.fit(X_train, y_train)

clf.score(X_test, y_test)

prediction = clf.predict(X_test)


f = open('default_regression_algorithm_20150121.pickle', 'wb')
pickle.dump(clf, f)
f.close()


print X_test.shape

plt.scatter(prediction, y_test)
plt.xlabel('prediction')
plt.ylabel('y_test')
plt.show()
