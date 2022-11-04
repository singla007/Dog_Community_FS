from django.http import HttpResponse
from django.shortcuts import render, redirect
# from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from dog_community_app.models import Admin, User
from django.contrib import messages

# Create your views here.
def login(request):
    # Write login logic
    print("okau")
    if request.method == "POST":
        # return redirect('/dashboard')
        admin_login_id = request.POST.get("login_id")
        password = request.POST.get("password")
        print(admin_login_id)
        print(password)
        print(Admin.objects.filter(admin_login_id = admin_login_id))
        return redirect('/')
        # admin_obj = Admin.objects.filter(admin_login_id = admin_login_id)
        # if admin_obj is not None:
        #     if admin_obj.admin_login_pass == password:
        #         print("login success!")
        #     else:
        #         print("fail")
        # if not user_obj.exists():
        #     messages.info(request, "Account not found")
        #     return HttpResponse("<h1>Account not found</h1>")
        # else:
        #     return HttpResponse("<h1>Account found</h1>")
    else:
        print("hello")
        return render(request, 'login.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def register(request):
    if request.method == "POST":
        login_id = request.POST['login_id']
        password = request.POST['password']
        repassword = request.POST['repassword']
        username = request.POST['username']
        user_address = request.POST['user_address']
        user_contact = request.POST['user_contact']
        user_email = request.POST['user_email']
        # print(User.objects.all().order_by('user_id').last().user_id)
        user_id = User.objects.all().order_by('user_id').last().user_id +1
        new_user = User.objects.create(user_id=user_id,field_user_name=username,user_address=user_address,user_contact=user_contact,user_email=user_email)
        new_user.save()
        new_admin = Admin(admin_id=user_id,admin_login_id=login_id,admin_login_pass=password)
        new_admin.save()
        print(User)
        
        return redirect('/')
    else:
        print("hello")
        return render(request, 'register.html')
