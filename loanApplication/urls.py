from django.urls import path,include
from . import views
urlpatterns = [
    path('api/apply-loan/', views.ApplyLoan, name='apply-loan'),
]
