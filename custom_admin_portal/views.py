from django.http import HttpResponse
from django.shortcuts import render, redirect
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from dog_community_app.models import Breed,Dogs,Events,Reports,User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
import datetime 


from .forms import  CreateUserForm
# ,DogCreationForm

def register(request):
	if request.user.is_authenticated:
		return redirect('dashboard')
	else:
		form = CreateUserForm()
		if request.method == 'POST':
			form = CreateUserForm(request.POST,initial={'is_active': False})
			
			if form.is_valid():
				user = form.save()
				user.is_active = False
				user.save()
				user = form.cleaned_data.get('username')
				messages.success(request, 'Account is created for ' + user)
				messages.success(request, 'It is yet to be activated by system Administartor')

			else:
				messages.info(request, 'Failed: Registration Failed')
			

		context = {'form':form}
		return render(request, 'register.html', context)

def admin_login(request):
	if request.user.is_authenticated:
		return redirect('dashboard')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('dashboard')
			else:
				messages.info(request, 'Username / password is either incorrect or account is yet to be activated')
				

		context = {}
		return render(request, 'login.html', context)

@cache_control(no_cache=True, must_revalidate=True)
def admin_logout(request):
	logout(request)
	request.session.flush()
	return render(request, 'logout.html')
    
@login_required(login_url='login')  
def dashboard(request):
    breeds= Breed.objects.all().values()
    dogs= Dogs.objects.all().values()
    reports = Reports.objects.all().values()
    upcomingEvents = Events.objects.filter(event_time__gte=datetime.date.today()).values()
    events = Events.objects.all().values()

    if reports is None:
        reports =''
    if breeds is None:
        breeds = ''
    if dogs is None:
        dogs = ''
    if events is None:
        events = ''
    if upcomingEvents is None:
        upcomingEvents=''
    context = {
        "dog":dogs,
        "breed":breeds,
        "reports":reports,
        "customAdmin": getUserName(request),
        "events":upcomingEvents,
        "totalDogs":len(dogs),
        "totalBreeds":len(breeds),
        "totalReports":len(reports),
        "totalEvents": len(events)
    }
    return render(request, 'dashboard.html',context)

def error_page(request):
    return render(request,'error.html')

