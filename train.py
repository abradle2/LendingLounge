import pandas as pd
import numpy as np
import glob, sys
from datetime import date
import pickle
from random import randint
import random
import time
import json
import os
from datetime import datetime
import pymysql as mdb
from pandasql import sqldf

from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestRegressor 
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVR
from sklearn.dummy import DummyClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.metrics import precision_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import roc_curve, auc
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

import data_manipulation as dm

class Trainer():

	def __init__(self):
		
		with open('credentials.json') as credentials_file:
		    credentials = json.load(credentials_file)

		passwd = credentials['mysql']['password']
		self.con = mdb.connect(host='127.0.0.1', port=3306, user='root', passwd=passwd, db='insight', autocommit=True)
		self.cur = self.con.cursor()
		print "Connected to database"
		
		self.load_data()

	def load_data(self):
		f = open('./pickles/mysql_dump.pickle', 'rb')
		self.loanData = pickle.load(f)
		self.loanData = pd.DataFrame(self.loanData)
		f.close()

	def drop_na(self):
		self.loanData = loanData.dropna()
		self.loanData.index = range(len(self.loanData))

	def drop_columns(self):
		#drop the columns with malformed data in mysql db
		self.loanData = self.loanData.drop(['none',
											'educational',
											'IA',
											'IDAHO',
											'ME',
											'NE',
											'other_housing',
											'issue_year'], 1)

	def drop_prepaid_loans(self):
		indices_to_drop = []
		for i in range(len(self.loanData)):
			if self.loanData['loan_status'][i]==1 and self.loanData['days_to_zero_dollars'][i] < 1000:
				indices_to_drop.append(i)
		self.loanData = self.loanData.drop(indices_to_drop, 0)
		print "Number of prepaid loans: ", len(indices_to_drop)
		print "Number of loans after dropping prepaids: ", len(self.loanData)


	def define_features_targets(self, kind="regression"):
		
		#take out 1000 random loans with 36 month terms for testing
		#ids are already populated in test_loans for consistency
		test_ids = []
		sql_query = "select id from test_loans;"
		self.cur.execute(sql_query)
		sql_resp = self.cur.fetchall()
		print "length of sql response: ", len(sql_resp)
		for val in sql_resp:
			test_ids.append(val[0])
		print "length of test_ids: ", len(test_ids)
		#make the test and train data frames
		self.testLoanData = self.loanData[self.loanData['id'].isin(test_ids)]
		self.trainLoanData = self.loanData[~self.loanData['id'].isin(test_ids)]
		self.testLoanData.index = range(len(self.testLoanData))
		self.trainLoanData.index = range(len(self.trainLoanData))
		print "Train Loan Data: ", len(self.trainLoanData)
		print "Test Loan Data: ", len(self.testLoanData)
		
		self.features = self.trainLoanData.drop(['loan_status', 
											'days_to_zero_dollars',
											'id'], 1)
		self.features = self.features.values
		#choose different target variables for regression vs classification
		if kind == "regression":
			self.targets = self.trainLoanData['days_to_zero_dollars'].values
			self.y_test = self.testLoanData['days_to_zero_dollars'].values
		elif kind == "classification":
			self.targets = self.trainLoanData['loan_status'].values
			self.y_test = self.testLoanData['loan_status'].values

	def preprocess(self):
		(self.X_train, 
		 self.X_cv, 
		 self.y_train, 
		 self.y_cv) = dm.split_train_test(features=self.features, 
		 									targets=self.targets, 
		 									test_size=0.1)
		self.X_test = self.testLoanData.drop(['loan_status', 
											  'days_to_zero_dollars',
											  'id'], 1).values
		(self.X_train, self.X_cv) = dm.standardize_samples(self.X_train, 
														  self.X_cv)
		(self.X_train, self.X_cv) = dm.scale_samples_to_range(self.X_train, 
																self.X_cv)
		(self.X_test, _) = dm.standardize_samples(self.X_test, 
														  self.X_test)
		(self.X_test, _) = dm.scale_samples_to_range(self.X_test, 
																self.X_test)

	def define_dummy_classifier(self):
		self.clf = DummyClassifier()

	def define_rfr(self, n_estimators=10):
		self.regr = RandomForestRegressor(n_estimators=n_estimators, oob_score=True)
		print self.regr.get_params()

	def define_linear_regressor(self):
		self.regr = LinearRegression()
		print self.regr.get_params()

	def define_SVR(self, C=1, gamma=0.1):
		self.regr = SVR(C=C, gamma=gamma, verbose=3)
		print self.regr.get_params()

	def define_logistic_regressor(self, penalty="l2", C=1.0, class_weight=None):
		self.clf = LogisticRegression(penalty=penalty, 
									  C=C, 
									  class_weight=class_weight)
		print self.clf.get_params()

	def define_rfc(self, n_estimators=10):
		self.clf = RandomForestClassifier(n_estimators=n_estimators, oob_score=True)
		print self.clf.get_params()

	def train(self, kind="regression"):
		print "Fitting training data"
		if kind == "regression":
			self.regr.fit(self.X_train, self.y_train)
		elif kind == "classification":
			self.clf.fit(self.X_train, self.y_train)

	def predict(self, X, kind="regression"):
		if kind == "regression":
			self.prediction = self.regr.predict(X)
		elif kind == "classification":
			self.prediction = self.clf.predict(X)

	def score(self, X, y, kind="regression"):
		if kind == "regression":
			score_val = self.regr.score(X, y)
			print "R2 Score: ", score_val
		elif kind == "classification":
			score_val = self.clf.score(X, y)
			print "Accuracy: ", score_val
			print classification_report(y, self.prediction)
			self.precision = precision_score(y, self.prediction, labels=[0,1,2], average=None)
			print "\n\nPrecision Score: ", self.precision, "\n\n"
			self.accuracy = accuracy_score(y, self.prediction)

	def test(self, kind="regression"):
		#run clf and regr on the test data to determine to top 100 loans
		#the top loans are the ones least likely to default
		if kind == "regression":
			pred = self.regr.predict(self.X_test)
			print "length of regression pred: ", len(pred)
			for i, loan in enumerate(self.testLoanData['id']):
				sql_query = "UPDATE test_loans SET pred_days_to_zero_dollars=%s where id='%s';" %(
						pred[i], self.testLoanData['id'][i])
				self.cur.execute(sql_query)
			print i
		elif kind == "classification":
			pred_proba = self.clf.predict_proba(self.X_test)
			for i, loan in enumerate(self.testLoanData['id']):
				sql_query = "UPDATE test_loans SET pred_default=%s, pred_paid=%s, pred_prepaid=%s where id='%s';" %(
						pred_proba[i][0], pred_proba[i][1],pred_proba[i][2], self.testLoanData['id'][i])
				self.cur.execute(sql_query)
		self.con.close()

	def run_pca(self, n_components=20):
		self.pca = PCA(n_components=n_components)
		self.X_train = self.pca.fit_transform(self.X_train)
		print "Reduced data down to ", self.pca.n_components_, " dimensions: "
		print "Transforming cv data ..."
		self.X_cv = self.pca.transform(self.X_cv)
		print "Transforming test data ..."
		self.X_test = self.pca.transform(self.X_test)

	def plot_prediction(self):
		plt.scatter(self.prediction, self.y_cv)
		plt.xlabel('prediction')
		plt.ylabel('y_test')
		plt.show()

	def runSVRGridSearch(self):
		C_vals = [0.01, 0.1, 1, 10, 100]
		gamma_vals = [1E-2, 1E-1, 1, 1E1, 1E2, 1E3, 1E4]

		for C in C_vals:
			for gamma in gamma_vals:
				print "\n\n C: ", C, "  gamma: ", gamma
				self.define_SVR(C=C, gamma=gamma)
				self.train()
				print "Training Scores:"
				self.predict(self.X_train)
				self.score(self.X_train, self.y_train)
				print "Testing Scores:"
				self.predict(self.X_cv)
				self.score(self.X_cv, self.y_cv)

	def roc(self):
		'''Compute ROC curve using one-vs-all technique'''
		pred_proba = self.clf.predict_proba(self.X_cv)
		fpr = []
		tpr = []
		thresholds = []
		for i in [0, 1, 2]:
			fpr_i, tpr_i, thresholds_i = roc_curve(self.y_cv, pred_proba[:,i], pos_label=i)
			fpr.append(fpr_i)
			tpr.append(tpr_i)
			thresholds.append(thresholds_i)
			print "AUC: ", auc(fpr_i, tpr_i)
		plt.plot([0,1], [0,1], '--', color=(0.6, 0.6, 0.6))
		plt.plot(fpr[0], tpr[0], label="Default", linewidth=3)
		plt.xlim([-0.05, 1.05])
		plt.ylim([-0.05, 1.05])
		plt.show()


	def pickle_algo(self, X, fileName):
		print "pickling algorithm"
		f = open(fileName, 'wb')
		pickle.dump(X, f)
		f.close()

