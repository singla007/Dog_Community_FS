import json
from .models import Team, Breed, Dogs, User, Adoption, Reports, Events, EventSubscription

from django.shortcuts import (get_object_or_404,
                              render,
                              redirect,
                              HttpResponseRedirect)
from django.template.loader import get_template
from django.template import loader
from django.core.mail import send_mail
from datetime import datetime
# importing forms
from .forms import ContactUsForm, NewsletterForm, AdoptionDogDetailsForm, UserDetailsForm, ReportDogDetails, ReportLastLocation

# Create your views here.

from django.http import HttpResponse

def home_view(request):
    context = {}
    contact_form = ContactUsForm(request.POST or None)
    context['contact_form'] = contact_form
    # if(request.GET and request.GET['contactmessage']):
    #     print(request.GET['contactmessage'])
    # print(request.GET.get("contactmessage"))
    # if request.GET.getlist("contact-message"):
    #     print("checking")
    #     contact_form = ContactUsForm(request.POST or None, initial={'message': request.GET.getlist("contact-message")})
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
    context['report_type'] = type
    context['all_breeds'] = Breed.objects.all()
    
    return render(request, "report_dogs.html", context)

def report_dogs_form_view(request, type):
    context = {}
    context['all_breeds'] = Breed.objects.all()
    user_details = UserDetailsForm(request.POST or None)
    dog_details = ReportDogDetails(request.POST or None)
    dog_last_location = ReportLastLocation(request.POST or None)
    context['user_details'] = user_details
    context['dog_details'] = dog_details
    context['dog_last_location'] = dog_last_location
    if('action-report' in request.POST):
        dog_details_updated = ReportDogDetails(request.POST, request.FILES)
        if dog_details_updated.is_valid() and dog_last_location.is_valid():
            is_dog_exist = False
            dog_id = -1
            user_id = -1
            for dog in Dogs.objects.filter(dog_name=request.POST.get('dog_name'), dog_age=request.POST.get('dog_age'), dog_color=request.POST.get('dog_color') ):
                is_dog_exist = True
                dog_id = dog.dog_id
            
            if is_dog_exist:
                # show snackbar if dog has already been reported
                pass 
            else: 
                print("dog validated")
                dog_instance = dog_details_updated.save(commit=False)
                dog_instance.is_adopted = False
                dog_instance.is_disable = True if request.POST.get('is_disable')=='on' else False
                dog_instance.is_adoption_ready = False if dog_instance.is_disable else True
                dog_instance.is_featured = False
                dog_instance.save() # saving dog in the Dogs model
                
                for dog in Dogs.objects.filter(dog_name=request.POST.get('dog_name'), dog_age=request.POST.get('dog_age'), dog_color=request.POST.get('dog_color') ):
                    dog_id = dog.dog_id
                if type == "missing":
                    if user_details.is_valid():
                        print("user and dog validated")
                        user_name_p = request.POST.get('user_name')
                        user_contact_p = request.POST.get('user_contact')
                        print(user_name_p)
                        user_details.save()  # saving the user in the Users model
                        for user in User.objects.filter(user_name=user_name_p, user_contact=user_contact_p):
                            user_id = user.user_id
                elif type == "stray":
                    for user in User.objects.filter(user_name='Dog Community'):
                        user_id = user.user_id
                
                # create report object in the Reports model
                if dog_id>-1 and user_id>-1:
                    Reports.objects.create(
                        dog_id = dog_id,
                        breed_id = request.POST.get('breed'),
                        reporter_id = user_id,
                        last_known_location = request.POST.get('last_known_location'),
                        category = type                    
                    )
                    if type == 'missing':
                        return redirect('missing-form-success', id=dog_id, user_id=user_id)
                    elif type == 'stray':
                        return redirect('stray-form-success', id=dog_id, user_id=user_id)
    return render(request, "report_dogs_form.html", context)

def meetup_view(request):
    context = {}
    context['meetups'] = Events.objects.all()
    user_form = UserDetailsForm(request.POST or None)
    context['user_form'] = user_form
    if request.method == 'POST':
        if 'action-meetup' in request.POST:
            if user_form.is_valid():
                user_name_p = request.POST.get('user_name')
                user_contact_p = request.POST.get('user_contact')
                user_email_p = request.POST.get('user_email')
                is_user_exist = False
                user_id = -1
                event_id = request.POST.get('event_id')
                for user in User.objects.filter(user_name=user_name_p, user_contact=user_contact_p):
                    is_user_exist = True
                    user_id = user.user_id
                    
                if not is_user_exist:
                    user_form.save()
                    for user in User.objects.filter(user_name=user_name_p, user_contact=user_contact_p):
                        user_id = user.user_id

                # create report object in the Reports model
                if user_id>-1:
                    EventSubscription.objects.create(
                        event_id = request.POST.get('event_id'),
                        user_id = user_id                 
                    )
                    return redirect('meetup-success', id=event_id, user_id=user_id)
                    
    return render(request, "meetup.html", context)

