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
def products(request: HttpRequest):
    product = Product.objects.select_related('prod_type', 'prod_br')
    obj = {
        'result': product,
    }
    return render(request, 'main/products.html', obj)

def add_product(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect('/')
    
    if request.user.acc_type_id != 3:
        prod_type = ProductType.objects.all()
        prod_br = ProductBrand.objects.all()
        obj = {
            'type': prod_type,
            'brand': prod_br
        }
        return render(request, 'main/add_product.html', obj)
    
    raise PermissionDenied()

@csrf_exempt
def submit_product(request: HttpRequest):
    if request.user.is_authenticated:
        if request.user.acc_type_id == 1:
            if request.method == "POST":
                p = request.POST['prod']
                d = request.POST['desc']
                pr = request.POST['price']
                pt = request.POST['prod_type']
                pb = request.POST['prod_br']
                
                pro = Product.objects.create(prod_name=p, prod_desc=d, prod_price=pr, prod_type_id=pt, prod_br_id=pb)
                pro.save()
                
                obj = {
                    'code': 200 if pro else 204,
                    'message': 'Product is successfully added!' if pro else 'Error!',
                }
                return JsonResponse(obj)
                
    return redirect('/')

def view_product(request: HttpRequest, id: int):
    if not request.user.is_authenticated:
        return redirect('/')
        
    prod = Product.objects.filter(prod_id=id) # results in multiple query
    prod_type = ProductType.objects.all()
    prod_br = ProductBrand.objects.all()
    
    if prod:
        for u in prod:
            prod = u

        obj = {
            'product': prod,
            'type': prod_type,
            'brand': prod_br
        }
    
        return render(request, 'main/view_product.html', obj)

    return render(request, 'main/view_product.html', {
            'error': 'Product not found!'
        })

@csrf_exempt  
def delete_product(request: HttpRequest):
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
                inv = Inventory.objects.get(prod_id=prod.prod_id)
                inv.in_status = 'Removed'
                prod.save()
                inv.save()
                
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
def update_product(request: HttpRequest):
    if request.user.is_authenticated:
        if request.user.acc_type_id != 3:
            if request.method == "POST":
                id = request.POST['id']
                p = request.POST['prod']
                d = request.POST['desc']
                pr = request.POST['price']
                pt = request.POST['prod_type']
                pb = request.POST['prod_br']
                s = request.POST['prod_status']
                
                pro = Product.objects.get(prod_id=id)
                pro.prod_name = p
                pro.prod_desc = d
                pro.prod_price = pr
                pro.prod_type_id = pt
                pro.prod_br_id = pb
                pro.prod_status = s
                pro.save()
                
                obj = {
                    'code': 200 if pro else 204,
                    'message': 'Product is successfully updated!' if pro else 'Error!',
                }
                return JsonResponse(obj)
                
    return redirect('/')