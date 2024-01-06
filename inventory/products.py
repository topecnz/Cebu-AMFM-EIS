from django.shortcuts import render, redirect
from django.http import HttpRequest, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist, SuspiciousOperation
from django.utils import timezone
from .forms import *
from .models import Employee, AccountType, Product, ProductBrand, ProductType, Inventory

@login_required(login_url='/login')
def products(request: HttpRequest):
    product = Product.objects.select_related('prod_type', 'prod_br').filter(prod_status='Active')
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
def check_product_name(request: HttpRequest):
    if request.user.is_authenticated:
        if request.user.acc_type_id == 1:
            if request.method == "POST":
                p = request.POST['prod']
                product = Product.objects.filter(prod_name=p, prod_status='Active')
                
                is_found = False
                
                for r in product:
                    if r.prod_name.lower() == p.lower():
                        is_found = True
                        break
                
                obj = {
                    'found': is_found
                }
                return JsonResponse(obj)

    return redirect('/')

@csrf_exempt
def submit_product(request: HttpRequest):
    if request.user.is_authenticated:
        if request.user.acc_type_id == 1:
            if request.method == "POST":
                # p = request.POST['prod']
                d = request.POST['desc']
                pr = float("{:.2f}".format(request.POST['price']))
                pt = request.POST['prod_type']
                pb = request.POST['prod_br']
                
                pro, created = Product.objects.get_or_create(prod_desc=d)
                pro.prod_price = pr
                pro.prod_status = 'Active'
                
                ptype, pt_created = ProductType.objects.get_or_create(prod_type_name=pt)
                pbr, pb_created = ProductBrand.objects.get_or_create(prod_br_name=pb)
                
                ptype.save()
                pbr.save()
                
                pro.prod_type_id = ptype.prod_type_id
                pro.prod_br_id = pbr.prod_br_id
                pro.prod_updated_at = timezone.now() if not created else pro.prod_updated_at
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
        for p in prod:
            prod = p

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
                prod.prod_updated_at = timezone.now()
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
                # p = request.POST['prod']
                d = request.POST['desc']
                pr = float(request.POST['price'])
                pt = request.POST['prod_type']
                pb = request.POST['prod_br']
                # s = request.POST['prod_status']
                
                pro = Product.objects.get(prod_id=id)
                # pro.prod_name = p
                pro.prod_desc = d
                pro.prod_price = pr
                ptype, pt_created = ProductType.objects.get_or_create(prod_type_name=pt)
                pbr, pb_created = ProductBrand.objects.get_or_create(prod_br_name=pb)
                
                ptype.save()
                pbr.save()
                
                pro.prod_type_id = ptype.prod_type_id
                pro.prod_br_id = pbr.prod_br_id
                pro.prod_updated_at = timezone.now()
                
                pro.save()
                
                obj = {
                    'code': 200 if pro else 204,
                    'message': 'Product is successfully updated!' if pro else 'Error!',
                }
                return JsonResponse(obj)
                
    return redirect('/')
