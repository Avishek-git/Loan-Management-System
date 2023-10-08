from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import User
from .serializers import UserSerializer
from .task import calculate_user_credit_score 

@api_view(['POST'])
def RegisterUser(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()
        # Trigger the Celery task to calculate the credit score asynchronously
        calculate_user_credit_score.delay(user.uuid)
        #calculate_user_credit_score(user.uuid)
        return Response({"Error":None,"unique_user_id":user.uuid}, status=status.HTTP_200_OK)

    return Response({"Error":serializer.errors,"unique_user_id":user.uuid}, status=status.HTTP_400_BAD_REQUEST)