from django.shortcuts import render, redirect
from django.http import HttpRequest, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist, SuspiciousOperation
from .forms import *
from .models import Customer, Employee, AccountType, Inventory

@login_required (login_url = '/login')
def customers(request: HttpRequest):
    customer = Customer.objects.all()
    obj = {
        'result': customer,
    }
    return render(request, 'main/customers.html', obj)

def add_customer(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect('/')
    
    if request.user.acc_type_id != 3:
        return render(request, 'main/add_customer.html')
    
    raise PermissionDenied()



@csrf_exempt
def submit_customer(request: HttpRequest):
    if request.user.is_authenticated:
        if request.user.acc_type_id == 1:
            if request.method == "POST":
                fn = request.POST['fname']
                mn = request.POST['mname']
                ln = request.POST['lname']
                phone = request.POST['phone']

                cus = Customer.objects.create(cus_fname=fn, cus_mname= mn, cus_lname=ln, cus_phone=phone)
                cus.save()

                obj = {
                    'code': 200 if cus else 204,
                    'message': 'Customer is successfully added!' if cus else 'Error!',
                }
                return JsonResponse(obj)
                
    return redirect('/')

def view_customer(request: HttpRequest, id: int):
    if not request.user.is_authenticated:
        return redirect('/')
    
    cus = Customer.objects.filter(cus_id=id)

    if cus:
        for u in cus:
            cus = u
        
        obj = {
            'customer': cus
        }

        return render(request, 'main/view_customer.html', obj)
    
    return render(request, 'main/view_customer.html', {
       'error': 'Customer not found!'
   })



@csrf_exempt
def update_customer(request: HttpRequest):
    if request.user.is_authenticated:
        if request.user.acc_type_id != 3:
            if request.method == "POST":
                id = request.POST['id']
                fn = request.POST['fname']
                ln = request.POST['lname']
                phone = request.POST['phone']

                cus = Customer.objects.get(cus_id=id)
                cus.cus_fname = fn
                cus.cus_lname = ln
                cus.cus_phone = phone
                cus.save()

                obj = {
                    'code': 200 if cus else 204,
                    'message': 'Customer is successfully updated!' if cus else 'Error!',

                }
                return JsonResponse(obj)
            
    return redirect('/')