"""Module for manipulating training and testing data"""
import pandas as pd
import numpy as np

from sklearn.cross_validation import train_test_split
from sklearn import preprocessing

def scale(X_train, X_test):
	scalerX = preprocessing.StandardScaler().fit(X_train)
	X_train, X_test = scalerX.transform(X_train), \
								scalerX.transform(X_test)
	return (X_train, X_test)

def standardize_samples(X_train, X_test):
	##0 mean, unit variance
	X_train = preprocessing.scale(X_train)
	X_test = preprocessing.scale(X_test)
	return (X_train, X_test)

def scale_samples_to_range(X_train, X_test):
	##Samples lie in range between 0 and 1
	minMaxScaler = preprocessing.MinMaxScaler()
	X_train = minMaxScaler.fit_transform(X_train)
	X_test = minMaxScaler.fit_transform(X_test)
	return (X_train, X_test)

def split_train_test(features, targets, test_size=0.2):
	X_train, X_test, y_train, y_test = train_test_split(features, 
																targets, 
																test_size=test_size)
	X_train = X_train.astype(float)
	y_train = y_train.astype(float)
	X_test = X_test.astype(float)
	y_test = y_test.astype(float)

	print "Loans in training set: ", len(y_train)
	print "Loans in testing set: ", len(y_test)

	return (X_train, X_test, y_train, y_test)
