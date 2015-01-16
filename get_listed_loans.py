import os

from lendingclub import LendingClub


password = os.environ['LC_PASSWORD'] 
lc = LendingClub(email='abradle2@gmail.com', password=password)

lc.authenticate()

results = lc.search()

print results['loan_id']