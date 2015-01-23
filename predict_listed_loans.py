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

import data_manipulation as dm


with open('credentials.json') as credentials_file:
    credentials = json.load(credentials_file)

passwd = credentials['mysql']['password']
con = mdb.connect(host='127.0.0.1', port=3307, user='root', passwd=passwd, db='insight', autocommit=True)

sql_query = "SELECT * FROM listed_loans;"
loanData = sql.read_sql(sql_query, con)

f = open('./pickles/rfr_20150123.pickle', 'rb')
regr = pickle.load(f)
f.close()

f = open('./pickles/rfc_20150123.pickle', 'rb')
clf = pickle.load(f)
f.close()

loanData = loanData.drop(['asOfDate',
                     'memberId',
                     'expDefaultRate',
                     'serviceFeeRate',
                     'acceptD',
                     'expD',
                     'listD',
                     'creditPullD',
                     'reviewStatusD',
                     'reviewStatus',
                     'investorCount',
                     'ilsExpD',
                     'initialListStatus',
                     'bcOpenToBuy',
                     'percentBcGt75',
                     'bcUtil',
                     'ficoRangeLow',
                     'ficoRangeHigh',
                     'mthsSinceRecentRevolDelinq',
                     'mthsSinceRecentBc',
                     'mortAcc',
                     'totalBalExMort',
                     'totalBcLimit',
                     'totalIlHighCreditLimit',
                     'mthsSinceRecentBcDlq',
                     'pubRecBankruptcies',
                     'numAcctsEver120Ppd',
                     'chargeoffWithin12Mths',
                     'taxLiens',
                     'numSats',
                     'numTlOpPast12m',
                     'avgCurBal',
                     'numBcTl',
                     'numActvBcTl',
                     'numBcSats',
                     'pctTlNvrDlq',
                     'numTl90gDpd24m',
                     'numTl30Dpd',
                     'numTl120dpd2m',
                     'numIlTl',
                     'moSinOldIlAcct',
                     'numActvRevTl',
                     'moSinOldRevTlOp',
                     'moSinRcntRevTlOp',
                     'totalRevHiLim',
                     'numRevTlBalGt0',
                     'numOpRevTl',
                     'totCollAmt',
                     'totHiCredLim',
                     'moSinRcntTl',
                     'accNowDelinq',
                     'delinqAmnt',
                     'mthsSinceRecentInq',
                     'numRevAccts',
                     'totCurBal',
                     'fundedAmount',
                     'accOpenPast24Mths'], 1)

##addr_state
statesBinarized = pd.get_dummies(loanData['addrState'])
loanData = pd.concat([loanData, statesBinarized], axis=1)

##Fill in the missing states:
cols = loanData.columns
states = ['AK',
          'AL',
          'AR',
          'AZ',
          'CA',
          'CO',
          'CT',
          'DC',
          'DE',
          'FL',
          'GA',
          'HI',
          'IA',
          'IL',
          'IDAHO',
          'INDIANA',
          'KS',
          'KY',
          'LA',
          'MA',
          'MD',
          'ME',
          'MI',
          'MN',
          'MO',
          'MS',
          'MT',
          'NC',
          'NE',
          'NH',
          'NJ',
          'NM',
          'NV',
          'NY',
          'OH',
          'OK',
          'OREGON',
          'PA',
          'RI',
          'SC',
          'SD',
          'TN',
          'TX',
          'UT',
          'VA',
          'VT',
          'WA',
          'WI',
          'WV',
          'WY']

for state in states:
    if state not in cols:
        loanData[state] = 0

##term
print "term"
loanData['term'] = [0 if x == 36 else 1 for x in loanData['term']]

##grade
print "grade"
loanData = loanData[pd.isnull(loanData['grade']) == 0]
loanData.index = range(len(loanData))
#Binarize the grade
gradesBinarized = pd.get_dummies(loanData['grade'])
loanData = pd.concat([loanData, gradesBinarized], axis=1)
loanData = loanData.drop(['grade'], 1)
grades = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
cols = loanData.columns
for grade in grades:
    if grade not in cols:
        loanData[grade] = 0


