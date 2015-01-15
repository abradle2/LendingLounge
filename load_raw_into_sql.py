import pandas as pd
import numpy as np
import glob, sys
from datetime import date
import pickle

import mysql_connector as m

mysql = m.MySQL_Connector()
mysql.connect()


##Load Data
files = glob.glob('./data/LoanStats3a.csv')
list1 = []
for fileName in files:
    tempFrame = pd.read_csv(fileName, header=1)
    list1.append(tempFrame)
loanData = pd.concat(list1, ignore_index=True)


##Make sure columns exist in database table
columns = list(loanData.columns.values)

#rename desc -> description 
#		id -> loan_id

for i, col in enumerate(columns):
	if col == "desc":
		columns[i] = "description"
	elif col == "id":
		columns[i] = "loan_id"
loanData.columns = columns
print columns
'''
for col in columns: 
	exists = mysql.execute("SHOW COLUMNS FROM `raw_data` LIKE '%s';" %col)
	if not exists:
		if col == "desc":
			mysql.execute("ALTER TABLE raw_data ADD description text")
		else:
			mysql.execute("ALTER TABLE raw_data ADD %s text" %col)
	else:
		print exists
'''


##Load data into table
for col in columns:
	for value in loanData[col][:1]:
		i = mysql.execute("INSERT INTO raw_data (%s) VALUES ('%s')" %(col, value));

mysql.disconnect()
