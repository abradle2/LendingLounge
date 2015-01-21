import pymysql
import json
with open('credentials.json') as credentials_file:
			credentials = json.load(credentials_file)
passwd = credentials['mysql']['password']
conn = pymysql.connect(host='127.0.0.1', 
					   port=3307, 
					   user='root', 
					   passwd=passwd, 
					   db='insight', 
					   autocommit=True)
cur = conn.cursor()

sql_command = "SELECT * FROM test;"

cur.execute(sql_command)
result = cur.fetchall()
print result[0][1]

cur.close()
conn.close()

