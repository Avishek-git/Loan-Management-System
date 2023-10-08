
from datetime import datetime, timedelta


def updateEMI(loan,amount,payment_date):
    loan.total_amount_paid+=amount
    next_month_start = loan.disbursement_date.replace(day=1)
    next_month_start = next_month_start.replace(month=next_month_start.month + 1)
    tenure_over = 0
    for i in range(loan.term_period):
        tenure_over+=1
        if next_month_start==payment_date:
            break
        if next_month_start.month == 12:
            next_month_start = next_month_start.replace(year=next_month_start.year + 1, month=1)
        else:
            next_month_start = next_month_start.replace(month=next_month_start.month + 1)
    remaining_tenure = loan.term_period -tenure_over
    interest = (loan.loan_amount*loan.interest_rate*loan.term_period)/(100*12)
    total_amount = loan.loan_amount+interest
    remaining_amount = total_amount-loan.total_amount_paid
    if remaining_tenure == 0:
        loan.emi_amount = remaining_amount
    else:
        loan.emi_amount = remaining_amount/remaining_tenure
    if loan.emi_amount == 0:
        loan.status = "CLOSED"
    loan.save()