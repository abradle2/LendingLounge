import requests
import json
import prettytable

import mysql_connector

def get_state_unemployment_rate(argyear, argmonth, state):

    #mysql = mysql_connector.MySQL_Connector()
    #mysql.connect()

    state_codes = dict()
    state_codes['AL'] = 'ST0100000000000'
    state_codes['AK'] = 'ST0200000000000' 
    state_codes['AZ'] = 'ST0400000000000'
    state_codes['AR'] = 'ST0500000000000'   
    state_codes['CA'] = 'ST0600000000000' 
    state_codes['CO'] = 'ST0800000000000'   
    state_codes['CT'] = 'ST0900000000000'
    state_codes['DE'] = 'ST1000000000000'       
    state_codes['DC'] = 'ST1100000000000'
    state_codes['FL'] = 'ST1200000000000'
    state_codes['GA'] = 'ST1300000000000'  
    state_codes['HI'] = 'ST1500000000000'   
    state_codes['ID'] = 'ST1600000000000'    
    state_codes['IL'] = 'ST1700000000000'     
    state_codes['IN'] = 'ST1800000000000'  
    state_codes['IA'] = 'ST1900000000000'     
    state_codes['KS'] = 'ST2000000000000'  
    state_codes['KY'] = 'ST2100000000000' 
    state_codes['LA'] = 'ST2200000000000'    
    state_codes['ME'] = 'ST2300000000000'    
    state_codes['MD'] = 'ST2400000000000'     
    state_codes['MA'] = 'ST2500000000000'    
    state_codes['MI'] = 'ST2600000000000'      
    state_codes['MN'] = 'ST2700000000000'     
    state_codes['MS'] = 'ST2800000000000'   
    state_codes['MO'] = 'ST2900000000000'      
    state_codes['MT'] = 'ST3000000000000'  
    state_codes['NE'] = 'ST3100000000000'     
    state_codes['NV'] = 'ST3200000000000'   
    state_codes['NH'] = 'ST3300000000000'     
    state_codes['NJ'] = 'ST3400000000000'   
    state_codes['NM'] = 'ST3500000000000'   
    state_codes['NY'] = 'ST3600000000000'     
    state_codes['NC'] = 'ST3700000000000'   
    state_codes['ND'] = 'ST3800000000000'     
    state_codes['OH'] = 'ST3900000000000'     
    state_codes['OK'] = 'ST4000000000000'     
    state_codes['OR'] = 'ST4100000000000'   
    state_codes['PA'] = 'ST4200000000000'     
    state_codes['RI'] = 'ST4400000000000'     
    state_codes['SC'] = 'ST4500000000000'   
    state_codes['SD'] = 'ST4600000000000'     
    state_codes['TN'] = 'ST4700000000000'    
    state_codes['TX'] = 'ST4800000000000'    
    state_codes['UT'] = 'ST4900000000000'     
    state_codes['VT'] = 'ST5000000000000'  
    state_codes['VA'] = 'ST5100000000000'     
    state_codes['WA'] = 'ST5300000000000'   
    state_codes['WV'] = 'ST5400000000000'    
    state_codes['WI'] = 'ST5500000000000'    
    state_codes['WY'] = 'ST5600000000000'  
    state_codes['PR'] = 'ST7200000000000'

    series_IDs = ''
    for state in state_codes:
        series_IDs += "\'" + state_codes[state] + "03\', "
    series_IDs = series_IDs[:-2]

    headers = {'Content-type': 'application/json'} 
    exec('data = json.dumps({"seriesid": [%s],"startyear": 2007, \
                                                 "endyear": 2015})' %series_IDs)
    
    print "http://api.bls.gov/publicAPI/v1/timeseries/%s/" %data
    p = requests.post('http://api.bls.gov/publicAPI/v1/timeseries/data/:10800', data=data, headers=headers) 
    json_data = json.loads(p.text)
    for series in json_data['Results']['series']:
        x=prettytable.PrettyTable(["series id","year","period","value"])
        seriesId = series['seriesID']
        for item in series['data']:
            year = item['year']
            period = item['period'][1:]
            u_rate = item['value']
            '''
            exists = mysql.execute("SELECT * FROM unemployment_rates \
                                    WHERE state=\'%s\' \
                                    AND year=\'%s\' \
                                    AND month=\'%s\' \
                                    LIMIT 1" %(state, argyear, argmonth))
            if exists:
                pass
            else:
                statement = "INSERT INTO unemployment_rates (state, year, month, unemp_rate) \
                                    VALUES (\'%s\', \
                                    \'%s\', \
                                    \'%s\', \
                                    \'%s\')" %(state, year, period, u_rate)
                print statement
                mysql.execute(statement)
            '''
            
            x.add_row([seriesId,year,period,u_rate])
        print x.get_string()
        mysql.disconnect()
        


get_state_unemployment_rate(2014, 'M11', 'CO')