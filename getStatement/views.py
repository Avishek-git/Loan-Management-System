from datetime import date, datetime
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from loanApplication.models import Loan
from registerPayment.models import Payment
from loanApplication.task import calcuateEMI
from registration.models import User

# Create your views here.

@api_view(['GET'])
def GetStatement(request):
    loan_id = request.GET.get('loan_id')
    response_message = {"Error":None,"Past_transactions":[],"Upcoming_transactions":[]}
    try:
        loan = Loan.objects.get(id=loan_id)
        if loan.status == "CLOSED":
            return Response({"Error": "Loan is closed."}, status=status.HTTP_400_BAD_REQUEST)

        payments = Payment.objects.filter(Loan_id=loan_id)

        for transaction in payments:
            resp = {}
            resp["Date"] = transaction.Payment_date
            resp["Amount_paid"] = transaction.Amount
            response_message["Past_transactions"].append(resp)

        user = User.objects.get(uuid=loan.uuid)
        temp_msg = calcuateEMI(loan.loan_amount,loan.interest_rate,loan.term_period,loan.disbursement_date,user.annual_income)
        current_date = date.today().replace(day=1).strftime("%d/%m/%y")
        temp = 0
        for due_date in temp_msg["Due_Dates"]:
            if due_date["Date"] == current_date:
                temp =1
            if temp ==1:
                response_message["Upcoming_transactions"].append(due_date)

        return Response(response_message, status=status.HTTP_200_OK)

    except Loan.DoesNotExist:
        response_message["Error"] = "Loan Not Found"
        return Response(response_message, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        response_message["Error"] = str(e)
        return Response(response_message, status=status.HTTP_400_BAD_REQUEST)

