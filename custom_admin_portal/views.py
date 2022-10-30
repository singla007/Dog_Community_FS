from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

# Create your views here.
def admin_login(request):
    # Write login logic
    login_id = request.POST.get("login_id")
    password = request.POST.get("password")
    print(login_id)
    print(password)
    # user_obj = Admin.objects.filter(login_id = login_id)

    return render(request, 'login.html')
