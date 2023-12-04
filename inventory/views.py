from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import *

# Create your views here.

def user_login(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        u = request.POST['username']
        p = request.POST['password']
        form = UserLoginForm(request.POST)
        message = None
        status = None
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user:
                login(request, user)
                if request.user.acc_is_active:
                    if request.method == 'GET':
                        rd = request.GET['next']
                        if rd:
                            return redirect(rd)
                    return redirect('/')
                else:
                    message = 'Account Removed'
                    status = 'danger'
                    logout(request)
            
        obj = {
            'message': message if message else 'Invalid Username or Password',
            'status': status if status else 'warning'
        }
        
        return render(request, 'main/login.html', obj)
    
    return render(request, "main/login.html", {})

@login_required(login_url='/login')
def home(request: HttpRequest):
    obj = {
        'user': request.user
    }
    return render(request, "main/index.html", obj)

def user_logout(request: HttpRequest):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/login')
