from django.shortcuts import render, redirect
from django.http import HttpRequest, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMessage
from django.utils import timezone
from .forms import *
from .models import Account, Employee
from eis import settings

import datetime
import time
import uuid
import json

def user_login(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect('/')
    
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
    if not request.user.emp_id:
        return render(request, 'main/information.html')
    
    curr = datetime.datetime.now()
    
    if curr.hour >= 6 < 12:
        greet = 'Good Morning'
    elif curr.hour > 12 <= 18:
        greet = 'Good Afternoon'
    else:
        greet = 'Good Evening'
        
    print(curr.hour, greet)
    
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
    if not request.user.is_authenticated:
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
                
                if True:
                    # request.session['r_token'] = str(token)
                    # request.session['r_user'] = user.acc_id
                    # request.session.modified = True
                    with open('./static/reset/user_token.json', 'r') as f:
                        data = json.load(f)
                        
                    # print(data)
                    
                    unix_expires = datetime.datetime.now() + datetime.timedelta(minutes=15)
                    
                    data['request'].append({
                        "token": str(token),
                        "acc_id": user.acc_id,
                        "expires": time.mktime(unix_expires.timetuple())
                    })
                    
                    with open('./static/reset/user_token.json', 'w') as fw:
                        json.dump(data, fw, indent=4) # no permission to network disk
                
            obj = {
                'success': True if emp and email else False,
                'status': 'success' if emp and email else 'warning',
                'message': 'We\'ve sent a reset password link into the associated email. Please check you inbox or spam folder.' if emp and email else 'Email not found',
                'reset': True
            }
            
            return render(request, 'main/reset_password.html', obj)
        
        return render(request, 'main/reset_password.html', { 'reset': True })
    
    return redirect('/')

def change_password(request: HttpRequest, token: str = None):
    if not request.user.is_authenticated:
        is_valid = False
        data_found = False
        
        with open('./static/reset/user_token.json', 'r') as f:
                data = json.load(f)
                
        for res in data['request']:
            if res['token'] == token:
                data = res
                data_found = True
                break
            
        # check if token is invalid
        if not data_found:
            obj = {
                    'reset': True,
                    'is_valid': is_valid,
                    'status': 'warning',
                    'success': False,
                    'message': 'Invalid token',
                    'is_token_expired': True
                }
                
            return render(request, 'main/change_password.html', obj)
        
        # if token expires
        if time.mktime(datetime.datetime.now().timetuple()) > data['expires']:
            obj = {
                    'reset': True,
                    'is_valid': is_valid,
                    'status': 'warning',
                    'success': False,
                    'message': 'Token has expired.',
                    'is_token_expired': True
                }
                
            return render(request, 'main/change_password.html', obj)
        
        is_valid = True
            
        if request.method == "POST":
            user = Account.objects.get(acc_id=data['acc_id'])
            
            if user:
                password = request.POST['pass']
                cpassword = request.POST['cpass']
                
                if password != cpassword:
                    obj = {
                        'reset': True,
                        'is_valid': is_valid,
                        'status': 'warning',
                        'success': False,
                        'message': 'Password did not matched!',
                        'is_token_expired': False
                    }
                    return render(request, 'main/change_password.html', obj)
                
                user.password = make_password(password)
                user.acc_updated_at = timezone.now()
                user.save()
            
            obj = {
                'reset': True,
                'is_valid': is_valid,
                'status': 'success' if user else 'warning',
                'success': True if user else False,
                'message': 'Password has been updated!\nYou can now login now!' if user else 'User not found'
            }
            
            
            return render(request, 'main/change_password.html', obj)

        return render(request, 'main/change_password.html', { 'reset': True, 'is_token_expired': False })
        
    return redirect('/')

@csrf_exempt
def check_email(request: HttpRequest):
    if request.user.is_authenticated:
        if request.method == "POST":
            u = request.POST['email'].lower()
            emp = Employee.objects.filter(emp_email=u).first()
            
            is_found = False
            if emp:
                is_found = True
            
            obj = {
                'found': is_found
            }
            return JsonResponse(obj)

    return redirect('/')

@csrf_exempt
def submit_info(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect('/')
    
    if request.method == "POST":
        pw = request.POST['pass']
        cpw = request.POST['cpass']
        fn = request.POST['fn']
        mn = request.POST['mn']
        ln = request.POST['ln']
        phone = request.POST['phone']
        email = request.POST['email'].lower()
        birthdate = request.POST['birthdate']
        
        User = get_user_model()
        user = User.objects.get(acc_id=request.user.acc_id)
        
        is_email = Employee.objects.filter(emp_email=email).first()
        
        if len(pw) < 8 or pw != cpw or is_email:
            message = ''
            if len(pw) < 8:
                message += 'Password must be 8 characters. <br/>' 
            elif pw != cpw:
                message += 'Password not matched. <br/>'
                
            if is_email:
                message += 'Email already existed'
                 
            return JsonResponse({
                'code': 204,
                'message': f'Error: {message}' 
            })
        
        user.password = make_password(pw)
            
        emp = Employee.objects.create(
            emp_fname = fn,
            emp_mname = mn,
            emp_lname = ln,
            emp_phone = phone,
            emp_email = email,
            emp_birthdate = birthdate    
        )
        emp.save()
        
        user.emp_id = emp.emp_id
        user.save()
        
        # reloging user
        userlogin = authenticate(username=user.username, password=pw)
        login(request, userlogin)
        
        obj = {
            'code': 200 if emp else 204,
            'message': 'Employee information is successfully added!' if emp else 'Error!',
        }
        
        return JsonResponse(obj)
    
    return redirect('/')