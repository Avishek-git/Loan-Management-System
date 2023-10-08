from datetime import date, datetime
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Payment
from .serializers import PaymentSerializer
from loanApplication.models import Loan
from .task import *
# Create your views here.

@api_view(['POST'])
def MakePayment(request):
    serializer = PaymentSerializer(data=request.data)
    if serializer.is_valid():
        loan_id = serializer.validated_data['Loan_id']
        amount_paid = serializer.validated_data['Amount']
        payment_date = date.today().replace(day=1)
        #payment_date = datetime.now().replace(day=1)
        try:
            loan = Loan.objects.get(id=loan_id)
            if loan.disbursement_date.replace(day=1) == payment_date:
                return Response({"Error": "EMI starts from next month."}, status=status.HTTP_400_BAD_REQUEST)
            checkPayment = Payment.objects.filter(Loan_id=loan_id,Payment_date=payment_date).exists()
            if checkPayment:
                return Response({"Error": "Payment for the given date already exists."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                payment = Payment(Loan_id=loan_id, Amount=amount_paid, Payment_date=payment_date)
                payment.save()
                updateEMI(loan,amount_paid,payment_date)
                payment.save()
                return Response({"Error":None}, status=status.HTTP_200_OK)

        except Loan.DoesNotExist:
            return Response({"Error": "Loan not found."}, status=status.HTTP_400_BAD_REQUEST)
    else:
        print("Invlaid")
    return Response({"Error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)