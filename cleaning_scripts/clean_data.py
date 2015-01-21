import pandas as pd
import numpy as np
import glob, sys
from datetime import date
from datetime import datetime
import pickle
import base64

import mysql_connector

##Load Data
files = glob.glob('./data/LoanStats3a.csv')
list1 = []
for fileName in files:
    print "loading file ", fileName
    tempFrame = pd.read_csv(fileName, header=1)
    list1.append(tempFrame)
print "concatenating files"
loanData = pd.concat(list1, ignore_index=True)


##remove all non-finished loans
print "loan_status"
loanData = loanData[[x in ['Charged Off',
						   'Default', 
						   'Fully Paid', 
						   'Does not meet the credit policy.  Status:Charged Off',
						   'Does not meet the credit policy.  Status:Default',
						   'Does not meet the credit policy.  Status:Fully Paid'
						   ] for x in loanData['loan_status']]]
loanData.index = range(len(loanData))
print "loans: ", len(loanData)


##int_rate
print "int_rate"
loanData['int_rate'] = loanData['int_rate'].str.replace('%', '')
loanData['int_rate'] = loanData['int_rate'].astype(float)


##term
print "term"
loanData['term'] = [0 if x == " 36 months" else 1 for x in loanData['term']]



##grade
print "grade"
loanData = loanData[pd.isnull(loanData['grade']) == 0]
loanData.index = range(len(loanData))
print "loans: ", len(loanData)



#grades = dict(zip(loanData['grade'].unique(), np.arange(loanData['grade'].nunique())))
#loanData['grade'] = loanData['grade'].map(lambda x: grades[x])


#Binarize the grade
gradesBinarized = pd.get_dummies(loanData['grade'])
loanData = pd.concat([loanData, gradesBinarized], axis=1)
loanData = loanData.drop(['grade'], 1)


#Subgrade - numeric part of LendingClub's subgrade (ie: b3 -> grade=b, subgrade=3)
loanData['sub_grade'] = [x[1:] for x in loanData['sub_grade']]


##emp_length
print "emp_length"
emp_years = dict(zip(loanData['emp_length'].unique(), np.arange(loanData['emp_length'].nunique())))
loanData['emp_length'] = loanData['emp_length'].map(lambda x: emp_years[x])


##home_ownership
#loanData['home_ownership'] = ["None" if pd.isnull(x) else x for x in loanData['home_ownership']]
#ownership_dict = dict(zip(loanData['home_ownership'].unique(), np.arange(loanData['home_ownership'].nunique())))
#loanData['home_ownership'] = loanData['home_ownership'].map(lambda x: ownership_dict[x])


homeOwnershipBinarized = pd.get_dummies(loanData['home_ownership'])
loanData = pd.concat([loanData, homeOwnershipBinarized], axis=1)



##is_inc_v
#possible values:
#	Source Verified
#	Verified
#	Not Verified
loanData['is_inc_v'] = [1 if x == "Source Verified" else x for x in loanData['is_inc_v']]
loanData['is_inc_v'] = [2 if x == "Verified" else x for x in loanData['is_inc_v']]
loanData['is_inc_v'] = [0 if x == "Not Verified" else x for x in loanData['is_inc_v']]

##Deal with datetimes and create days_active
loanData = loanData[pd.notnull(loanData['last_pymnt_d'] )]
loanData.index = range(len(loanData))
print loanData['last_pymnt_d'].unique()

loanData['issue_d'] = [datetime.strptime(str(x), '%b-%Y') for x in loanData['issue_d']]
loanData['last_pymnt_d'] = [datetime.strptime(str(x), '%b-%Y') for x in loanData['last_pymnt_d']]
days_active = [(loanData['last_pymnt_d'][i] - loanData['issue_d'][i]).days for i in range(len(loanData))]
loanData['days_active'] = days_active


##issue_month and issue_year
print "issue_month"
loanData['issue_d'] = pd.to_datetime(loanData['issue_d'])
loanData['last_pymnt_d'] = pd.to_datetime(loanData['last_pymnt_d'])


