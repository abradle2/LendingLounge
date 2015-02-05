python ~/LendingLounge/get_listed_loans.py
python ~/LendingLounge/predict_listed_loans.py
sudo supervisorctl restart LendingClubWebApp
sudo supervisorctl restart LendingLoungeWebApp_staging
