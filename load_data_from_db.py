#!/usr/bin/env python

"""Load the training and testing data from the database

"""
import pickle
import os
import pymysql as mdb
from pandas.io import sql
import json

with open('credentials.json') as credentials_file:
    credentials = json.load(credentials_file)

passwd = credentials['mysql']['password']
con = mdb.connect(host='127.0.0.1', port=3306, user='root', passwd=passwd, db='insight', autocommit=True)

features_defaults = [
			"id",
			"loan_amnt",
			"term",
			"int_rate",
			"installment",
			"emp_length",
			"annual_inc",
			"is_inc_v",
			"loan_status",
			"zip_code",
			"dti",
			"delinq_2yrs",
			"inq_last_6mths",
			"mths_since_last_delinq",
			"mths_since_last_record",
			"open_acc",
			"pub_rec",
			"revol_bal",
			"revol_util",
			"total_acc",
			"collections_12_mths_ex_med",
			"mths_since_last_major_derog",
			"A",
			"B",
			"C",
			"D",
			"E",
			"F",
			"G",
			"mortgage",
			"none",
			"own",                         
			"rent",                
			"issue_month",                 
			"issue_year",                              
			"car",                         
			"credit_card",                 
			"debt_consolidation",          
			"educational",                 
			"home_improvement",            
			"house",                       
			"major_purchase",              
			"medical",                     
			"moving",                      
			"renewable_energy",            
			"small_business",              
			"vacation",                    
			"wedding",                     
			"AK",                          
			"AL",                          
			"AR",                          
			"AZ",                          
			"CA",                          
			"CO",                          
			"CT",                          
			"DC",                          
			"DE",                          
			"FL",                          
			"GA",                          
			"HI",                          
			"IA",                          
			"IL",                          
			"IDAHO",                       
			"INDIANA",                     
			"KS",                          
			"KY",                          
			"LA",                          
			"MA",                          
			"MD",                          
			"ME",                          
			"MI",                          
			"MN",                          
			"MO",                          
			"MS",                          
			"MT",                          
			"NC",                          
			"NE",                          
			"NH",                          
			"NJ",                          
			"NM",                          
			"NV",                          
			"NY",                          
			"OH",                          
			"OK",                          
			"OREGON",                      
			"PA",                          
			"RI",                          
			"SC",                          
			"SD",                          
			"TN",                          
			"TX",                          
			"UT",                          
			"VA",                          
			"VT",                          
			"WA",                          
			"WI",                          
			"WV",                          
			"WY",                          
			"yrs_since_first_cr_line",     
			"desc_length",                         
			"unemp_rate_6mths",                                                                                          
			"sub_grade",                   
			"other_housing",               
			"other_purpose",
			"install_frac_of_monthly_inc",
			"implied_risk", 
			"days_to_zero_dollars"]

#get desired features for all 36 months loans
sql_query = "SELECT "
for feat in features_defaults:
	sql_query += feat + ','
sql_query = sql_query[:-1]
sql_query += " FROM completed_loans where term=0"

loanData = sql.read_sql(sql_query, con)

f = open('./pickles/mysql_dump.pickle', 'wb')
pickle.dump(loanData, f)
f.close()


con.close()