@login_required(login_url='login')
def add_breed(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            breedname = request.POST.get('breed_name')
            breedarticle =request.POST.get('breed_article')
            bred_for = request.POST.get('bred_for')
            life_span = request.POST.get('life_span')
            temperament = request.POST.get('temperament')
            origin =request.POST.get('origin')
            breed_image_path = request.FILES.get('breed_image_path')
            # upload = request.FILES['upload']
            

            breed = Breed.objects.create(breed_name = breedname, bred_for = bred_for, life_span = life_span, temperament = temperament, origin =origin,  breed_article = breedarticle, breed_image_path = breed_image_path)

            if breed is not None:
                messages.success(request, 'Sucess: Breed Added')
                return redirect('add_breed_html')
            else:
                messages.error(request, 'Failure: Breed can not be added')
        else:
            redirect('login')        
    return redirect('add_breed_html')

@login_required(login_url='login')
def register_dog(request):
    if request.method == 'POST':
        dog_name = request.POST.get('dog_name')
        dog_color =request.POST.get('dog_colour')
        dog_age = request.POST.get('dog_age')
        is_disable = request.POST.get('is_disable')
        breed_id = request.POST.get('breed_id')
        unique_identification = request.POST.get('unique_identification')
        dog_image = request.FILES.get('dog_image_path')

        disabilty = ""
        is_adopted = False
        is_adoption_ready = True
        dog  = None

        if is_disable == "1":
            disabilty = request.POST.get('disabilty')

        if breed_id is not None :
            dog  = add_dog(breed_id=breed_id, is_adopted= is_adopted,dog_name= dog_name,dog_color= dog_color, dog_age= dog_age, is_disable= is_disable, disabilty=disabilty, unique_identification=unique_identification, is_adoption_ready=is_adoption_ready, dog_image=dog_image)
       
        if dog is not None:
            messages.success(request, 'Sucess: Dog Added for adoption')
            return redirect('add_dog')
        else:
            messages.error(request, 'Failure: Dog can not be added for adoption')

    return redirect('add_dog')

def add_reporter_user(user_name,user_address,user_contact,user_email):
   
    user = User.objects.create(field_user_name=user_name,user_address=user_address,user_contact=user_contact,user_email=user_email)
    return user

def search_and_add_breed(breed_name,dog_image):
    breed = Breed.objects.filter(breed_name=breed_name).values()
    if breed is not None:
        if len(breed) > 0:
            breed_id = breed[0]["breed_id"]
            return breed_id

    breed = Breed.objects.create(breed_name=breed_name, breed_article= "",breed_image_path= dog_image)
    if breed is not None:
        return breed.breed_id
    else:
        return -1

def add_dog(breed_id,is_adopted,dog_name, dog_color, dog_age, is_disable, disabilty, unique_identification, is_adoption_ready, dog_image):
    dog = Dogs.objects.create(breed_id=breed_id, is_adopted= is_adopted,dog_name= dog_name,dog_color= dog_color, dog_age= dog_age, is_disable= is_disable, disabilty=disabilty, unique_identification=unique_identification, is_adoption_ready=is_adoption_ready, dog_image=dog_image)
    if dog is not None:
        return dog.dog_id
    else:
        return -1

@login_required(login_url='login') 
def add_event(request):
    event_location =request.POST.get('event_location')
    event_time = request.POST.get('event_time')
    event_duration = request.POST.get('event_duration')
    event_capacity = request.POST.get('event_capacity')
    event_description = request.POST.get('event_description')
    event_image = request.FILES.get('event_image')
    event = None
    event = Events.objects.create(event_location=event_location, event_duration=event_duration, event_time=event_time,event_capacity=event_capacity,event_description=event_description,event_image=event_image)

    if event is not None:
        messages.success(request, 'Sucess: Event Added')
    else:
        messages.error(request, 'Failure: Event can not be added')
       
    return redirect('add_event_html')

def event_subscribe(request):
    pass
    return redirect('dashboard')


@login_required(login_url='login') 
def add_breed_html(request):
    breed= Breed.objects.all().values()
    dogs= Dogs.objects.all().values()
    context = {
        "dogs":dogs,
        "breeds":breed,
        "report":{},
        "customAdmin": getUserName(request)
    }
    return render(request,'add_breed.html',context)


@login_required(login_url='login')
def add_dog_html(request):
    breed= Breed.objects.all().values()
    dogs= Dogs.objects.all().values()
    context = {
        "dogs":dogs,
        "breeds":breed,
        "report":{},
        "customAdmin": getUserName(request)
    }
    return render(request,'add_dog.html',context)
@login_required(login_url='login')
def add_event_html(request):
    breed= Breed.objects.all().values()
    dogs= Dogs.objects.all().values()
    context = {
        "dogs":dogs,
        "breeds":breed,
        "report":{},
        "customAdmin": getUserName(request)
    }
    return render(request,'add_event.html',context)

@login_required(login_url='login')
def update_dog_html(request):
    breeds= Breed.objects.all().values()
    dogs= Dogs.objects.all().values()
    context = {
        "dogs":dogs,
        "breeds":breeds,
        "report":{},
        "customAdmin": getUserName(request)
    }
    return render(request,'update_dog.html',context)

@login_required(login_url='login')
def update_dog(request):
    if request.method == 'POST':
        breeds= Breed.objects.all().values()
        dogs= Dogs.objects.all().values()
        context = {
            "dogs":dogs,
            "breeds":breeds,
            "report":{},
            "customAdmin": getUserName(request)
        }
        dog_id = request.POST.get('dog_details').split(",")[0]
        isAdopted = request.POST.get('is_adopted').lower() in ("yes", "true", "t", "1")
        
        dog = Dogs.objects.get(dog_id=dog_id)
        dog.is_adopted = isAdopted
        dog.is_featured  = isAdopted
        dog.is_adoption_ready = not isAdopted
        dog.save()

        if dog is not None:
            messages.success(request, 'Sucess: Dog Updated after adoption')
            return render(request,'update_dog.html',context)
        else:
            messages.error(request, 'Failure: Dog can not be updated after adoption')

        return render(request,'update_dog.html',context)
    return redirect('update_dog_html')   
def getUserName(request):
    name = str(request.user)  
    if(request.user is not None):
        if request.user.get_full_name() != '':
            name = str(request.user.get_full_name())
    return name.title()

