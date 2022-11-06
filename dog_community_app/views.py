from datetime import datetime
from .models import Team

from django.shortcuts import (get_object_or_404,
                              render,
                              HttpResponseRedirect)

# importing forms
from .forms import ContactUsForm, NewsletterForm

# Create your views here.

from django.http import HttpResponse

from django.views.generic.list import ListView

from django.views import View

def home_view(request):
    contact_form = ContactUsForm(request.POST or None)
    newsletter_form = NewsletterForm(request.POST or None)
    if(contact_form.is_valid):
        print(contact_form)
        # contact_form.save()
    if(newsletter_form.is_valid):
        print(newsletter_form)
        # newsletter_form.save()
    team_members = Team.objects.all()
    return render(request, "index.html",{"team_members":team_members})
    
def aboutus_view(request):
    return render(request, "aboutus.html")
    
def breedinfo_view(request):
    return render(request, "breedinfo.html")
    
def report_missing_dogs_view(request):
    return render(request, "missing_dogs.html")
    
def report_stray_dogs_view(request):
    return render(request, "stray_dogs.html")
    
def meetup_view(request):
    return render(request, "meetup.html")
    
def adoption_view(request):
    return render(request, "adoption.html")
    
def contact_view(request):
    return render(request, "contact.html")