from django.shortcuts import render, redirect
from django.http import HttpRequest, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist, SuspiciousOperation
from .forms import *
from .models import Employee, AccountType, Account

def add_account(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect('/')
    
    if request.user.acc_type_id == 1:
        acc_type = AccountType.objects.all()

        obj = {
            'acc_type': acc_type
        }
        
        return render(request, 'main/add_account.html', obj)
    
    # Error code 403
    raise PermissionDenied()

@csrf_exempt
def check_username(request: HttpRequest):
    if request.user.is_authenticated:
        if request.user.acc_type_id == 1:
            if request.method == "POST":
                u = request.POST['username'].lower()
                User = get_user_model()
                user = User.objects.filter(username=u).first()
                
                is_found = False
                if user:
                    is_found = True
                
                obj = {
                    'found': is_found
                }
                return JsonResponse(obj)

    return redirect('/')

@csrf_exempt
def submit_account(request: HttpRequest):
    if request.user.is_authenticated:
        if request.user.acc_type_id == 1:
            if request.method == "POST":
                # fn = request.POST['fname']
                # ln = request.POST['lname']
                u = request.POST['username'].lower()
                p = request.POST['password']
                acc_type = request.POST['acc_type']
                
                # validate username (security)
                
                User = get_user_model()
                user = User.objects.filter(username=u).first()

                if user and len(p) < 8:
                    return JsonResponse({
                        'code': 204,
                        'message': 'error'
                    })

                reg = None
                
                if not user:
                    # emp = Employee.objects.create(emp_fname=fn, emp_lname=ln)
                    # emp.save()
                    reg = User.objects.create(username=u, password=make_password(p), acc_type_id=acc_type)
                    reg.save()
                
                
                obj = {
                    'code': 200 if reg else 204,
                    'message': 'Account is successfully added!' if reg else 'Error!',
                }
                return JsonResponse(obj)
                
    return redirect('/')

def all_accounts(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect('/')
    
    if request.user.acc_type_id == 1:
    
        if request.method == 'POST':
            pass
        
        Account = get_user_model() 
        accounts = Account.objects.select_related('acc_type')
        obj = {
            'result': accounts,
        }
        return render(request, 'main/accounts.html', obj)
    
    # Error code 403
    raise PermissionDenied()

def search_account(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        pass
    
    # Error code 403
    raise PermissionDenied()

def view_account(request: HttpRequest, id: int):
    if not request.user.is_authenticated:
        return redirect('/')
    
    if request.user.acc_type_id == 1:
        User = get_user_model()
        user = User.objects.filter(acc_id=id) # results in multiple query
        atype = AccountType.objects.all()
        
        if user:
            for u in user:
                user = u

            obj = {
                'userdata': user,
                'type': atype
            }
        
            return render(request, 'main/view_account.html', obj)

        return render(request, 'main/view_account.html', {
                'error': 'Account not found!'
            })
    
    if request.method == 'POST':
        pass
    
    # Error code 403
    raise PermissionDenied()

@csrf_exempt
def delete_account(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect('/')
    
    if request.user.acc_type_id == 1:
        if request.method == 'POST':
            id = request.POST['id']
            print(id)

            User = get_user_model()
            user = User.objects.filter(acc_id=id).first()
            
            if user:
                if user.acc_type_id == 1 == request.user.acc_type_id:
                    obj = {
                        'code': 204,
                        'message': "Error: You can't delete yourself",
                        'status': 'Warning',
                    }
                    return JsonResponse(obj)
                
                user.acc_is_active = False
                user.save()

            obj = {
                    'code': 200 if user else 204,
                    'message': 'Account is successfully deleted!' if user else 'Error: user not found',
                    'status': 'success' if user else 'Warning',
                }
            return JsonResponse(obj)

@csrf_exempt
def update_account(request: HttpRequest):
    if request.user.is_authenticated:
        if request.user.acc_type_id == 1: # Super Admin
            if request.method == "POST":
                id = request.POST['id']
                fn = request.POST['fname']
                ln = request.POST['lname']
                u = request.POST['username'].lower()
                p = request.POST['password']
                acc_type = request.POST['acc_type']

                acc = Account.objects.get(acc_id=id)
                emp, created = Employee.objects.get_or_create(emp_fname=fn, emp_lname=ln)
                emp.emp_fname = fn
                emp.emp_lname = ln
                emp.emp_updated_at = timezone.now()
                emp.save()
                acc.username = u
                acc.password = make_password(p)
                acc.acc_type_id = acc_type
                acc.emp_id = emp.emp_id
                acc.acc_type_id = int(acc_type)
                acc.emp_id = emp.emp_id
                acc.save()
                
                obj = {
                    'code': 200 if acc else 204,
                    'message': 'Account is successfully updated!' if acc else 'Error!',
                }
                return JsonResponse(obj)
            
    return redirect('/')

@csrf_exempt
def update_account_2(request: HttpRequest):
    if request.user.is_authenticated:
    #     if request.user.acc_type_id == 2: # Admin
        if request.method == "POST":
            fn = request.POST['fn']
            mn = request.POST['mn']
            ln = request.POST['ln']
            u = request.POST['u'].lower()
            p = request.POST['phone']
            email = request.POST['email']
            bd = request.POST['birthdate']
            
            User = get_user_model()
            user = User.objects.get(acc_id=request.user.acc_id)
            
            user.username = u
            user.acc_updated_at = timezone.now()
            user.save()
            
            emp = Employee.objects.get(emp_id=request.user.emp_id)
            emp.emp_fname = fn
            emp.emp_mname = mn
            emp.emp_lname = ln
            emp.emp_phone = p
            emp.emp_email = email
            emp.emp_birthdate = bd
            emp.emp_updated_at = timezone.now()
            emp.save()
                
            obj = {
                'code': 200 if user and emp else 204,
                'message': 'Account is successfully updated!' if user and emp else 'Error!',
            }
            return JsonResponse(obj)
            
        return render(request, 'main/account_settings.html')         
    
    return redirect('/') 

@csrf_exempt
def change_password_dropdown(request: HttpRequest):
    if request.user.is_authenticated:
        if request.method == "POST":
            p = request.POST['password']
            cp = request.POST['cpassword']
            op = request.POST['opassword']
            
            User = get_user_model()
            acc = User.objects.filter(acc_id=request.user.acc_id).first()
            
            is_pass_valid = acc.check_password(op)
            
            if p != cp:
                return JsonResponse({
                    'code': 204,
                    'message': 'Error: Password not matched'
                })
            
            if not is_pass_valid:
                return JsonResponse({
                    'code': 204,
                    'message': 'Error: Incorrect Password'
                })
                    
            acc.password = make_password(p)
            acc.acc_updated_at = timezone.now()
            acc.save()
            
            userlogin = authenticate(username=acc.username, password=p)
            login(request, userlogin)
            
            obj = {
                'code': 200,
                'message': 'Password is successfully updated',
            }
            return JsonResponse(obj)
        
        return render(request, 'main/change_password_dropdown.html')
    return redirect('/')

@csrf_exempt
def reset_password(request: HttpRequest):
    if request.user.is_authenticated:
        if request.method == "POST":
            id = request.POST['id']
            
            User = get_user_model()
            user = User.objects.filter(acc_id=id).first()
            
            if user:
                newpass = get_random_string(8)
                user.set_password(newpass)
                user.save()
            
            obj = {
                    'code': 200 if user else 204,
                    'message': f'Account password has ben reset' if user else 'Error: user not found!',
                    'new': f'New password for {user.username} is: {newpass}' if user else '',
                    'status': 'success' if user else 'warning',
                }
            return JsonResponse(obj)
        
    return redirect('/')