#Add precision and accuracy to arrays to eventually get mean/std
precision_0_vals_dummy = []
precision_1_vals_dummy = []
precision_2_vals_dummy = []
accuracy_vals_dummy = []

precision_0_vals = []
precision_1_vals = []
precision_2_vals = []
accuracy_vals = []
for iteration in range(2):
	
	#Run regression
	trainer = Trainer()
	trainer.drop_columns()
	#trainer.drop_prepaid_loans()
	trainer.define_features_targets()
	trainer.preprocess()
	trainer.define_rfr(n_estimators=100)
	#trainer.define_linear_regressor()
	trainer.train()
	print "Training Scores"
	trainer.predict(trainer.X_train)
	trainer.score(trainer.X_train, trainer.y_train)
	print "Test Scores"
	trainer.predict(trainer.X_cv)
	trainer.score(trainer.X_cv, trainer.y_cv)
	#trainer.test(kind="regression")
	#print "Feature Importances"
	#feature_importances = trainer.regr.feature_importances_
	#for i, f in enumerate(feature_importances):
	#	print trainer.loanData.drop(['id', 'loan_status'], 1).columns[i], f
	#print "oob score"
	#print trainer.regr.oob_score_
	fileName = './pickles/rfr_%s.pickle' %iteration
	trainer.pickle_algo(fileName=fileName, X=trainer.regr)
	
	
	#Run Clasification
	print "Iteration ", iteration
	trainer = Trainer()
	trainer.drop_columns()
	trainer.define_features_targets(kind="classification")
	trainer.preprocess()
	#trainer.define_rfc(n_estimators=100)
	
	'''dummy classifier'''
	'''
	trainer.define_dummy_classifier()
	trainer.train(kind="classification")
	print "Training Scores"
	trainer.predict(trainer.X_train, kind="classification")
	trainer.score(trainer.X_train, trainer.y_train, kind="classification")
	print "Test Scores"
	trainer.predict(trainer.X_cv, kind="classification")
	trainer.score(trainer.X_cv, trainer.y_cv, kind="classification")
	precision_0_vals_dummy.append(trainer.precision[0])
	precision_1_vals_dummy.append(trainer.precision[1])
	precision_2_vals_dummy.append(trainer.precision[2])
	accuracy_vals_dummy.append(trainer.accuracy)
	'''
	'''logisitic regression '''

	trainer.define_logistic_regressor(C=0.01, penalty="l2")
	trainer.train(kind="classification")
	print "Training Scores"
	trainer.predict(trainer.X_train, kind="classification")
	trainer.score(trainer.X_train, trainer.y_train, kind="classification")
	print "Test Scores"
	trainer.predict(trainer.X_cv, kind="classification")
	trainer.score(trainer.X_cv, trainer.y_cv, kind="classification")
	precision_0_vals.append(trainer.precision[0])
	precision_1_vals.append(trainer.precision[1])
	precision_2_vals.append(trainer.precision[2])
	accuracy_vals.append(trainer.accuracy)
	#trainer.test(kind="classification")
	#print "Feature Importances"
	#feature_importances = trainer.clf.feature_importances_
	#for i, f in enumerate(feature_importances):
	#	print trainer.loanData.drop(['id', 'loan_status'], 1).columns[i], f
	#print "oob score"
	#print trainer.clf.oob_score_
	fileName = './pickles/rfc_%s.pickle' %iteration
	trainer.pickle_algo(fileName=fileName, X=trainer.clf)
	#trainer.roc()

