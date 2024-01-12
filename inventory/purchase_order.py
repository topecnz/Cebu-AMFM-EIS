from django.shortcuts import render, redirect
from django.http import HttpRequest, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist, SuspiciousOperation
from .forms import *
from .models import Employee, AccountType, Product, ProductBrand, ProductType, Inventory, Invoice, InvoiceType, OrderList, Customer, Supplier, SupplierItem, PurchaseOrder

import json
import qrcode

@login_required(login_url='/login')
def orders(request: HttpRequest):
    if request.user.acc_type_id != 3:    
        po = PurchaseOrder.objects.select_related('emp', 'sup')
        obj = {
            'result': po,
        }
        return render(request, 'main/orders.html', obj)
    
    raise PermissionDenied()

def create_po(request:HttpRequest):
    if not request.user.is_authenticated:
        return redirect('/')
    
    if request.user.acc_type_id != 3:
        supplier = Supplier.objects.filter(sup_status='Active')
        prod = Product.objects.select_related('prod_type', 'prod_br').filter(prod_status='Active')
        
        obj = {
            'product': prod,
            'supplier': supplier
        }
        return render(request, 'main/create_po.html', obj)
    
    raise PermissionDenied()

@csrf_exempt
def check_product(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect('/')
    
    if request.method == "POST":
        id = request.POST["id"]
        
        product = Product.objects.filter(prod_id = id)

        if product:
            for p in product:
                product = p
                
            obj = {
                'code': 200, 
                'price': product.prod_price,
                'desc': product.prod_desc,
                'brand': product.prod_br.prod_br_name
            }
            
            return JsonResponse(obj)
        
        return JsonResponse({ 'code': 204 })
    
@csrf_exempt
def check_supplier(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect('/')
    
    if request.method == "POST":
        id = request.POST["id"]
        
        supplier = Supplier.objects.filter(sup_id = id)

        if supplier:
            for p in supplier:
                supplier = p
                
            obj = {
                'code': 200, 
                'name': supplier.sup_name,
                'phone': supplier.sup_phone,
                'address': supplier.sup_address,
            }
            
            return JsonResponse(obj)
        
        return JsonResponse({ 'code': 204 })
    
@csrf_exempt
def submit_order(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect('/')
    
    if request.method == "POST":
        data = request.POST['data']
        
        j = json.loads(data)
        
        if not j:
            return JsonResponse({
                'code': 204,
                'message': 'Error'
            })
        
        product = Product.objects.select_related('prod_type', 'prod_br')
        po = PurchaseOrder.objects.create(
            po_del_name = request.POST['name'],
            po_del_phone = request.POST['phone'],
            po_del_address = request.POST['addr'],
            sup_id=request.POST['sup_id'],
            emp_id=request.user.emp_id)
        po.save()
        
        total = 0
        for r in j['result']:
            data = product.get(prod_id= r['id'])
            
            sup_item = SupplierItem.objects.create(
                sup_itm_price = "{:.2f}".format(float(r['price'])),
                sup_itm_qty = r['qty'],
                sup_itm_amount= "{:.2f}".format(float(r['price']) * float(r['qty'])),
                po_id = po.po_id,
                prod_id = data.prod_id
            )
            sup_item.save()
            
            total += float(r['price']) * float(r['qty'])
            
        po.po_amount = "{:.2f}".format(total)

        po.save()
        
        # generate qrcode
        img = qrcode.make(f"CEBU AMFM ELECTRONICS CENTER DATA=po-{po.po_id}")
        img.save(f'./static/assets/qrcode/po-{po.po_id}.png')
            
        obj = {
            'code': 200 if po else 204,
            'message': 'Puchase Order is successfuly created!' if po else 'Error',
            'id': po.po_id if po else ''
        }
            
        return JsonResponse(obj)

    return redirect('/')

def view_po(request: HttpRequest, id: int):
    if not request.user.is_authenticated:
        return redirect('/')
    
    po = PurchaseOrder.objects.select_related('emp', 'sup').filter(po_id = id)
    
    if po:
        for p in po:
            po = p
        
        prod = Product.objects.filter(prod_status='Active')
        sup = Supplier.objects.all()            
        sup_itm = SupplierItem.objects.select_related('prod').filter(po_id = id, sup_itm_status='Active')
                
        if po.po_status != 'Removed':
            obj = {
                'po': po,
                'supplier': sup,
                'sup_itm': sup_itm,
                'prod': prod
            }
        
            return render(request, 'main/view_po.html', obj)

    return render(request, 'main/view_po.html', {
            'error': 'Purchase Order not found!'
        })

def print_po(request: HttpRequest, id: int):
    if not request.user.is_authenticated:
        return redirect('/')
    
    po = PurchaseOrder.objects.select_related('emp', 'sup').filter(po_id = id)

    if po:
        for p in po:
            po = p

        sup_itm = SupplierItem.objects.select_related('prod').filter(po_id = id, sup_itm_status='Active')
        
        if po.po_status != 'Removed':
            obj = {
                'po': po,
                'sup_itm': sup_itm
            }
            
            return render(request, 'print/po.html', obj)
        else:
            return render(request, 'main/view_po.html', {
                'error': 'Purchase Order not found!'
            })

    return redirect('/')

@csrf_exempt
def update_po(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect('/')
    
    if request.method == "POST":
        data = request.POST['data']
        
        j = json.loads(data)
        
        if not j:
            return JsonResponse({
                'code': 204,
                'message': 'Error'
            })
            
        po = PurchaseOrder.objects.get(po_id=request.POST['id'])
        inventory = Inventory.objects.select_related('prod')
        
        if po.po_status == 'Pending':
            po.po_status = 'Approved'
        elif po.po_status == 'Approved':
            po.po_status = 'Ordered'
        elif po.po_status == 'Ordered':
            po.po_status = 'In-Transit'
        elif po.po_status == 'In-Transit':
            po.po_status = 'Delivered'
        
        total = 0
        for r in j['result']:
            sup_itm, created = SupplierItem.objects.get_or_create(
                po_id = po.po_id,
                prod_id = r['id']
            )
            
            sup_itm.sup_itm_status = 'Removed' if r['remove'] else 'Active'
            
            if not r['remove']:
                sup_itm.sup_itm_qty = r['qty']
                sup_itm.sup_itm_price = float("{:.2f}".format(float(r['price'])))
                sup_itm.sup_itm_amount = float("{:.2f}".format(float(r['price']) * float(r['qty'])),)
                total += float(float(r['price']) * float(r['qty']))
            else:
                sup_itm.sup_itm_status = 'Removed'

            sup_itm.save()
            
            if po.po_status == 'Approved':
                sup_itm.prod.prod_price = float("{:.2f}".format(float(r['price'])))
                sup_itm.prod.save()
        
            if po.po_status == 'Delivered':
                data, in_created = inventory.get_or_create(prod_id = sup_itm.prod.prod_id)
                data.in_qty = data.in_qty if data.in_qty else 0
                data.in_qty = data.in_qty + int(r['qty']) if not in_created else int(r['qty'])
                data.in_status = 'Available' if data.in_qty else 'Out of Stock'
                data.save()
        
        po.po_amount = "{:.2f}".format(total)        

        po.save()
            
        obj = {
            'code': 200 if po else 204,
            'message': 'Purchase Order is successfuly updated!' if po else 'Error',
            'id': po.po_id if po else ''
        }
            
        return JsonResponse(obj)
    
@csrf_exempt
def delete_po(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect('/')
    
    if request.user.acc_type_id != 3:
        if request.method == 'POST':
            id = request.POST['id']
            po = PurchaseOrder.objects.filter(po_id=id) # results in multiple query
            
            code = None
            message = None
            if po:
                for u in po:
                    po = u
                    
                po.po_status = 'Cancelled'
                po.save()
                
                code = 200
                message = 'Purchase order is successfully deleted!'

            obj = {
                    'code': code if code else 204,
                    'message': message if message else 'Error!',
                    'status': 'success' if code else 'warning',
                }
            return JsonResponse(obj)
        
    raise redirect('/')