def adoption_view(request):
    context = {}
    adoption_dog_form = AdoptionDogDetailsForm(request.POST or None)
    adoption_user_form = UserDetailsForm(request.POST or None)
    context['adoption_dog_form'] = adoption_dog_form
    context['adoption_user_form'] = adoption_user_form
    context['all_breeds'] = Breed.objects.all()
    context['filtered_dogs'] = request.session.get(
        'filtered_dogs',
        Dogs.objects.filter(is_featured=True, is_adoption_ready=True, is_adopted=False)
        )
    if('action-adopt' in request.POST):
        if adoption_dog_form.is_valid() and adoption_user_form.is_valid():
            is_user_exist = False
            user_id = -1
            dog_id = -1
            
            user_name_p = request.POST.get('user_name')
            user_contact_p = request.POST.get('user_contact')
            dog_name_p = request.POST.get('dog_name')
            
            for user in User.objects.filter(user_name=user_name_p, user_contact=user_contact_p):
                is_user_exist = True
                user_id = user.user_id
            
            if not is_user_exist:
                adoption_user_form.save()      
                for user in User.objects.filter(user_name=user_name_p,user_contact=user_contact_p):
                    user_id = user.user_id
            for dog in Dogs.objects.filter(dog_name=dog_name_p):
                dog_id = dog.dog_id
            
            return redirect('adoption-success', id=dog_id, user_id=user_id)
            # Adoption.objects.create(dog_id=dog_id,user_id=user_id)
    return render(request, "adoption.html", context)

def success_view(request, user_id, id):
    context={}
    print(id,user_id,request.path)
    data = {}
    user_email = ''
    if int(id)>-1 and int(user_id)>-1:
        if 'meetup/success' in request.path:
            context['action'] = 'meetup'
            for event in Events.objects.filter(event_id=id):
                event_time_calculated = event.event_time.strftime("%I:%M %p")
                data = {
                    'event_id': event.event_id,
                    'event_location': event.event_location,
                    'event_time': event_time_calculated,
                    'event_duration': event.event_duration
                }
        if 'adoption/success' in request.path:
            context['action'] = 'adoption'
            for dog in Dogs.objects.filter(dog_id=id):
                data = {
                    'dog_id': dog.dog_id,
                    'dog_name': dog.dog_name,
                    'dog_age': dog.dog_age,
                    'dog_color': dog.dog_color
                }
        if 'report-dogs' in request.path and 'form/success' in request.path:
            for dog in Dogs.objects.filter(dog_id=id):
                data = {
                    'dog_id': dog.dog_id,
                    'dog_name': dog.dog_name,
                    'dog_age': dog.dog_age,
                    'dog_color': dog.dog_color,
                    'unique_identification': dog.unique_identification
                }
            for dog in Reports.objects.filter(dog_id=id):
                data['dog_last_location'] = dog.last_known_location
                
            if 'missing' in request.path:
                context['action'] = 'report-missing'
            else:
                context['action'] = 'report-stray'
                
        for user in User.objects.filter(user_id=user_id):
            first_name = user.user_name.split(' ')[0]
            user_name = first_name
            user_email = user.user_email
        context['id'] = id
        context['data'] = data
        context['user_email'] = user_email
        context['user_name'] = user_name
    else:
        pass  # handle when the user is not propogated properly
    
    return render(request, 'success.html', context)

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
        print("i am coming")
        filtered_dogs = Dogs.objects.filter(is_adoption_ready=True, breed_id=query_breed_id)
        template=  get_template('adoption.html')
        context['filtered_dogs'] = filtered_dogs
        result = template.render(context, request=request)
        # request.session['filtered_dogs'] = filtered_dogs
        return HttpResponse(result)
    elif(request.POST.get('action') == "featured_dogs"):
        filtered_dogs = Dogs.objects.filter(is_adoption_ready=True, is_featured=True, is_adopted=False)
        template=  get_template('adoption.html')
        context['filtered_dogs'] = filtered_dogs
        # request.session['filtered_dogs'] = filtered_dogs
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