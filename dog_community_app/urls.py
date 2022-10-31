from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', home_view, name='main_home'),
    path('home', home_view, name='home'),
    path('aboutus', aboutus_view, name="aboutus")

]