#Subgrade - numeric part of LendingClub's subgrade (ie: b3 -> grade=b, subgrade=3)
loanData['subGrade'] = [x[1:] for x in loanData['subGrade']]

##emp_length
emp_years = dict(zip(loanData['empLength'].unique(), np.arange(loanData['empLength'].nunique())))
loanData['empLength'] = loanData['empLength'].map(lambda x: emp_years[x])

homeOwnershipBinarized = pd.get_dummies(loanData['homeOwnership'])
loanData = pd.concat([loanData, homeOwnershipBinarized], axis=1)
ownership = ['ANY', 'MORTGAGE', 'NONE', 'OWN', 'RENT', 'OTHER']
cols = loanData.columns
for val in ownership:
    if val not in cols:
        loanData[val] = 0
loanData = loanData.drop(['homeOwnership'], 1)

loanData['isIncV'] = [1 if x == "SOURCE_VERIFIED" else x for x in loanData['isIncV']]
loanData['isIncV'] = [2 if x == "VERIFIED" else x for x in loanData['isIncV']]
loanData['isIncV'] = [0 if x == "NOT_VERIFIED" else x for x in loanData['isIncV']]

purposeBinarized = pd.get_dummies(loanData['purpose'])
loanData = pd.concat([loanData, purposeBinarized], axis=1)
purposes = ['car',
            'credit_card',
            'debt_consolidation',
            'home_improvement',
            'house',
            'major_purchase',
            'medical',
            'moving',
            'renewable_energy',
            'small_business',
            'vacation',
            'wedding',
            'other']
cols = loanData.columns
for purpose in purposes:
    if purpose not in cols:
        loanData[purpose] = 0

loanData['addrZip'] = [x[:3] for x in loanData['addrZip']]

##yrs_since_first_cr_line
yrs_since_first_cr_line = []
loanData['yrs_since_first_cr_line'] = 0
for i in range(len(loanData['earliestCrLine'])):
    earliest_year = pd.to_datetime(loanData['earliestCrLine'][i]).year
    yrs_since_first_cr_line.append(date.today().year - earliest_year )
loanData['yrs_since_first_cr_line'] = yrs_since_first_cr_line

loanData['issue_month'] = date.today().month
loanData['issue_year'] = date.today().year

loanData['desc_length'] = [len(str(x)) for x in loanData['description']]

loanData['install_frac_of_monthly_inc'] = loanData['installment']/loanData['annualInc']*12.0

cur = con.cursor()

cur.execute("SELECT * FROM unemployment_rates")
unemp_rate_tuple = cur.fetchall()
print unemp_rate_tuple[0]

unemp_rate_dict = dict()
for entry in unemp_rate_tuple:
	unemp_state = entry[1]
	unemp_year = entry[2]
	unemp_month = entry[3]
	unemp_rate = entry[4]
	key = "%s%s%s" %(unemp_state, unemp_year, unemp_month)
	unemp_rate_dict[key] = unemp_rate
loanData['unemp_rate_12mths'] = 0
loanData['unemp_rate_6mths'] = 0
loanData['unemp_rate_3mths'] = 0
for i, loan in enumerate(loanData['id']):
	key_12mths = "%s%s%s" %(loanData['addrState'][i],
							(loanData['issue_year'][i]-1),
							loanData['issue_month'][i])
	if loanData['issue_month'][i] <= 6:
		key_6mths = "%s%s%s" %(loanData['addrState'][i],
								(loanData['issue_year'][i]-1),
								loanData['issue_month'][i]+6)
	else:
		key_6mths = "%s%s%s" %(loanData['addr_state'][i],
								(loanData['issue_year'][i]),
								loanData['issue_month'][i]-6)
	if loanData['issue_month'][i] <= 3:
		key_3mths = "%s%s%s" %(loanData['addrState'][i],
								(loanData['issue_year'][i]-1),
								loanData['issue_month'][i]+3)
	else:
		key_3mths = "%s%s%s" %(loanData['addrState'][i],
								(loanData['issue_year'][i]),
								loanData['issue_month'][i]-3)
	try:
		loanData['unemp_rate_12mths'].iloc[i] = unemp_rate_dict[key_12mths]
		loanData['unemp_rate_6mths'].iloc[i] = unemp_rate_dict[key_6mths]
		loanData['unemp_rate_3mths'].iloc[i] = unemp_rate_dict[key_3mths]
	except KeyError:
		print KeyError, "loan ", i
		loanData = loanData.drop(loanData.index[i])
		loanData.index = range(len(loanData))

