from django.shortcuts import render, redirect
from django.http import HttpRequest, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist, SuspiciousOperation
from .forms import *
from .models import Employee, AccountType, Product, ProductBrand, ProductType, Inventory, Supplier

@login_required(login_url='/login')
def suppliers(request: HttpRequest):
    if request.user.acc_type_id != 3:
        supplier = Supplier.objects.all()
        obj = {
            'result': supplier,
        }
        return render(request, 'main/suppliers.html', obj)
    
    raise PermissionDenied()

def add_supplier(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect('/')
    
    if request.user.acc_type_id != 3:
        return render(request, 'main/add_supplier.html')
    
    raise PermissionDenied()

def view_supplier(request: HttpRequest, id: int):
    if not request.user.is_authenticated:
        return redirect('/')
        
    supplier = Supplier.objects.filter(sup_id=id) # results in multiple query
    
    if supplier:
        for u in supplier:
            supplier = u

        obj = {
            'supplier': supplier,
        }
    
        return render(request, 'main/view_supplier.html', obj)

    return render(request, 'main/view_supplier.html', {
            'error': 'Supplier not found!'
        })

@csrf_exempt
def submit_supplier(request: HttpRequest):
    if request.user.is_authenticated:
        if request.user.acc_type_id != 3:
            if request.method == "POST":
                sn = request.POST['name']
                phone = request.POST['phone']
                email = request.POST['email']
                
                sup = Supplier.objects.create(sup_name=sn, sup_phone=phone, sup_email=email, sup_status='Active')
                sup.save()
                
                obj = {
                    'code': 200 if sup else 204,
                    'message': 'Supplier is successfully added!' if sup else 'Error!',
                }
                return JsonResponse(obj)
                
    return redirect('/')

@csrf_exempt
def update_supplier(request: HttpRequest):
    if request.user.is_authenticated:
        if request.user.acc_type_id != 3:
            if request.method == "POST":
                id = request.POST['id']
                sn = request.POST['name']
                phone = request.POST['phone']
                email = request.POST['email']
                
                sup = Supplier.objects.get(sup_id=id)
                sup.sup_name = sn
                sup.sup_phone = phone
                sup.sup_email = email
                sup.save()
                
                obj = {
                    'code': 200 if sup else 204,
                    'message': 'Supplier is successfully updated!' if sup else 'Error!',
                }
                return JsonResponse(obj)
                
    return redirect('/')

@csrf_exempt  
def delete_supplier(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect('/')
    
    if request.user.acc_type_id != 3:
        if request.method == 'POST':
            id = request.POST['id']
            sup = Supplier.objects.filter(sup_id=id) # results in multiple query
            
            code = None
            message = None
            if sup:
                for u in sup:
                    sup = u
                    
                sup.sup_status = 'Removed'
                sup.save()
                
                code = 200
                message = 'Supplier is successfully deleted!'

            obj = {
                    'code': code if code else 204,
                    'message': message if message else 'Error!',
                    'status': 'success' if code else 'warning',
                }
            return JsonResponse(obj)
        
    raise redirect('/')