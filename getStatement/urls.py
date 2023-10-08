from django.urls import path,include
from . import views
urlpatterns = [
    path('api/get-statement/', views.GetStatement, name='get-statement'),
]