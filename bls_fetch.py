import requests
import json
import prettytable

import mysql_connector

def get_state_unemployment_rate():

    mysql = mysql_connector.MySQL_Connector()
    mysql.connect()

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

    inverse_state_codes = dict()
    for key, val in state_codes.items():
        inverse_state_codes[val] = key

    data = open('unemployment_stats_4.txt')
    json_data = json.load(data)

    #json_data = json.loads(p.text)
    for series in json_data['Results']['series']:
        x=prettytable.PrettyTable(["series id","state","year","month","value"])
        seriesId = series['seriesID']
        state = inverse_state_codes[seriesId[3:-2]]
        for item in series['data']:
            year = item['year']
            month = item['period'][1:]
            u_rate = item['value']
            
            exists = mysql.execute("SELECT * FROM unemployment_rates \
                                    WHERE state=\'%s\' \
                                    AND year=\'%s\' \
                                    AND month=\'%s\' \
                                    LIMIT 1" %(state, year, month))
            if exists:
                pass
            else:
                statement = "INSERT INTO unemployment_rates (state, year, month, unemp_rate) \
                                    VALUES (\'%s\', \
                                    \'%s\', \
                                    \'%s\', \
                                    \'%s\')" %(state, year, month, u_rate)
                print statement
                mysql.execute(statement)
            
            
            
            x.add_row([seriesId,state,year,month,u_rate])
        print x.get_string()

    mysql.disconnect()

get_state_unemployment_rate()