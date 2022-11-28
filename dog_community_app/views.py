import json
from .models import Team, Breed, Dogs, User, Adoption

from django.shortcuts import (get_object_or_404,
                              render,
                              HttpResponseRedirect)
from django.template.loader import get_template
from django.template import loader
# importing forms
from .forms import ContactUsForm, NewsletterForm, AdoptionDogDetailsForm, UserDetailsForm

# Create your views here.

from django.http import HttpResponse

def home_view(request):
    context = {}
    contact_form = ContactUsForm(request.POST or None)
    context['contact_form'] = contact_form
    if('action-contact' in request.POST):
        if(contact_form.is_valid()):
            contact_form.save()
            
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
    context = {}
    if request.method == 'GET':
        context['all_breeds'] = Breed.objects.all()
        context['filtered_breeds'] = Breed.objects.all()
    return render(request, "breed-info.html", context)

def report_dogs_view(request, type):
    context = {}
    print(type)
    if request.method == 'GET':
        context['all_breeds'] = Breed.objects.all()
    return render(request, "report_dogs.html", context)

def meetup_view(request):
    return render(request, "meetup.html")

def adoption_view(request):
    context = {}
    adoption_dog_form = AdoptionDogDetailsForm(request.POST or None)
    adoption_user_form = UserDetailsForm(request.POST or None)
    print("checking")
    context['adoption_dog_form'] = adoption_dog_form
    context['adoption_user_form'] = adoption_user_form
    print('action-adopt' in request.POST)
    if('action-adopt' in request.POST):
        if adoption_dog_form.is_valid() and adoption_user_form.is_valid():
            print(request.POST)
            adoption_user_form.save()
            user_name_p = request.POST.get('user_name')
            dog_name_p = request.POST.get('dog_name')
            print(dog_name_p)
            user_id = -1
            dog_id = -1
            for user in User.objects.filter(user_name=user_name_p):
                user_id = user.user_id
            for dog in Dogs.objects.filter(dog_name=dog_name_p):
                dog_id = dog.dog_id
            
            Adoption.objects.create(dog_id=dog_id,user_id=user_id)
            context['all_breeds'] = Breed.objects.all()
            context['filtered_dogs'] = request.session.get(
                'filtered_dogs',
                Dogs.objects.filter(is_featured=True, is_adoption_ready=True, is_adopted=False)
                )
        
            
            
    if request.method == 'GET':
        context['all_breeds'] = Breed.objects.all()
        context['filtered_dogs'] = Dogs.objects.filter(is_featured=True, is_adoption_ready=True, is_adopted=False)
        context['selected_dog_detail'] = {}
    
    return render(request, "adoption.html", context)

def adoption_dog_list(request):
    query_breed_id = request.POST.get('breed_id')
    context = {}
    adoption_dog_form = AdoptionDogDetailsForm(request.POST or None)
    adoption_user_form = UserDetailsForm(request.POST or None)
    context['adoption_dog_form'] = adoption_dog_form
    context['adoption_user_form'] = adoption_user_form
    context['all_breeds'] = Breed.objects.all()
    context['filtered_dogs'] = Dogs.objects.filter(is_featured=True, is_adoption_ready=True, is_adopted=False)
    if(request.POST.get('action') == "filter_dogs"):
        filtered_dogs = Dogs.objects.filter(is_adoption_ready=True, breed_id=query_breed_id)
        template=  get_template('adoption.html')
        context['filtered_dogs'] = filtered_dogs
        request.session['filtered_dogs'] = filtered_dogs
        result = template.render(context, request=request)
        return HttpResponse(result)
    elif(request.POST.get('action') == "featured_dogs"):
        filtered_dogs = Dogs.objects.filter(is_adoption_ready=True, is_featured=True, is_adopted=False)
        template=  get_template('adoption.html')
        context['filtered_dogs'] = filtered_dogs
        request.session['filtered_dogs'] = filtered_dogs
        result = template.render(context, request=request)
        return HttpResponse(result)
    elif(request.POST.get('action') == "breed_name_to_breed_id"):
        breed_name = request.POST.get('breed_name')
        breed_id = -1
        for breed in Breed.objects.filter(breed_name = breed_name):
            breed_id = breed.breed_id
        json_data = json.dumps({'breed_id': breed_id})
        return HttpResponse(json_data, content_type="application/json")
    elif(request.POST.get('action') == "get_dog_data"):
        dog_id = request.POST.get('dog_id')
        dog_filter = Dogs.objects.filter(is_adoption_ready=True, is_adopted=False, dog_id=dog_id)
        selected_dog_detail = {}
        for dog in dog_filter:
            selected_dog_detail = dog.dog_name
        json_data = json.dumps({'dogName': selected_dog_detail})
        return HttpResponse(json_data, content_type="application/json")

    else:
        return HttpResponse()

def contact_view(request):

    return render(request, "contact.html")