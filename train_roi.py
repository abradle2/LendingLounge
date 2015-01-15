import pandas as pd
import numpy as np
import glob, sys
from datetime import date
import pickle
from random import randint

from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from scipy.stats import randint as sp_randint
import matplotlib.pyplot as plt


class TrainROI():
	"""Train a regressor and test it on ROI loan data

	"""

	def __init__(self):
		self.load_data()
		self.calculate_roi()
		self.convert_to_float()
		self.split_by_grade()
		self.balance()
		self.targets = self.A_loans['roi'].values
		
		self.features = self.A_loans.drop(['loan_status', 'total_pymnt', 'roi'], 1).values
		
		self.split_train_test(test_size=0.2)

	def load_data(self):
		fileName = 'data.pickle'
		print "Loading %s" %fileName
		f = open(fileName, 'rb')
		self.loanData = pickle.load(f)

	def calculate_roi(self):
		self.loanData['roi'] = self.loanData['total_pymnt']/self.loanData['loan_amnt']

	def convert_to_float(self):
		self.loanData = self.loanData.astype(float)

	def split_by_grade(self):
		self.A_loans = self.loanData[self.loanData['A'] == 1]
		self.A_loans = self.A_loans.drop(['A', 'B', 'C', 'D', 'E', 'F', 'G'], 1)


	def split_train_test(self, test_size=0.2):
		self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
													self.features, 
													self.targets, 
													test_size=test_size)
		print "Instances in training: ", len(self.X_train)
		print "Instances in testing: ", len(self.X_test)


	def scale(self):
		self.scalerX = StandardScaler().fit(self.X_train)
		self.X_train, self.X_test = self.scalerX.transform(self.X_train), \
									self.scalerX.transform(self.X_test)

	def balance(self):
		"""Balances the default and non-default data"""
		print "Total loans before balancing: ", len(self.A_loans)
		print "Defaults before balancing: ", np.sum(self.A_loans['loan_status'] == 0)
		loans = self.A_loans
		defaults_added = 0
		for i in range(1, len(loans)):
			loan = loans[i-1:i]
			if int(loan['loan_status']) == 0:
				for n in range(13): 	#replicate the loan multiple times
					defaults_added += 1
					if defaults_added%100 == 0:
						print defaults_added
					self.A_loans = self.A_loans.append(loan)
		print "Total loans after balancing: ", len(self.A_loans)
		print "Defaults after balancing: ", np.sum(self.A_loans['loan_status'] == 0)

	def define_SVR(self, C=1.0, kernel='rbf', degree=3, gamma=0.0, coef0=0.0, shrinking=True, 
				  probability=False, tol=0.01, cache_size=200, class_weight='auto', verbose=True, 
				  max_iter=-1, random_state=None):

		print "Using a Support Vector Machine Regressor ..."
		self.regr = SVR(C=C, kernel=kernel, degree=degree, gamma=gamma, coef0=coef0, shrinking=shrinking, 
				  probability=probability, tol=tol, cache_size=cache_size, verbose=verbose, 
				  max_iter=max_iter, random_state=random_state)

		print self.regr.get_params()

	def train_regr(self):
		self.regr.fit(self.X_train, self.y_train)

	def score_regr(self, X, y):
		score = self.regr.score(X, y)
		print "Score: %0.3f" %score

	def runPCA(self, n_components=None, copy=False, whiten=False):
		print "Running PCA Dimensionality Reduction with n_components = ", n_components
		self.pca = PCA(n_components=n_components, copy=copy, whiten=whiten)
		self.X_train = self.pca.fit_transform(self.X_train)
		print "Reduced data down to ", self.pca.n_components_, " dimensions: "
		print "Transforming test data ..."
		self.X_test = self.pca.transform(self.X_test)
		#self.X_cv = self.pca.transform(self.X_cv)

	def runSVRGridSearch(self):
		C_vals = [0.001, 0.01, 0.1, 0.5, 1, 10]
		gamma_vals = [1E-4, 1E-3, 1E-2, 1E-1, 1, 1E1, 1E2]

		for C in C_vals:
			for gamma in gamma_vals:
				print "\n\n C: ", C, "  gamma: ", gamma
				self.define_SVR(C=C, gamma=gamma)
				self.train_regr()
				print "Training Scores:"
				self.score_regr(self.X_train, self.y_train)
				print "Testing Scores:"
				self.score_regr(self.X_test, self.y_test)

trainer = TrainROI()
trainer.scale()
trainer.define_SVR()
trainer.runPCA(n_components=20)
#trainer.train_regr()
#trainer.score_regr(trainer.X_test, trainer.y_test)
trainer.runSVRGridSearch()


