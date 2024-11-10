from django.urls import path, include
from .views import *

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('registration', SingUp.as_view(), name='reg'),
]