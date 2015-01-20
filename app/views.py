from flask import render_template
from flask import request
from flask import jsonify
from app import app
import pymysql as mdb
import os
import mysql_connector

passwd = os.environ['MYSQL_PASSWORD']
db = mdb.connect(host='127.0.0.1', port=3307, user='root', passwd=passwd, db='insight', autocommit=True)

with db:
		cur = db.cursor()
		cur.execute("SELECT * from listed_loans LIMIT 10;")
		query_results = cur.fetchall()
loans = []
for result in query_results:
	loans.append({'AsOfDate':result[0],
				  'id':result[1], 
				  'memberId': result[2],
				  'term':result[3],
				  'intRate': result[4],
				  'defaultProb': result[5],
				  'serviceFeeRate':result[6],
				  'installment':result[7],
				  'grade': result[9],
				  'empLength':result[10],
				  'homeOwnership':result[11],
				  'annualInc': result[12],
				  'isIncV':result[13],
				  'acceptD':result[14],
				  'expD':result[15],
				  'listD':result[16],
				  'creditPullD':result[17],
				  'reviewStatusD':result[18],
				  'reviewStatus':result[19],
				  'description':result[20],
				  'purpose':result[21],
				  'addrZip':result[22],
				  'addrState': result[23],
				  'investorCount':result[24],
				  'ilExpD':result[25],
				  'initialListStatus':result[26],
				  'dti': result[32],
				  'occupation': result[27],
				  
				  'openAccts': result[45],
				  'revolBl': result[48],
				  'defaultPeriod': 10})


@app.route('/')
@app.route('/index')
def index():
	return render_template("index.html",
				loans=loans, query_results=query_results[0][1])
#AJAX functions
@app.route('/default_prob')
def get_default_prob():
	default_prob = []
	loan_id = []
	for loan in loans:
		default_prob.append(loan['defaultProb'])
		loan_id.append(loan['id'])
	return jsonify(default_prob=default_prob, loan_id=loan_id)
