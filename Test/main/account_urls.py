from django.urls import path, include
from .views import *
urlpatterns = [
    path('/', include('django.contrib.auth.urls')),
    path('/registration', SingUp.as_view(), name='reg'),
    path('/username_change', change_username, name='username_change'),
    path('', profile, name='profile'),
    path('/tegs', tegs, name='tegs')
]