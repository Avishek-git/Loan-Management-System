from celery import shared_task
from .models import Loan
from registration.models import User
from datetime import datetime, timedelta

def calcuateEMI(loan_amount,interest_rate,term_period,disbursement_date,anuual_income):
    resp = {"Error":None,"Due_Dates":[]}
    interest = (loan_amount*interest_rate*term_period)/(100*12)
    monthly_emi = (loan_amount+interest)/term_period
    if monthly_emi > (0.6*float(anuual_income))/12 or interest <= 10000:
        resp["Error"]="Not Eligible for Loan"
        return resp
    else:
        next_month_start = disbursement_date.replace(day=1) + timedelta(days=32)
        for i in range(term_period):
            temp_due_dates = {}
            temp_due_dates["Date"] = next_month_start.replace(day=1).strftime("%d/%m/%y")
            temp_due_dates["Amount"] = monthly_emi
            if i==term_period-1:
                temp_due_dates["Amount"] = loan_amount+interest-(monthly_emi*(term_period-1))
            resp["Due_Dates"].append(temp_due_dates)
                
            if next_month_start.month == 12:
                next_month_start = next_month_start.replace(year=next_month_start.year + 1, month=1)
            else:
                next_month_start = next_month_start.replace(month=next_month_start.month + 1)
    return resp