cur.execute("SELECT * FROM interest_rate_swaps")
int_rate_swap_tuple = cur.fetchall()

int_rate_swap_dict = dict()
for entry in int_rate_swap_tuple:
	int_rate_swap_year = entry[1]
	int_rate_swap_rate = entry[3]
	int_rate_swap_dict[int_rate_swap_year] = int_rate_swap_rate
loanData['implied_risk'] = 0
loanData.index = range(len(loanData))
indices_to_drop = []
for i in range(len(loanData)):
    year_i = loanData['issue_year'][i]
    swap_rate_i = int_rate_swap_dict[year_i - 1]
    int_rate_i = loanData['intRate'][i]
    impl_risk = int_rate_i - swap_rate_i
    try:
        loanData['implied_risk'].iloc[i] = impl_risk
    except Error:
        print Error, "loan ", i
loanData = loanData[loanData['implied_risk'] != 0]
loanData.index = range(len(loanData))

listedLoanData = loanData[['loanAmount',
'term',
'intRate',
'installment',
'empLength',
'annualInc',
'isIncV',
'addrZip',
'dti',
'delinq2Yrs',
'inqLast6Mths',
'mthsSinceLastDelinq',
'mthsSinceLastRecord',
'openAcc',
'pubRec',
'revolBal',
'revolUtil',
'totalAcc',
'collections12MthsExMed',
'mthsSinceLastMajorDerog',
'A',
'B',
'C',
'D',
'E',
'F',
'G',
'MORTGAGE',
'OWN',
'RENT',
'issue_month',
#'issue_year',
'car',
'credit_card',
'debt_consolidation',
'home_improvement',
'house',
'major_purchase',
'medical',
'moving',
'renewable_energy',
'small_business',
'vacation',
'wedding',
'AK',
'AL',
'AR',
'AZ',
'CA',
'CO',
'CT',
'DC',
'DE',
'FL',
'GA',
'HI',
'IL',
'INDIANA',
'KS',
'KY',
'LA',
'MA',
'MD',
'MI',
'MN',
'MO',
'MS',
'MT',
'NC',
'NH',
'NJ',
'NM',
'NV',
'NY',
'OH',
'OK',
'OREGON',
'PA',
'RI',
'SC',
'SD',
'TN',
'TX',
'UT',
'VA',
'VT',
'WA',
'WI',
'WV',
'WY',
'yrs_since_first_cr_line',
'desc_length',
'unemp_rate_12mths',
'unemp_rate_6mths',
'unemp_rate_3mths',
'subGrade',
'other',
'install_frac_of_monthly_inc',
'implied_risk']]

#Only keep 36 month terms:
listedLoanData = listedLoanData[listedLoanData['term']==0]
X_test = listedLoanData.values

X_test = listedLoanData.astype(float).values
(X_test, _) = dm.standardize_samples(X_test, X_test)
(X_test, _) = dm.scale_samples_to_range(X_test, X_test)

prediction_clf = clf.predict_proba(X_test)
print prediction_clf[0]

prediction_regr = regr.predict(X_test)

##Upload predicted default times to database
for i, val in enumerate(prediction_regr):
  sql_query = "UPDATE listed_loans SET pred_default_time='%s' WHERE id='%s';" %(int(val), loanData['id'][i])
  cur.execute(sql_query)
for i, val in enumerate(prediction_clf):
  sql_query = "UPDATE listed_loans SET pred_default='%s' WHERE id='%s';" %(val[0], loanData['id'][i])
  cur.execute(sql_query)
  sql_query = "UPDATE listed_loans SET pred_paid='%s' WHERE id='%s';" %(val[1], loanData['id'][i])
  cur.execute(sql_query)
cur.close()