loanData['issue_month'] = 0
loanData['issue_year'] = 0
loanData['last_pymnt_month'] = 0
loanData['last_pymnt_year'] = 0
print "entering for loop issue_m and issue_y"
for i in range(len(loanData['issue_d'])):
    m = pd.to_datetime(loanData['issue_d'][i]).month
    y = pd.to_datetime(loanData['issue_d'][i]).year
    loanData['issue_month'].iloc[i] = m
    loanData['issue_year'].iloc[i] = y

    m_last = pd.to_datetime(loanData['last_pymnt_d'][i]).month
    y_last = pd.to_datetime(loanData['last_pymnt_d'][i]).year
    loanData['last_pymnt_month'].iloc[i] = m_last
    loanData['last_pymnt_year'].iloc[i] = y_last
    if i%100 == 0:
    	print i


##purpose
print "purpose"
purposeBinarized = pd.get_dummies(loanData['purpose'])
loanData = pd.concat([loanData, purposeBinarized], axis=1)

##zip_code
loanData['zip_code'] = [x[:3] for x in loanData['zip_code']]


##addr_state
statesBinarized = pd.get_dummies(loanData['addr_state'])
loanData = pd.concat([loanData, statesBinarized], axis=1)


##yrs_since_first_cr_line
print "yrs_since_first_cr_line"
loanData['yrs_since_first_cr_line'] = 0
for i in range(len(loanData['earliest_cr_line'])):
    earliest_year = pd.to_datetime(loanData['earliest_cr_line'][i]).year
    loanData['yrs_since_first_cr_line'].iloc[i] = date.today().year - earliest_year


##delinquencies
loanData['mths_since_last_delinq'] = [-1 if pd.isnull(x) else x for x in loanData['mths_since_last_delinq']]


##records
print "records"
loanData['mths_since_last_record'] = [-1 if pd.isnull(x) else x for x in loanData['mths_since_last_record']]


##revol_util
loanData['revol_util'] = loanData['revol_util'].str.replace('%', '')
loanData['revol_util'] = loanData['revol_util'].astype(float)
loanData['revol_util'] = [-1 if pd.isnull(x) else x for x in loanData['revol_util']]


##initial_list_status
print "initial_list_status"
loanData['initial_list_status'] = [1 if x in ['w', 'W'] else 0 for x in loanData['initial_list_status']]


##major_derog
loanData['mths_since_last_major_derog'] = [-1 if pd.isnull(x) else x for x in loanData['mths_since_last_major_derog']]


##collections_12_mths_ex_med
loanData['collections_12_mths_ex_med'] = [-1 if pd.isnull(x) else x for x in loanData['collections_12_mths_ex_med']]


##Remove features which aren't available for new loan listings
print "removing features"
#loanData = loanData.drop('total_pymnt', 1)
loanData = loanData.drop('initial_list_status', 1)



loanData['loan_status'] = [0 if x in ['Charged Off',
						   			  'Default',
								      'Does not meet the credit policy.  Status:Charged Off',
								      'Does not meet the credit policy.  Status:Default'
						   			 ] else 1 for x in loanData['loan_status'] ]



##desc_length
print "putting in lengths of string features"
loanData['desc_length'] = [len(str(x)) for x in loanData['desc']]

##title_length
loanData['title_length'] = [len(str(x)) for x in loanData['title']]

##emp_title
loanData['emp_title'] = [len(str(x)) for x in loanData['emp_title']]


##desc
loanData['desc'] = [base64.b64encode(str(x)) for x in loanData['desc']]

##Drop 0 and negative annual incomes. Also drop huge incomes
loanData = loanData[loanData['annual_inc'] > 0]
loanData = loanData[loanData['annual_inc'] < 2000000]

##engineer new feature
loanData['install_frac_of_monthly_inc'] = loanData['installment']/loanData['annual_inc']*12.0


##Drop loans with missing values
#print "dropping NAs"
#loanData = loanData.dropna()
#loanData.index = range(len(loanData))
print "loans: ", len(loanData)

print "Putting in unemployment rates"

####Putting unemployment data in a dictionary:
mysql = mysql_connector.MySQL_Connector()
mysql.connect()
unemp_rate_tuple = mysql.execute("SELECT * FROM unemployment_rates")

