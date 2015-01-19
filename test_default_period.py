
# coding: utf-8

# In[689]:

import pandas as pd
import numpy as np
import glob, sys
from datetime import date
import pickle
from random import randint

from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor 
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix

from sklearn.ensemble import RandomForestClassifier

from sklearn.tree import export_graphviz 
from sklearn.decomposition import PCA
from sklearn.metrics import recall_score

from scipy.stats import randint as sp_randint
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', 200)
get_ipython().magic(u'matplotlib inline')


# In[407]:

f = open('data.pickle', 'rb')
loanData = pickle.load(f)


# In[408]:

loanData[:10]


# In[409]:

loanData['roi'] = (loanData['total_pymnt']-loanData['funded_amnt'])/loanData['funded_amnt']


# In[410]:

#mths active
days_active = loanData['last_pymnt_d'] - loanData['issue_d']
loanData['days_active'] = [x.item().days for x in days_active]


#### Separate by Default Period

# In[411]:

#default_period
#0 -> no default
#1 -> 0-6 months
#2 -> 6-12 months
#3 -> 12+ months
loanData['default_period'] = 0
for i in range(len(loanData)):
    if loanData['loan_status'][i] == 0:
        if loanData['days_active'][i] <= 180:
            loanData['default_period'].iloc[i] = 1
        elif loanData['days_active'][i] <= 365:
            loanData['default_period'].iloc[i] = 2
        else:
            loanData['default_period'].iloc[i] = 3


# In[414]:

loanData[:1]


# In[413]:

loanData = loanData.drop(['issue_d', 'last_pymnt_d', 'total_pymnt', 'funded_amnt', 'funded_amnt_inv', 'loan_status'], 1)


# In[415]:

#drop roi for now - working on classifying default time
loanData = loanData.drop(['roi'], 1)


# In[740]:

#A_loans = loanData[loanData['A'] == 1]
A_loans = loanData
A_loans = A_loans[A_loans['term'] == 0]


# In[741]:

B_loans = loanData[loanData['B'] == 1]
B_loans = B_loans[B_loans['term'] == 0]


# In[742]:

len(A_loans)


# In[743]:

A_loans = A_loans.drop(['A', 'B', 'C', 'D', 'E', 'F', 'G'], 1)


#### Classify A loans by default period

# In[744]:

A_loans[:1]


# In[745]:

features = A_loans.drop(['default_period', 'days_active'], 1).values
targets = A_loans['default_period'].values


# In[762]:

X_train, X_test, y_train, y_test = train_test_split(features, 
															targets, 
															test_size=0.1)


# In[763]:

X_train = X_train.astype(float)
y_train = y_train.astype(float)
X_test = X_test.astype(float)
y_test = y_test.astype(float)


# In[766]:

pca = PCA(n_components=30)
X_train = pca.fit_transform(X_train)
print "Reduced data down to ", pca.n_components_, " dimensions: "
print "Transforming test data ..."
X_test = pca.transform(X_test)


# In[767]:

X_test.shape


# In[728]:

#balance the loan categories
loans_per_default_period = [np.sum(y_train == 0), 
                           np.sum(y_train == 1), 
                           np.sum(y_train == 2), 
                           np.sum(y_train == 3)]
total_loans = len(y_train)
max_num = max(loans_per_default_period)
print "the largest category has %s loans" %max_num
for index, q in enumerate(loans_per_default_period):
    print "balancing loans in category %s" %index
    print "there are currently %s loans" %q
    num_loans_to_add = max_num - q
    print "we are going to add %s loans" %num_loans_to_add
    X_train_to_add = []
    y_train_to_add = []
    loan_category_indices = []
    for cat_index, j in enumerate(y_train):
        if j == index:
            loan_category_indices.append(cat_index)
    loans_in_category = X_train[loan_category_indices]
    targets_in_category = y_train[loan_category_indices]
    print "About to add %s loans" %num_loans_to_add
    for i in range(num_loans_to_add):
        r = np.random.randint(q-1)
        X_train_to_add.append(loans_in_category[r])
        y_train_to_add.append(targets_in_category[r])
    if len(y_train_to_add) > 0:
        X_train_to_add = np.array(X_train_to_add)
        y_train_to_add = np.array(y_train_to_add)
        print "appending %s loans" %len(y_train_to_add)
        print "length of y_train before: %s" %len(y_train)
        X_train = np.concatenate((X_train, X_train_to_add))
        y_train = np.concatenate((y_train, y_train_to_add))
        print "length of y_train after: %s" %len(y_train)
    


