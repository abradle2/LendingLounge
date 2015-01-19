from flask import render_template
from app import app
import pymysql as mdb
import os

passwd = os.environ['MYSQL_PASSWORD']
db = mdb.connect(host='127.0.0.1', port=3307, user='root', passwd=passwd, db='insight', autocommit=True)

@app.route('/')
@app.route('/index')

def index():
	return render_template("index.html",
				title='Home', user={'nickname': 'Miguel'})

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