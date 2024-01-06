from django.shortcuts import render, redirect
from django.http import HttpRequest, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist, SuspiciousOperation
from .forms import *
from .models import Employee, AccountType, Product, ProductBrand, ProductType, Inventory

@login_required(login_url='/login')
def inventory(request: HttpRequest):
    inventory = Inventory.objects.select_related('prod')
    obj = {
        'result': inventory,
    }
    return render(request, 'main/inventory.html', obj)

def add_inventory(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect('/')
    
    if request.user.acc_type_id != 3:
    
        inventory = Inventory.objects.all()
        product = Product.objects.all()
        
        # Excluding the existing inventory from product
        result = []
        for p in product:
            found = False
            for i in inventory:
                if i.prod_id == p.prod_id:
                    found = True
                    break
            if not found:
                result.append({
                    'id': p.prod_id,
                    'name': p.prod_desc
                })
        
        obj = {
            'product': result
        }
        return render(request, 'main/add_inventory.html', obj)
    
    raise PermissionDenied()

def view_inventory(request: HttpRequest, id: int):
    if not request.user.is_authenticated:
        return redirect('/')
        
    inventory = Inventory.objects.select_related('prod').filter(in_id=id) # results in multiple query
    
    if inventory:
        for u in inventory:
            inventory = u

        obj = {
            'inventory': inventory,
        }
    
        return render(request, 'main/view_inventory.html', obj)

    return render(request, 'main/view_inventory.html', {
            'error': 'Inventory not found!'
        })

@csrf_exempt
def submit_inventory(request: HttpRequest):
    if request.user.is_authenticated:
        if request.user.acc_type_id == 1:
            if request.method == "POST":
                p = request.POST['prod']
                q = request.POST['qty']
                
                inv = Inventory.objects.create(in_qty=q, in_status='Available', prod_id=p)
                inv.save()
                
                obj = {
                    'code': 200 if inv else 204,
                    'message': 'Inventory is successfully added!' if inv else 'Error!',
                }
                return JsonResponse(obj)
                
    return redirect('/')

# still not sure
@csrf_exempt  
def delete_inventory(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect('/')
    
    if request.user.acc_type_id != 3:
        if request.method == 'POST':
            id = request.POST['id']
            prod = Product.objects.filter(prod_id=id) # results in multiple query
            
            code = None
            message = None
            if prod:
                for u in prod:
                    prod = u
                    
                prod.prod_status = 'Removed'
                prod.save()
                
                code = 200
                message = 'Product is successfully deleted!'

            obj = {
                    'code': code if code else 204,
                    'message': message if message else 'Error!',
                    'status': 'success' if code else 'warning',
                }
            return JsonResponse(obj)
        
    raise redirect('/')

@csrf_exempt
def update_inventory(request: HttpRequest):
    if request.user.is_authenticated:
        if request.user.acc_type_id != 3:
            if request.method == "POST":
                p = request.POST['prod_id']
                i = request.POST['in_id']
                q = request.POST['qty']
                
                inv = Inventory.objects.get(in_id=i, prod_id=p)
                inv.in_qty = q
                inv.save()
                
                obj = {
                    'code': 200 if inv else 204,
                    'message': 'Inventory is successfully updated!' if inv else 'Error!',
                }
                return JsonResponse(obj)
                
    return redirect('/')