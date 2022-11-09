from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('login', login, name='login'),
    path('dashboard', dashboard, name='dashboard'),
    path('register', register, name='register'),
    path('', include('django.contrib.auth.urls')),
    path('signup',signup,name='signup')
]
