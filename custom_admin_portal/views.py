from django.http import HttpResponse
from django.shortcuts import render, redirect
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from dog_community_app.models import Breed,Dogs,Events,Reports
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
# Create your views here.
from .forms import  CreateUserForm



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
		return render(request, 'register.html', context)

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
		return render(request, 'login.html', context)

def admin_logout(request):
	logout(request)
	return render(request, 'logout.html')


def error_page(request):
    return render(request,'error.html')
    
@login_required(login_url='login')  
def dashboard(request):
    return render(request, 'dashboard.html')

def add_breed(request):
    if request.method == 'POST':
        breedname = request.POST.get('username')
        breedarticle =request.POST.get('password')
        breedimage = request.POST.get('breedimage')

        breed = Breed.objects.create(breedname=breedname, breedarticle= breedarticle,breedimage= breedimage)

        if breed is not None:
            messages.sucess(request, 'Sucess: Breed Added')
            return redirect('dashboard')
        else:
            messages.error(request, 'Failure: Breed can not be added')
    return render(request,'dashboard.html')

def register_dog(request):
    if request.method == 'POST':
        breed_id = request.POST.get('breed_id')
        is_adopted = request.POST.get('is_adopted')
        dog_name = request.POST.get('dog_name')
        dog_color =request.POST.get('dog_color')
        dog_age = request.POST.get('dog_age')
        is_disable = request.POST.get('is_disable')
        disabilty = request.POST.get('disabilty')
        unique_identification = request.POST.get('unique_identification')
        is_adoption_ready = request.POST.get('is_adoption_ready')
        dog_image_path = request.POST.get('dog_image')

        dog = Dogs.objects.create(breed_id=breed_id, is_adopted= is_adopted,dog_name= dog_name,dog_color= dog_color, dog_age= dog_age, is_disable= is_disable, disabilty=disabilty, unique_identification=unique_identification, is_adoption_ready=is_adoption_ready, dog_image_path=dog_image_path)

        if dog is not None:
            messages.sucess(request, 'Sucess: Dog Added')
            return redirect('dashboard')
        else:
            messages.error(request, 'Failure: Breed can not be added')
    return render(request,'dashboard.html')

def report_dog(request):
    if request.method == 'POST':
        dog_id = request.POST.get('dog_id')
        breed_id = request.POST.get('breed_id')
        last_known_loaction =request.POST.get('lastlocation')
        reporter = request.POST.get('reporter')
        category = request.POST.get('category')

        report = Reports.objects.create(dog_id=dog_id, breed_id=breed_id, last_known_loaction = last_known_loaction,reporter= reporter,category=category)

        if report is not None:
            messages.sucess(request, 'Sucess: Report Added')
            return redirect('dashboard')
        else:
            messages.error(request, 'Failure: Report can not be created')
    return render(request,'dashboard.html')

