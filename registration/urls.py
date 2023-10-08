from django.urls import path,include
from . import views
urlpatterns = [
    path('api/register-user/', views.RegisterUser, name='register-user'),
]