unemp_rate_dict = dict()
for entry in unemp_rate_tuple:
	unemp_state = entry[1]
	unemp_year = entry[2]
	unemp_month = entry[3]
	unemp_rate = entry[4]
	key = "%s%s%s" %(unemp_state, unemp_year, unemp_month)
	unemp_rate_dict[key] = unemp_rate
loanData['unemp_rate_12mths'] = 0
loanData['unemp_rate_6mths'] = 0
loanData['unemp_rate_3mths'] = 0
for i, loan in enumerate(loanData):
	key_12mths = "%s%s%s" %(loanData['addr_state'][i],
							(loanData['issue_year'][i]-1),
							loanData['issue_month'][i])
	if loanData['issue_month'][i] <= 6:
		key_6mths = "%s%s%s" %(loanData['addr_state'][i],
								(loanData['issue_year'][i]-1),
								loanData['issue_month'][i]+6)
	else:
		key_6mths = "%s%s%s" %(loanData['addr_state'][i],
								(loanData['issue_year'][i]),
								loanData['issue_month'][i]-6)
	if loanData['issue_month'][i] <= 3:
		key_3mths = "%s%s%s" %(loanData['addr_state'][i],
								(loanData['issue_year'][i]-1),
								loanData['issue_month'][i]+3)
	else:
		key_3mths = "%s%s%s" %(loanData['addr_state'][i],
								(loanData['issue_year'][i]),
								loanData['issue_month'][i]-3)
	try:
		loanData['unemp_rate_12mths'].iloc[i] = unemp_rate_dict[key_12mths]
		loanData['unemp_rate_6mths'].iloc[i] = unemp_rate_dict[key_6mths]
		loanData['unemp_rate_3mths'].iloc[i] = unemp_rate_dict[key_3mths]
	except KeyError:
		print KeyError, "loan ", i
		loanData = loanData.drop(loanData.index[i])
		loanData.index = range(len(loanData))


#Putting in interest rate swap-engineered feature
print "calculating implied risk"
int_rate_swap_tuple = mysql.execute("SELECT * FROM interest_rate_swaps")

int_rate_swap_dict = dict()
for entry in int_rate_swap_tuple:
	int_rate_swap_year = entry[1]
	int_rate_swap_rate = entry[3]
	int_rate_swap_dict[int_rate_swap_year] = int_rate_swap_rate
	unemp_rate_dict[key] = unemp_rate
loanData['implied_risk'] = 0
loanData.index = range(len(loanData))
indices_to_drop = []
for i in range(len(loanData)):
    if i%100 == 0:
        print i
    year_i = loanData['issue_year'][i]
    swap_rate_i = int_rate_swap_dict[year_i]
    int_rate_i = loanData['int_rate'][i]
    impl_risk = int_rate_i - swap_rate_i
    try:
        loanData['implied_risk'].iloc[i] = impl_risk
    except Error:
        print Error, "loan ", i
loanData = loanData[loanData['implied_risk'] != 0]
loanData.index = range(len(loanData))


##Pickle the dataframe
print "pickling"
f = open('data.pickle', 'wb')
pickle.dump(loanData, f)
f.close()


##Writing cleaned data to the database
col_string = ""
for col in loanData.columns:
    if col == "desc":
        next_col = "description"
    elif col == "ID":
        next_col = "IDAHO"
    elif col == "IN":
        next_col = "INDIANA"
    elif col == "OR":
        next_col = "OREGON"
    elif col == "OTHER":
        next_col = "other_housing"
    elif col == "other":
        next_col = "other_purpose"
    else:
        next_col = col
    col_string += "%s," %(next_col)
col_string = col_string[:-1]

for i in range(len(loanData)-1):
	vals_string = ""
	for item in loanData.iloc[i]:
	    vals_string += "'" + str(item) + "',"
	vals_string = vals_string[:-1]
	sql_insert_string = "INSERT INTO completed_loans (%s) VALUES (%s)" %(col_string, vals_string)
	if i%1000 == 0:
	    print "Inserting %s into database" %i
	try:
		insert_query = mysql.execute(sql_insert_string)
	except:
		print "Insert Failed "
		e = sys.exc_info()
		print e
		print loanData.iloc[i]
	


mysql.disconnect()

