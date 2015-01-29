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

class Predictor():
  def __init__(self):
    self.load_data()
    self.load_classifiers()
    self.clean_data()
    self.add_unemp_rates()
    self.add_swap_rates()
    self.rearrange_loans()
    self.remove_60mths()
    self.define_x_test()
    self.predict()
    self.calculate_roi()
    self.upload_to_db()
    self.close_db_connection()

  def load_data(self):
    with open('credentials.json') as credentials_file:
      credentials = json.load(credentials_file)
    passwd = credentials['mysql']['password']
    self.con = mdb.connect(host='127.0.0.1', port=3307, user='root', passwd=passwd, db='insight', autocommit=True)

    sql_query = "SELECT * FROM test_loans;"
    self.loanData = sql.read_sql(sql_query, self.con)

  def load_classifiers(self):
    self.regrs = []
    self.clfs = []
    for i in range(0, 2):
      rfr_file = './pickles/rfr_%s.pickle' %i
      rfc_file = './pickles/rfc_%s.pickle' %i
      print "loading rf classifiers %s" %i
      f = open(rfr_file, 'rb')
      self.regrs.append(pickle.load(f))
      f.close()

      f = open(rfc_file, 'rb')
      self.clfs.append(pickle.load(f)) 
      f.close()

  def clean_data(self):
    self.loanData = self.loanData.drop(['asOfDate',
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
    statesBinarized = pd.get_dummies(self.loanData['addrState'])
    self.loanData = pd.concat([self.loanData, statesBinarized], axis=1)

    ##Fill in the missing states:
    cols = self.loanData.columns
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
            self.loanData[state] = 0

    ##term
    print "term"
    self.loanData['term'] = [0 if x == 36 else 1 for x in self.loanData['term']]

    ##grade
    print "grade"
    #self.loanData = self.loanData[pd.isnull(self.loanData['grade']) == 0]
    #self.loanData.index = range(len(self.loanData))
    #Binarize the grade
    gradesBinarized = pd.get_dummies(self.loanData['grade'])
    self.loanData = pd.concat([self.loanData, gradesBinarized], axis=1)
    self.loanData = self.loanData.drop(['grade'], 1)
    grades = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    cols = self.loanData.columns
    for grade in grades:
        if grade not in cols:
            self.loanData[grade] = 0


    #Subgrade - numeric part of LendingClub's subgrade (ie: b3 -> grade=b, subgrade=3)
    self.loanData['subGrade'] = [x[1:] for x in self.loanData['subGrade']]

    ##emp_length
    emp_years = dict(zip(self.loanData['empLength'].unique(), np.arange(self.loanData['empLength'].nunique())))
    self.loanData['empLength'] = self.loanData['empLength'].map(lambda x: emp_years[x])

    homeOwnershipBinarized = pd.get_dummies(self.loanData['homeOwnership'])
    self.loanData = pd.concat([self.loanData, homeOwnershipBinarized], axis=1)
    ownership = ['ANY', 'MORTGAGE', 'NONE', 'OWN', 'RENT', 'OTHER']
    cols = self.loanData.columns
    for val in ownership:
        if val not in cols:
            self.loanData[val] = 0
    self.loanData = self.loanData.drop(['homeOwnership'], 1)

    self.loanData['isIncV'] = [1 if x == "SOURCE_VERIFIED" else x for x in self.loanData['isIncV']]
    self.loanData['isIncV'] = [2 if x == "VERIFIED" else x for x in self.loanData['isIncV']]
    self.loanData['isIncV'] = [0 if x == "NOT_VERIFIED" else x for x in self.loanData['isIncV']]

    purposeBinarized = pd.get_dummies(self.loanData['purpose'])
    self.loanData = pd.concat([self.loanData, purposeBinarized], axis=1)
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
    cols = self.loanData.columns
    for purpose in purposes:
        if purpose not in cols:
            self.loanData[purpose] = 0

    self.loanData['addrZip'] = [x[:3] for x in self.loanData['addrZip']]

    ##yrs_since_first_cr_line
    yrs_since_first_cr_line = []
    self.loanData['yrs_since_first_cr_line'] = 0
    for i in range(len(self.loanData['earliestCrLine'])):
        earliest_year = pd.to_datetime(self.loanData['earliestCrLine'][i]).year
        yrs_since_first_cr_line.append(date.today().year - earliest_year )
    self.loanData['yrs_since_first_cr_line'] = yrs_since_first_cr_line

    self.loanData['issue_month'] = date.today().month
    self.loanData['issue_year'] = date.today().year

    self.loanData['desc_length'] = [len(str(x)) for x in self.loanData['description']]

    self.loanData['install_frac_of_monthly_inc'] = self.loanData['installment']/self.loanData['annualInc']*12.0

  def add_unemp_rates(self):
    self.cur = self.con.cursor()

    self.cur.execute("SELECT * FROM unemployment_rates")
    unemp_rate_tuple = self.cur.fetchall()
    print unemp_rate_tuple[0]

    unemp_rate_dict = dict()
    for entry in unemp_rate_tuple:
    	unemp_state = entry[1]
    	unemp_year = entry[2]
    	unemp_month = entry[3]
    	unemp_rate = entry[4]
    	key = "%s%s%s" %(unemp_state, unemp_year, unemp_month)
    	unemp_rate_dict[key] = unemp_rate
    self.loanData['unemp_rate_12mths'] = 0
    self.loanData['unemp_rate_6mths'] = 0
    self.loanData['unemp_rate_3mths'] = 0
    for i, loan in enumerate(self.loanData['id']):
    	key_12mths = "%s%s%s" %(self.loanData['addrState'][i],
    							(self.loanData['issue_year'][i]-1),
    							self.loanData['issue_month'][i])
    	if self.loanData['issue_month'][i] <= 6:
    		key_6mths = "%s%s%s" %(self.loanData['addrState'][i],
    								(self.loanData['issue_year'][i]-1),
    								self.loanData['issue_month'][i]+6)
    	else:
    		key_6mths = "%s%s%s" %(self.loanData['addr_state'][i],
    								(self.loanData['issue_year'][i]),
    								self.loanData['issue_month'][i]-6)
    	if self.loanData['issue_month'][i] <= 3:
    		key_3mths = "%s%s%s" %(self.loanData['addrState'][i],
    								(self.loanData['issue_year'][i]-1),
    								self.loanData['issue_month'][i]+3)
    	else:
    		key_3mths = "%s%s%s" %(self.loanData['addrState'][i],
    								(self.loanData['issue_year'][i]),
    								self.loanData['issue_month'][i]-3)
    	try:
    		self.loanData['unemp_rate_12mths'].iloc[i] = unemp_rate_dict[key_12mths]
    		self.loanData['unemp_rate_6mths'].iloc[i] = unemp_rate_dict[key_6mths]
    		self.loanData['unemp_rate_3mths'].iloc[i] = unemp_rate_dict[key_3mths]
    	except KeyError:
    		print KeyError, "loan ", i
    		#self.loanData = self.loanData.drop(self.loanData.index[i])
    		#self.loanData.index = range(len(self.loanData))

  def add_swap_rates(self): 
    self.cur.execute("SELECT * FROM interest_rate_swaps")
    int_rate_swap_tuple = self.cur.fetchall()

    int_rate_swap_dict = dict()
    for entry in int_rate_swap_tuple:
    	int_rate_swap_year = entry[1]
    	int_rate_swap_rate = entry[3]
    	int_rate_swap_dict[int_rate_swap_year] = int_rate_swap_rate
    self.loanData['implied_risk'] = 0
    self.loanData.index = range(len(self.loanData))
    for i in range(len(self.loanData)):
        year_i = self.loanData['issue_year'][i]
        swap_rate_i = int_rate_swap_dict[year_i - 1]
        int_rate_i = self.loanData['intRate'][i]
        impl_risk = int_rate_i - swap_rate_i
        try:
            self.loanData['implied_risk'].iloc[i] = impl_risk
        except:
            print "Error ", "loan ", i
    #self.loanData = self.loanData[self.loanData['implied_risk'] != 0]
    #self.loanData.index = range(len(self.loanData))

  def rearrange_loans(self):
    self.listedLoanData = self.loanData[[
    'id',
    'loanAmount',
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

  def remove_60mths(self):
    #Only keep 36 month terms:
    self.listedLoanData = self.listedLoanData[self.listedLoanData['term']==0]
    self.listedLoanData.index = range(len(self.listedLoanData))
  
  def define_x_test(self):
    #self.X_test = self.listedLoanData.drop(['id'], 1).values

    self.X_test = self.listedLoanData.drop(['id'], 1).astype(float).values
    (self.X_test, _) = dm.standardize_samples(self.X_test, self.X_test)
    (self.X_test, _) = dm.scale_samples_to_range(self.X_test, self.X_test)

  def predict(self):
    #arrays to hold final prediction values
    self.prediction_clf_0 = []
    self.prediction_clf_1 = []
    self.prediction_regr = []
    self.error_clf = []
    self.error_regr = []

    print "predicting loans"
    for loan in self.X_test:
      #temporary variables to hold predictions for each new loan
      preds_clf = []
      preds_regr = []
      for i in range(0, 2):
        preds_clf.append(self.clfs[i].predict_proba(loan))
        preds_regr.append(self.regrs[i].predict(loan))
      #break up positive and negative probabilities for clf:
      preds_clf_0 = [x[0][0] for x in preds_clf]
      preds_clf_1 = [x[0][1] for x in preds_clf]

      mean_clf_0 = np.mean(preds_clf_0)
      mean_clf_1 = np.mean(preds_clf_1)
      std_clf = np.std(preds_clf_0)
      self.prediction_clf_0.append(mean_clf_0)
      self.prediction_clf_1.append(mean_clf_1)
      self.error_clf.append(std_clf)

      mean_regr = np.mean(preds_regr)
      std_regr = np.std(preds_regr)
      self.prediction_regr.append(mean_regr)
      self.error_regr.append(std_regr)
    print self.error_clf
    print len(self.error_clf)


  def calculate_roi(self):
    #Calculate expected ROI
    self.roi = []
    for index, pred in enumerate(self.prediction_regr):
        income = 0
        installment = self.listedLoanData['installment'][index]  
        loanAmount = self.listedLoanData['loanAmount'][index]
        mths_till_default = 36
        if self.prediction_clf_1[index] < 0.7:
            mths_till_default = int(pred/30)
        for i in range(0, mths_till_default):
            income += installment
        self.roi.append(income/loanAmount)

  def upload_to_db(self):
    ##Upload predicted default times to database
    for i, val in enumerate(self.prediction_regr):
      #default time
      sql_query = "UPDATE listed_loans SET pred_default_time='%s' WHERE id='%s';" %(int(val), self.listedLoanData['id'][i])
      self.cur.execute(sql_query)
      #default time error
      sql_query = "UPDATE listed_loans SET pred_default_time_error='%s' WHERE id='%s';" %(self.error_regr[i], self.listedLoanData['id'][i])
      self.cur.execute(sql_query)
    for i, val in enumerate(self.prediction_clf_0):
      #default prediction
      sql_query = "UPDATE listed_loans SET pred_default='%s' WHERE id='%s';" %(val, self.listedLoanData['id'][i])
      self.cur.execute(sql_query)
      #default prediction error
      sql_query = "UPDATE listed_loans SET pred_default_error='%s' WHERE id='%s';" %(self.error_clf[i], self.listedLoanData['id'][i])
      self.cur.execute(sql_query)
    for i, val in enumerate(self.prediction_clf_1):
      #paid prediction
      sql_query = "UPDATE listed_loans SET pred_paid='%s' WHERE id='%s';" %(val, self.listedLoanData['id'][i])
      self.cur.execute(sql_query)
      #roi
      sql_query = "UPDATE listed_loans SET pred_roi='%s' WHERE id='%s';" %(self.roi[i], self.listedLoanData['id'][i])
      self.cur.execute(sql_query)

  def close_db_connection(self):
    self.cur.close()

p = Predictor()
