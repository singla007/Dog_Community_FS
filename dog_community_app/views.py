import json
from .models import Team, Breed, Dogs

from django.shortcuts import (get_object_or_404,
                              render,
                              HttpResponseRedirect)
from django.template.loader import get_template
from django.template import loader

# importing forms
from .forms import ContactUsForm, NewsletterForm

# Create your views here.

from django.http import HttpResponse

def home_view(request):
    context = {}
    if(request.POST.get('action') == 'contact'):
        contact_form = ContactUsForm(request.POST or None)
        print(contact_form)
        if(contact_form.is_valid):
            contact_form.save()
        
        context['contact_form'] = contact_form
            
    if(request.POST.get('action') == 'newsletter'):
        newsletter_form = NewsletterForm(request.POST or None)
        if(newsletter_form.is_valid):
            newsletter_form.save()
            context['newsletter_form'] = newsletter_form
            
    team_members = Team.objects.all()
    
    context['team_members'] = team_members
    return render(request, "index.html",context)

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
    context = {}
    if request.method == 'GET':
        context['all_breeds'] = Breed.objects.all()
        context['filtered_dogs'] = Dogs.objects.filter(is_featured=True, is_adoption_ready=True)
    return render(request, "adoption.html", context)

def adoption_dog_list(request):
    query_breed_id = request.POST.get('breed_id')
    if(request.POST.get('action') == "filter_dogs"):
        filtered_dogs = Dogs.objects.filter(is_adoption_ready=True, breed_id=query_breed_id)
        template=  get_template('adoption.html')
        result = template.render({'all_breeds': Breed.objects.all(), 'filtered_dogs': filtered_dogs}, request=request)
        return HttpResponse(result)
    elif(request.POST.get('action') == "featured_dogs"):
        filtered_dogs = Dogs.objects.filter(is_adoption_ready=True, is_featured=True)
        template=  get_template('adoption.html')
        result = template.render({'all_breeds': Breed.objects.all(), 'filtered_dogs': filtered_dogs}, request=request)
        return HttpResponse(result)
    elif(request.POST.get('action') == "breed_name_to_breed_id"):
        breed_name = request.POST.get('breed_name')
        breed_id = -1
        for breed in Breed.objects.filter(breed_name = breed_name):
            breed_id = breed.breed_id
        json_data = json.dumps({'breed_id': breed_id})
        return HttpResponse(json_data, content_type="application/json")
    else:
        return HttpResponse()

def contact_view(request):

    return render(request, "contact.html")