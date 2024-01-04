from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .forms import *
from .models import Account

import datetime

def user_login(request: HttpRequest):    
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        message = None
        status = None
        if form.is_valid():
            u:str = form.cleaned_data['username']
            p = form.cleaned_data['password']
            user = authenticate(username=u.lower(), password=p)
            if user:
                login(request, user)
                if request.user.acc_is_active:
                    if request.GET:
                        rd = request.GET['next']
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
        
        if request.user.is_authenticated:
            return redirect('/')
        
        return render(request, 'main/login.html', obj)
    
    return render(request, "main/login.html")

@login_required(login_url='/login')
def home(request: HttpRequest):
    
    curr = datetime.datetime.now()
    
    if curr.hour <= 6 >= 12:
        greet = 'Good Morning'
    elif curr.hour < 18:
        greet = 'Good Afternoon'
    else:
        greet = 'Good Evening'
    
    # t = AccountType.objects.get(acc_type_id=request.user.acc_type_id)
    data = Account.objects.select_related('acc_type', 'emp').get(acc_id=request.user.acc_id)
    
    obj = {
        'user': data,
        'type': data.acc_type.acc_type_name,
        'greet': greet
    }
    return render(request, "main/index.html", obj)

def user_logout(request: HttpRequest):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/login')
