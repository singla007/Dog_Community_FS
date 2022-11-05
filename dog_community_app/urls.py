from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('', home_view, name='main_home'),
    path('home', home_view, name='home'),
    path('aboutus', aboutus_view, name="aboutus"),
    path('report_missing_dogs', report_missing_dogs_view, name="report_missing_dogs"),
    path('report_stray_dogs', report_stray_dogs_view, name="report_stray_dogs"),
    path('adoption', adoption_view, name="adoption")

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
