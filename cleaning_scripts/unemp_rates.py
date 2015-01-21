import pandas as pd
import numpy as np
from datetime import date
from datetime import datetime
import pickle

import mysql_connector

##load data
with open('credentials.json') as credentials_file:
    credentials = json.load(credentials_file)

passwd = credentials['mysql']['password']
con = mdb.connect(host='127.0.0.1', port=3307, user='root', passwd=passwd, db='insight', autocommit=True)

sql_query = "SELECT issue_month, issue_year from completed_loans;"
loanData = sql.read_sql(sql_query, con)



print "Putting in unemployment rates"

####Putting unemployment data in a dictionary:
mysql = mysql_connector.MySQL_Connector()
mysql.connect()
unemp_rate_tuple = mysql.execute("SELECT * FROM unemployment_rates")

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
for i, loan in enumerate(loanData):
	key_12mths = "%s%s%s" %(loanData['addr_state'][i],
							(loanData['issue_year'][i]-1),
							loanData['issue_month'][i])
	if loanData['issue_month'][i] <= 6:
		key_6mths = "%s%s%s" %(loanData['addr_state'][i],
								(loanData['issue_year'][i]-1),
								loanData['issue_month'][i]+6)
	else:
		key_6mths = "%s%s%s" %(loanData['addr_state'][i],
								(loanData['issue_year'][i]),
								loanData['issue_month'][i]-6)
	if loanData['issue_month'][i] <= 3:
		key_3mths = "%s%s%s" %(loanData['addr_state'][i],
								(loanData['issue_year'][i]-1),
								loanData['issue_month'][i]+3)
	else:
		key_3mths = "%s%s%s" %(loanData['addr_state'][i],
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

con.close()
