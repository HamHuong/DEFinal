from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm

from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Actioncustomerlist

# Create your views here.
def register_page(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request,'Account was created for ' + user)
            return redirect('login')

    context={'form':form}
    return render(request,'accounts/register.html',context) 

def login_page(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,'Username OR password is incorrect')

    context={}
    return render(request,'accounts/login.html',context)

def logout_user(request):
    logout(request)
    return redirect('login')

def home(request):
    return render(request,'accounts/home.html')

def customer(request):
    custom = Actioncustomerlist.objects.all()
    print(custom)
    return render(request,'accounts/customer.html',{'customer': custom})
