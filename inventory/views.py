from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.mail import EmailMessage
from django.utils import timezone
from .forms import *
from .models import Account, Employee
from eis import settings

import datetime
import uuid

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
    
def reset_password(request: HttpRequest):
    # if not request.user.is_authenticated:
    if request.method == "POST":
        emp = Employee.objects.filter(emp_email=request.POST['email']).first()
        
        if emp:
            user = Account.objects.select_related('emp').filter(emp_id=emp.emp_id).first()
            
            token = uuid.uuid4()
            from_email = settings.EMAIL_HOST_USER
            to_email = user.emp.emp_email
            url = request.build_absolute_uri(f'/changepass/{token}')
            
            email = EmailMessage(
                'Reset Password',
                f"Hi!,\n\n Here's the reset password link: {url}",
                from_email,
                [to_email]
            )
            
            email.send(fail_silently=False)
            
            if email:
                request.session['r_token'] = str(token)
                request.session['r_user'] = user.acc_id
                request.session.modified = True
            
        obj = {
            'success': True if emp and email else False,
            'status': 'success' if emp and email else 'warning',
            'message': 'We\'ve sent a reset password link into the associated email.' if emp and email else 'Email not found',
            'reset': True
        }
        
        return render(request, 'main/reset_password.html', obj)
    
    return render(request, 'main/reset_password.html', { 'reset': True })
    
    # return redirect('/')

def change_password(request: HttpRequest, token: str):
    # if not request.user.is_authenticated:
    is_valid = False
    if token == request.session.get('r_token'):
        is_valid = True
        
        if request.method == "POST":
            user = Account.objects.get(acc_id=request.session.get('r_user'))
            
            if user:
                password = request.POST['pass']
                cpassword = request.POST['cpass']
                
                if password != cpassword:
                    obj = {
                        'reset': True,
                        'is_valid': is_valid,
                        'status': 'warning',
                        'success': False,
                        'message': 'Password did not matched!'
                    }
                    return render(request, 'main/change_password.html', obj)
                
                user.password = make_password(password)
                user.acc_updated_at = timezone.now()
                user.save()
                
                del request.session['r_token']
                del request.session['r_user']
            
            obj = {
                'reset': True,
                'is_valid': is_valid,
                'status': 'success' if user else 'warning',
                'success': True if user else False,
                'message': 'Password has been updated!\nYou can now login now!' if user else 'User not found'
            }
            
            
            return render(request, 'main/change_password.html', obj)

        return render(request, 'main/change_password.html', { 'reset': True })
        
    # return redirect('/')