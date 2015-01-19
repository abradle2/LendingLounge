#!/usr/bin/env python

import os

import pymysql

class MySQL_Connector():

	def __init__(self):
		pass
	def connect(self):
		passwd = os.environ['MYSQL_PASSWORD']
		self.conn = pymysql.connect(host='127.0.0.1', port=3307, user='root', passwd=passwd, db='insight', autocommit=True)
		self.cur = self.conn.cursor()

	def execute(self, str):
		self.cur.execute(str)
		result = self.cur.fetchall()
		#if result:
		#	print result
		return result

	def disconnect(self):
		self.cur.close()
		self.conn.close()