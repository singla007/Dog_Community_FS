from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('', home_view, name='main_home'),
    path('home', home_view, name='home'),
    path('breed-info', breedinfo_view, name="breed-info"),
    path('aboutus', aboutus_view, name="aboutus"),
    path('report-dogs/<type>', report_dogs_view, name="report_dogs"),
    path('report-dogs/<type>/form', report_dogs_form_view, name="report_dogs_form"),
    path('adoption', adoption_view, name="adoption"),
    path('adoption/list', adoption_dog_list, name="adoption_dog_list")

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG: #add this
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)