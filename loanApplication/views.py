from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Loan
from .serializers import LoanSerializer
from .task import *
from .loan_limit import *


@api_view(['POST'])
def ApplyLoan(request):
    serializer = LoanSerializer(data=request.data)
    response = {"Error":None,"Loan_id":None,"Due_dates":[]}
    if serializer.is_valid():
        user_id = serializer.validated_data['uuid']
        loan_type = serializer.validated_data['loan_type']
        loan_amount = serializer.validated_data['loan_amount']
        interest_rate = serializer.validated_data['interest_rate']
        term_period = serializer.validated_data['term_period']
        disbursement_date = serializer.validated_data['disbursement_date']
        
        try:
            user = User.objects.get(pk=user_id)
            credit_score = user.credit_score
            anuual_income = user.annual_income  
            print(credit_score,anuual_income)        
            if credit_score>=450 and anuual_income>=150000:
                if loan_type == 'Car' and loan_amount <= CAR_LOAN_LIMIT and interest_rate>=14:
                    resp = calcuateEMI(loan_amount,interest_rate,term_period,disbursement_date,anuual_income)
                elif loan_type == 'Home' and loan_amount <= HOME_LOAN_LIMIT and interest_rate>=14:
                    resp = calcuateEMI(loan_amount,interest_rate,term_period,disbursement_date,anuual_income)
                elif loan_type == 'Education' and loan_amount <= EDUCATIONAL_LOAN_LIMIT and interest_rate>=14:
                    resp = calcuateEMI(loan_amount,interest_rate,term_period,disbursement_date,anuual_income)
                elif loan_type == 'Personal' and loan_amount <= PERSONAL_LOAN_LIMIT and interest_rate>=14:
                    resp = calcuateEMI(loan_amount,interest_rate,term_period,disbursement_date,anuual_income)
                else:
                    response["Error"]="Not Eligible for Loan"
                    return Response(response, status=status.HTTP_400_BAD_REQUEST)
            else:
                response["Error"]="Not Eligible for Loan"
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            response["Error"] = e
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        if resp["Error"]==None:
            loan = serializer.save()
            loan.emi_amount = resp["Due_Dates"][0]["Amount"]
            loan.total_amount_paid = 0
            loan.status = "OPEN"
            loan.save()
            response["Due_dates"]=resp["Due_Dates"]
            response["Loan_id"]=loan.id
            return Response(response, status=status.HTTP_200_OK)
        else:
            response["Error"]="Not Eligible for Loan"
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    response["Error"]=serializer.errors
    return Response(response, status=status.HTTP_400_BAD_REQUEST)