precision_0_mean_dummy = np.mean(precision_0_vals_dummy)
precision_0_std_dummy = np.std(precision_0_vals_dummy)
precision_1_mean_dummy = np.mean(precision_1_vals_dummy)
precision_1_std_dummy = np.std(precision_1_vals_dummy)
precision_2_mean_dummy = np.mean(precision_2_vals_dummy)
precision_2_std_dummy = np.std(precision_2_vals_dummy)
accuracy_mean_dummy = np.mean(accuracy_vals_dummy)
accuracy_std_dummy = np.std(accuracy_vals_dummy)

print "Dummy Default Precision: ", precision_0_mean_dummy, " +/- ", precision_0_std_dummy
print "Dummy Fully Paid Precision: ", precision_1_mean_dummy, " +/- ", precision_1_std_dummy
print "Dummy Prepaid Precision: ", precision_2_mean_dummy, " +/- ", precision_2_std_dummy
print "Dummy Accuracy: ", accuracy_mean_dummy, " +/- ", accuracy_std_dummy


precision_0_mean = np.mean(precision_0_vals)
precision_0_std = np.std(precision_0_vals)
precision_1_mean = np.mean(precision_1_vals)
precision_1_std = np.std(precision_1_vals)
precision_2_mean = np.mean(precision_2_vals)
precision_2_std = np.std(precision_2_vals)
accuracy_mean = np.mean(accuracy_vals)
accuracy_std = np.std(accuracy_vals)

print "Default Precision: ", precision_0_mean, " +/- ", precision_0_std
print "Fully Paid Precision: ", precision_1_mean, " +/- ", precision_1_std
print "Prepaid Precision: ", precision_2_mean, " +/- ", precision_2_std
print "Accuracy: ", accuracy_mean, " +/- ", accuracy_std

