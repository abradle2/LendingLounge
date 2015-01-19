import mysql_connector as m

mysql = m.MySQL_Connector()
mysql.connect()

unemp_rate_tuple = mysql.execute("SELECT * FROM unemployment_rates LIMIT 20")


unemp_rate_dict = dict()
for entry in unemp_rate_tuple:
	unemp_state = entry[1]
	unemp_year = entry[2]
	unemp_month = entry[3]
	unemp_rate = entry[4]
	key = "%s%s%s" %(unemp_state, unemp_year, unemp_month)
	unemp_rate_dict[key] = unemp_rate

print unemp_rate_dict
print unemp_rate_dict['FL201212']
