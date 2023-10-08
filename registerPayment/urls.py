from django.urls import path,include
from . import views
urlpatterns = [
    path('api/make-payment/', views.MakePayment, name='make-payment'),
]