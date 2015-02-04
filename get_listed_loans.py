import os
import pickle
import urllib2
import json
import pymysql as mdb


with open('credentials.json') as credentials_file:
    credentials = json.load(credentials_file)

passwd = credentials['mysql']['password']
con = mdb.connect(host='127.0.0.1', port=3306, user='root', passwd=passwd, db='insight', autocommit=True)
cur = con.cursor()

with open('credentials.json') as credentials_file:
    credentials = json.load(credentials_file)

api_key = credentials['lending_club']['api_key']
header = {'Authorization': api_key}
url = 'https://api.lendingclub.com/api/investor/v1/loans/listing'
req = urllib2.Request(url, None, header)
resp = urllib2.urlopen(req)

loans = resp.read()
json_data = json.loads(loans)
print json_data['loans'][0]['addrState']
s = cur.execute("truncate table listed_loans;")

for loan in json_data['loans']:
	cols = 'asOfDate,'
	vals = "'" + json_data['asOfDate'] + "',"
	for key, val in loan.iteritems():
		#deal with renaming a few columns:
		if key == "desc":
		    key = "description"
		elif key == "ID":
		    key = "IDAHO"
		elif key == "IN":
		    key = "INDIANA"
		elif key == "OR":
		    key = "OREGON"
		elif key == "OTHER":
		    key = "other_housing"
		elif key == "other":
			key = "other_purpose"			
		cols += '%s,' %key
		vals += "'%s'," %val
	cols = cols[:-1]
	vals = vals[:-1]
	sql_statement = "INSERT INTO listed_loans (%s) VALUES (%s);" %(cols, vals)
	#print sql_statement
	try:
		s = cur.execute(sql_statement)
	except mdb.err.ProgrammingError:
		print "Loan wasn't added to the database: %s" %sql_statement 
con.close()


