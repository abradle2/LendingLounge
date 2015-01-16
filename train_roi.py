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
from sklearn import preprocessing
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

		self.create_targets_features()
		self.split_train_test(train_size=0.8)
		#self.balance()

		self.X_train = self.X_train.drop(['loan_status', 'total_pymnt', 'roi'], 1).values
		self.y_train = self.y_train.values
		self.X_test = self.X_test.drop(['loan_status', 'total_pymnt', 'roi'], 1).values
		self.y_test = self.y_test.values


	def load_data(self):
		fileName = 'data.pickle'
		print "Loading %s" %fileName
		f = open(fileName, 'rb')
		self.loanData = pickle.load(f)

	def calculate_roi(self):
		self.loanData['roi'] = (self.loanData['total_pymnt']-self.loanData['funded_amnt'])/self.loanData['funded_amnt']

	def convert_to_float(self):
		self.loanData = self.loanData.astype(float)

	def split_by_grade(self, grade='A'):
		self.loans = self.loanData[self.loanData[grade] == 1]
		self.loans = self.loans.drop(['A', 'B', 'C', 'D', 'E', 'F', 'G'], 1)


	def split_train_test(self, train_size=0.8):
		mask = np.random.rand(len(self.targets)) < train_size
		self.X_train = self.features[mask]
		self.y_train = self.targets[mask]
		self.X_test = self.features[~mask]
		self.y_test = self.targets[~mask]

		print "Instances in training: ", len(self.X_train)
		print "Instances in testing: ", len(self.X_test)


	def scale(self):
		self.scalerX = StandardScaler().fit(self.X_train)
		self.X_train, self.X_test = self.scalerX.transform(self.X_train), \
									self.scalerX.transform(self.X_test)

	def standardize_samples(self):
		##0 mean, unit variance
		self.X_train = preprocessing.scale(self.X_train)
		self.X_test = preprocessing.scale(self.X_test)

	def scale_samples_to_range(self):
		##Samples lie in range between 0 and 1
		minMaxScaler = preprocessing.MinMaxScaler()
		self.X_train = minMaxScaler.fit_transform(self.X_train)
		self.X_test = minMaxScaler.fit_transform(self.X_test)

	def balance(self):
		"""Balances the training default and non-default instances"""
		print "Total loans before balancing: ", len(self.X_train)
		print "Defaults before balancing: ", np.sum(self.X_train['loan_status'] == 0)
		defaults_added = 0
		for i in range(1, len(self.X_train)):
			loan = self.X_train[i-1:i]
			loan_roi = self.y_train[i-1:i]
			if int(loan['loan_status']) == 0:
				for n in range(10): 	#replicate the loan multiple times
					defaults_added += 1
					if defaults_added%100 == 0:
						print defaults_added
					self.X_train = self.X_train.append(loan)
					self.y_train = self.y_train.append(loan_roi)
		print "Total loans after balancing: ", len(self.y_train)
		print "Defaults after balancing: ", np.sum(self.X_train['loan_status'] == 0)

	def create_targets_features(self):
		self.targets = self.loans['roi']
		self.features = self.loans

	def define_linear_regressor(self):
		self.regr = LinearRegression()

	def define_SVR(self, C=1.0, kernel='rbf', degree=3, gamma=0.0, coef0=0.0, shrinking=True, 
				  probability=False, tol=0.01, cache_size=200, class_weight='auto', verbose=True, 
				  max_iter=-1, random_state=None):
		print "Using a Support Vector Machine Regressor ..."
		self.regr = SVR(C=C, kernel=kernel, degree=degree, gamma=gamma, coef0=coef0, shrinking=shrinking, 
				  probability=probability, tol=tol, cache_size=cache_size, verbose=verbose, 
				  max_iter=max_iter, random_state=random_state)

		print self.regr.get_params()

	def define_rfr(self, n_estimators):
		self.regr = RandomForestRegressor(n_estimators=n_estimators)

	def train_regr(self):
		self.regr.fit(self.X_train, self.y_train)

	def score_regr(self, X, y):
		score = self.regr.score(X, y)
		print "Score: %0.3f" %score

	def predict(self, filename_label):
		print "predicting"
		self.prediction = self.regr.predict(self.X_test)
		print "Saving prdiction as A_%s.pickle" %filename_label
		self.save_pickle(fileName="A_%s_predict.pickle" %filename_label,
										 data=self.prediction)
		self.save_pickle(fileName="A_%s_test.pickle" %filename_label, 
										 data=self.y_test)

	def runPCA(self, n_components=None, copy=False, whiten=False):
		print "Running PCA Dimensionality Reduction with n_components = ", n_components
		self.pca = PCA(n_components=n_components, copy=copy, whiten=whiten)
		self.X_train = self.pca.fit_transform(self.X_train)
		print "Reduced data down to ", self.pca.n_components_, " dimensions: "
		print "Transforming test data ..."
		self.X_test = self.pca.transform(self.X_test)
		#self.X_cv = self.pca.transform(self.X_cv)

	def runRFRGridSearch(self):
		n_estimators = [10,50,100,500]
		for n in n_estimators:
			self.define_rfr(n_estimators=n)
			self.train_regr()
			self.predict(filename_label="rfr_n_est_%i" %n)

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
				self.predict(filename_label="svr_C_%s_gamma_%s" %(C, gamma))

	def plot_score(self):
		plt.scatter(self.prediction, self.y_test)
		plt.plot([0,1.3], [0,1.3])
		plt.xlabel('prediction')
		plt.ylabel('y_test')
		plt.show()

	def save_pickle(self, fileName, data):
		f = open(fileName, 'wb')
		pickle.dump(data, f)
		f.close()

trainer = TrainROI()
trainer.scale_samples_to_range()
trainer.standardize_samples
trainer.define_rfr(n_estimators=100)
trainer.runPCA(n_components=30)
#trainer.train_regr()
#trainer.predict(filename_label="n_estimators_100")
trainer.runRFRGridSearch()
trainer.define_SVR()
trainer.runSVRGridSearch()


#trainer.score_regr(trainer.X_test, trainer.y_test)
#trainer.plot_score()
#trainer.runSVRGridSearch()


