from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .database import Account
from .forms import *

# Create your views here.

def login(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        u = request.POST['username']
        p = request.POST['password']
        account = Account()
        
        data, code = account.login(u, p)
        account.mysql.mydb.close()
        
        if code == 200:
            form = UserLoginForm(request.POST)
            if form.is_valid():
                user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
                print(user)
                if user:
                    login(request, user)
                    rd = request.GET['next']
                    if rd:
                        return redirect(rd)
                    return redirect('/')
        elif code == 204:
            # error message
            # use dict to store data and pass it to render()
            return render(request, 'login.html', {
                'message': 'Invalid Username or Password'
            })
    
    return render(request, "login.html", {})

# Note: Only admins can add accounts
@login_required(login_url='/login')
def add_account(request):
    if request.method == 'POST':
        pass
    
    return render(request, "")

@login_required(login_url='/login')
def home(request):
    return render(request, "index.html")
