import os
import pickle
import urllib2
import json

with open('credentials.json') as credentials_file:
    credentials = json.load(credentials_file)

api_key = credentials['lending_club']['api_key']
header = {'Authorization': api_key}
url = 'https://api.lendingclub.com/api/investor/v1/loans/listing'
req = urllib2.Request(url, None, header)
resp = urllib2.urlopen(req)

loans = resp.read()
json_data = json.loads(loans)
print json_data['loans'][0]['addrState']