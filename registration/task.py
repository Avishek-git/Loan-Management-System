import csv
from celery import shared_task
from .models import User

@shared_task
def calculate_user_credit_score(uuid):
    user = User.objects.get(pk=uuid)
    balance = 0 #check no balance case
    credit_score = 300
    with open("./registration/transactions_data_Backend.csv","r") as f:
        csvreader = csv.reader(f)
        next(csvreader)
        for row in csvreader:
            if row[0]==uuid:
                if row[2]=="DEBIT":
                    balance -= float(row[3])
                elif row[2]=="CREDIT":
                    balance += float(row[3])
        f.close()
    if balance>=1000000:
        credit_score = 900
    elif balance<=100000:
        credit_score = 300
    else:
        temp = int(balance/15000)
        temp *= 10
        credit_score += temp
    user.credit_score = credit_score
    user.save()
