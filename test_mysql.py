import mysql_connector as m

mysql = m.MySQL_Connector()
mysql.connect()

unemp_rate = mysql.execute("SELECT * FROM unemployment_rates \
                                    WHERE state='CA' \
                                    AND year='2014' \
                                    AND month='10' \
                                    LIMIT 10")
print unemp_rate[0][0]