from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.http import HttpResponse
from student import models as student_models

# Create your views here.

def homepage_page(request):
    context = {}
    return render(request,'homepage.html',context)

def about_page(request):
    context = {}
    return render(request,'about.html',context)

def terms_page(request):
    context = {}
    return render(request,'terms.html',context)

def login_page(request):
    if request.user.is_authenticated:
        do_logout(request)

    context = {}
    if request.method == 'POST':
        if request.user.is_authenticated:
            return HttpResponse('You are already logged in')

        username = request.POST.get('username')
        password = request.POST.get('password')

        print("Username: ",username," password: ",password)
        user = authenticate(username=username,password=password)

        print("User is : ",user)
        if user is not None:
            if user.is_active:
                login(request,user)
                print("Login success")

                if user.is_superuser: # If admin, take to administrator dashboard
                    return redirect('administrator:dashboard_page')
                else:
                    return redirect('student:rules_page')
        else:
            print("It is none")
            context = {
                'error':'error'
            }
            
    return render(request,'login.html',context)

def register_page(request):
    test = None
    try:
        test = student_models.Test.objects.get(is_register_allowed=True)
        print('My test is ',test)
    except:
        pass
    context = {
        'test':test,
    }

    if request.method == 'POST':
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        print('username: ',username)
        print('fname: ',fname)
        print('lname: ',lname)
        print('email ',email)
        print('password: ',password)
        user = None
        customer = None
        
        try:
            # Create user account
            user = student_models.User.objects.create_user(username=username,first_name=fname,last_name=lname,email=email,password=password,is_active=True,is_staff=False,is_superuser=False)
            user.save()
            
            # Create custom user incase if future modifications
            customuser = student_models.CustomUser.objects.create(user=user)
            
            # Give permission to test
            test_permission = student_models.TestPermission.objects.create(test_id=test,user=customuser)
            return redirect('register_success_page')
        except:
            context = {
                'test':test,
                'messages':'invalid',
            }
    return render(request,'register.html',context)

def register_success_page(request):
    context = {}
    return render(request,'register_success.html',context)

# Functionalities
def do_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('login_page')