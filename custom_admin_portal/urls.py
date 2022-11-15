from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('login', admin_login, name='login'),
    path('dashboard', dashboard, name='dashboard'),
    path('register', register, name='register'),
    path('error', error_page, name='error'),
    path('logout',admin_logout,name='logout')
]
