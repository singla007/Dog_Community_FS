from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from dog_community_app.models import Admin
from django.contrib import messages

# Create your views here.
def admin_login(request):
    # Write login logic
    admin_login_id = request.POST.get("login_id")
    password = request.POST.get("password")
    print(admin_login_id)
    print(password)
    user_obj = Admin.objects.filter(admin_login_id = admin_login_id)
    # if not user_obj.exists():
    #     messages.info(request, "Account not found")
    #     return HttpResponse("<h1>Account not found</h1>")
    # else:
    #     return HttpResponse("<h1>Account found</h1>")


    return render(request, 'login.html')

def dashboard(request):
    return render(request, 'dashboard.html')
