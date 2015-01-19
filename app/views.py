from flask import render_template
from app import app
import pymysql as mdb
import os


#passwd = os.environ['MYSQL_PASSWORD']
#db = mdb.connect(host='127.0.0.1', port=3307, user='root', passwd=passwd, db='insight', autocommit=True)

@app.route('/')
@app.route('/index')

def index():

	a = 3
	loans = []
	loans.append({'id':1231, 
				  'memberId': 234, 
				  'grade': 'A2', 
				  'intRate': 8.2, 
				  'loanAmnt': 1500.00,
				  'defaultProb': 12.3,
				  'annualInc': 37000,
				  'dti': 0.43,
				  'occupation': 'Accountant',
				  'addrState': 'CA',
				  'openAccts': 9,
				  'revolBl': 12000,
				  'defaultPeriod': 10})
	loans.append({'id':1231, 
				  'memberId': 234, 
				  'grade': 'A2', 
				  'intRate': 8.2, 
				  'loanAmnt': 1500.00,
				  'defaultProb': 12.3,
				  'annualInc': 37000,
				  'dti': 0.43,
				  'occupation': 'Accountant',
				  'addrState': 'CA',
				  'openAccts': 9,
				  'revolBl': 12000,
				  'defaultPeriod': 10})
	
	return render_template("index.html",
				loans=loans)


'''
@app.route('/db')

def states_page():
	with db:
		cur = db.cursor()
		cur.execute("SELECT state from unemployment_rates LIMIT 15;")
		query_results = cur.fetchall()
	states = ""
	for result in query_results:
		states += result[0]
		states += "<br>"
	return states
'''