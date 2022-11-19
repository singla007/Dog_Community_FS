from django.http import HttpResponse
from django.shortcuts import render, redirect
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from dog_community_app.models import Breed,Dogs,Events,Reports,User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
# Create your views here.
from .forms import  CreateUserForm,DogCreationForm



def register(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		form = CreateUserForm()
		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			if form.is_valid():
				form.save()
				user = form.cleaned_data.get('username')
				messages.success(request, 'Account was created for ' + user)

				return redirect('login')
			

		context = {'form':form}
		return render(request, 'adminPortal/register.html', context)

def admin_login(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('dashboard')
			else:
				messages.info(request, 'Username OR password is incorrect')

		context = {}
		return render(request, 'adminPortal/login.html', context)

def admin_logout(request):
	logout(request)
	return render(request, 'logout.html')


def error_page(request):
    return render(request,'error.html')
    
@login_required(login_url='login')  
def dashboard(request):
    breed= Breed.objects.all().values()
    dogs= Dogs.objects.all().values()
    print(breed)
    context = {
        "dog":dogs,
        "breed":breed,
        "report":{}
    }
    return render(request, 'dashboard/index.html',context)
@login_required(login_url='login')
def add_breed(request):
    if request.method == 'POST':
        breedname = request.POST.get('breed_name')
        breedarticle =request.POST.get('breed_article')
        breed_image_path = request.POST.get('breed_image_path')

        breed = Breed.objects.create(breed_name=breedname, breed_article= breedarticle,breed_image_path= breed_image_path)

        if breed is not None:
            messages.success(request, 'Sucess: Breed Added')
            return redirect('dashboard')
        else:
            messages.error(request, 'Failure: Breed can not be added')
    return redirect('dashboard')

@login_required(login_url='login')
def register_dog(request):
    if request.method == 'POST':	
        breed_name = request.POST.get('breed_name')
        is_adopted = request.POST.get('is_adopted')
        dog_name = request.POST.get('dog_name')
        dog_color =request.POST.get('dog_color')
        dog_age = request.POST.get('dog_age')
        is_disable = request.POST.get('is_disable')
        disabilty = ""
        if is_disable == "1":
            disabilty = request.POST.get('disabilty')
        unique_identification = request.POST.get('unique_identification')
        is_adoption_ready = request.POST.get('is_adoption_ready')
        dog_image_path = request.POST.get('dog_image_path')
        breed_id = search_and_add_breed(breed_name)
        if breed_id != -1 :
            dog  = add_dog(breed_id=breed_id, is_adopted= is_adopted,dog_name= dog_name,dog_color= dog_color, dog_age= dog_age, is_disable= is_disable, disabilty=disabilty, unique_identification=unique_identification, is_adoption_ready=is_adoption_ready, dog_image_path=dog_image_path)
        if dog is not None:
            messages.success(request, 'Sucess: Dog Added')
            return redirect('dashboard')
        else:
            messages.error(request, 'Failure: Breed can not be added')
    return redirect('dashboard')

def report_dog(request):
    if request.method == 'POST':
        dog_name = ""
        breed_name = request.POST.get('breed_name')
        last_known_location =request.POST.get('last_known_location')
        category = request.POST.get('category')
        if category == "lost":
            is_adopted = 0
            dog_name = request.POST.get('dog_name')
        else:
            is_adopted = 1
        dog_color =request.POST.get('dog_color')
        dog_age = request.POST.get('dog_age')
        is_disable = request.POST.get('is_disable')
        disabilty = ""
        if is_disable == "1":
            disabilty = request.POST.get('disabilty')
        unique_identification = request.POST.get('unique_identification')
        is_adoption_ready = request.POST.get('is_adoption_ready')
        dog_image_path = request.POST.get('dog_image_path')

        user_name= request.POST.get('user_name')
        user_address= request.POST.get('user_address')
        user_contact= request.POST.get('user_contact')
        user_email= request.POST.get('user_contact')

        breed_id = search_and_add_breed(breed_name)
        dog_id  = add_dog(breed_id=breed_id, is_adopted= is_adopted,dog_name= dog_name,dog_color= dog_color, dog_age= dog_age, is_disable= is_disable, disabilty=disabilty, unique_identification=unique_identification, is_adoption_ready=is_adoption_ready, dog_image_path=dog_image_path)
        reporter = add_reporter_user(user_name,user_address,user_contact,user_email)

        if reporter is not None and breed_id != -1 and dog_id != -1:
            report = Reports.objects.create(dog_id=dog_id, breed_id=breed_id, last_known_location = last_known_location,reporter= reporter,category=category)
            if report is not None:
                messages.success(request, 'Sucess: Report Added')
                return redirect('dashboard')
            else:
                messages.error(request, 'Failure: Report can not be created')
        else:
            messages.error(request, 'Failure: Report can not be created')
    return redirect('dashboard')

def add_reporter_user(user_name,user_address,user_contact,user_email):
   
    user = User.objects.create(field_user_name=user_name,user_address=user_address,user_contact=user_contact,user_email=user_email)
    return user
def search_and_add_breed(breed_name):
    breed = Breed.objects.filter(breed_name=breed_name).values()
    if breed is not None:
        if len(breed) > 0:
            breed_id = breed[0]["breed_id"]
            return breed_id

    breed = Breed.objects.create(breed_name=breed_name, breed_article= "",breed_image_path= "/")
    if breed is not None:
        return breed.breed_id
    else:
        return -1
def add_dog(breed_id,is_adopted,dog_name, dog_color, dog_age, is_disable, disabilty, unique_identification, is_adoption_ready, dog_image_path):
    dog = Dogs.objects.create(breed_id=breed_id, is_adopted= is_adopted,dog_name= dog_name,dog_color= dog_color, dog_age= dog_age, is_disable= is_disable, disabilty=disabilty, unique_identification=unique_identification, is_adoption_ready=is_adoption_ready, dog_image_path=dog_image_path)
    if dog is not None:
            return dog.dog_id
    else:
            return -1

def add_event(request):
    event_location =request.POST.get('event_location')
    event_time = request.POST.get('event_time')
    event_duration = request.POST.get('event_duration')
    event_capacity = request.POST.get('event_capacity')
    event_description = request.POST.get('event_duration')
    
    event = Events.objects.create(event_location=event_location, event_duration=event_duration, event_time=event_time,event_capacity=event_capacity,event_description=event_description)

    if event is not None:
        messages.success(request, 'Sucess: Event Added')
    else:
        messages.error(request, 'Failure: Event can not be added')
       
    return redirect('dashboard')

def event_subscribe(request):
    pass
    return redirect('dashboard')

def adminHome(request):
    return render(request,'dashboard/index.html')
def add_breed_html(request):
    return render(request,'dashboard/add_breed.html')
def map(request):
    return render(request,'dashboard/map-google.html')
def add_dog_html(request):
    return render(request,'dashboard/add_dog.html')
def add_report_html(request):
    return render(request,'dashboard/add_report.html')
def add_event_html(request):
    return render(request,'dashboard/add_event.html')