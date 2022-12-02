from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('login', admin_login, name='login'),
    path('dashboard', dashboard, name='dashboard'),
    path('', dashboard, name='dashboard'),
    path('register', register, name='register'),
    path('error', error_page, name='error'),
    path('logout',admin_logout,name='logout'),
    path('add_breed',add_breed,name='add_breed'),
    path('register_dog',register_dog,name='register_dog'),
    path('add_event',add_event,name='add_event'),
    path('add_dog',add_dog_html,name='add_dog'),
    path('map',map,name='map'),
    path('add_breed_html',add_breed_html,name='add_breed_html'),
    path('adminHome',adminHome,name='adminHome'),
     path('add_event_html',add_event_html,name='add_event_html'),
]