# In[768]:

clf = RandomForestClassifier(n_estimators=50)


# In[769]:

clf.fit(X_train, y_train)


# In[770]:

score = clf.score(X_test, y_test)
print score


# In[771]:

prediction = clf.predict(X_test)


# In[778]:

np.sum(prediction == 3)


# In[773]:

clf.feature_importances_


# In[774]:

A_loans[:1]


# In[775]:

cm = confusion_matrix(y_test, prediction)
plt.matshow(cm)
plt.title('Confusion matrix')
plt.colorbar()
plt.ylabel('True label')
plt.xlabel('Predicted label')
plt.show()


#### Regression - Predict ROI on A Loans

# In[289]:

len(A_loans)


# In[290]:

plt.hist(A_loans['roi'].values, bins=10)
plt.xlabel('ROI')
plt.ylabel('Count')
plt.title('ROI Count for Grade A Loans')
plt.show()


# In[291]:

plt.scatter(A_loans['annual_inc'], A_loans['roi'])
plt.xlim([0,200000])
plt.show()


# In[292]:

features = A_loans.drop(['loan_status', 'total_pymnt', 'roi'], 1).values
targets = A_loans['roi'].values


# In[293]:

X_train, X_test, y_train, y_test = train_test_split(features, 
															targets, 
															test_size=0.1)


# In[293]:




# In[294]:

scalerX = StandardScaler().fit(X_train)


# In[295]:

X_train, X_test = scalerX.transform(X_train), scalerX.transform(X_test)


# In[296]:

X_train.shape


# In[208]:

pca = PCA(n_components=20, copy=False, whiten=False)
X_train = pca.fit_transform(X_train)
print "Reduced data down to ", pca.n_components_, " dimensions"
X_test = pca.transform(X_test)


# In[297]:

clf = LinearRegression()


# In[298]:

clf.fit(X_train, y_train)


# In[299]:

clf.score(X_test, y_test)


# In[300]:

prediction = clf.predict(X_test)


# In[301]:

y_test


# In[302]:

plt.scatter(prediction, y_test)
plt.plot([-1,0.3], [-1,0.3])
plt.xlabel('prediction')
plt.ylabel('y_test')
plt.show()


# In[161]:

clf = SVR(C=1, gamma=0.01, degree=5, kernel='rbf')


# In[162]:

clf.fit(X_train, y_train)


# In[163]:

prediction = clf.predict(X_test)


# In[164]:

clf.score(X_test, y_test)


# In[165]:

plt.scatter(prediction, y_test)
plt.plot([-1,0.5], [-1,0.5])
plt.plot([-1,0.5], [0,0], '--', color='black')
plt.plot([0,0], [-1,0.5], '--', color='black')
plt.xlabel('Predicted ROI')
plt.ylabel('Actual ROI')
plt.title('Predicted vs Actual ROI')
plt.show()


# In[303]:

clf = RandomForestRegressor(n_estimators=100)


# In[304]:

clf.fit(X_train, y_train)


# In[305]:

prediction = clf.predict(X_test)


# In[306]:

clf.score(X_test, y_test)


# In[307]:

plt.scatter(prediction, y_test)
plt.plot([-1,0.5], [-1,0.5])
plt.plot([-1,0.5], [0,0], '--', color='black')
plt.plot([0,0], [-1,0.5], '--', color='black')
plt.xlabel('Predicted ROI')
plt.ylabel('Actual ROI')
plt.title('Predicted vs Actual ROI')
#plt.savefig('random_forest_A.pdf')
plt.show()


# In[112]:

len(X_test)


# In[113]:

len(X_train)


# In[126]:

A_loans.drop(['loan_status', 'total_pymnt', 'roi'], 1)[:1]


# In[225]:

print recall_score(y_test, prediction, average="macro")


# In[226]:

A_loans[:1]


# In[234]:

plt.hist(loanData['roi'], bins=20)
plt.show()


# In[257]:

loanData[:1]


# In[ ]:



