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
from .models import Employee, AccountType, Product, ProductBrand, ProductType, Inventory, Invoice, InvoiceType, OrderList, Customer

import json
from datetime import timedelta, datetime

@login_required(login_url='/login')
def invoices(request: HttpRequest):
    invoice = Invoice.objects.select_related('inv_type')
    obj = {
        'result': invoice,
    }
    return render(request, 'main/invoices.html', obj)

def create_invoice(request:HttpRequest):
    if not request.user.is_authenticated:
        return redirect('/')
    
    inv_type = InvoiceType.objects.all()
    inventory = Inventory.objects.select_related('prod').filter(in_status='Available')
    
    obj = {
        'type': inv_type,
        'inventory': inventory
    }
    return render(request, 'main/create_invoice.html', obj)

@csrf_exempt
def check_product(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect('/')
    
    if request.method == "POST":
        id = request.POST["id"]
        
        inventory = Inventory.objects.select_related('prod').filter(prod_id = id)

        if inventory:
            for p in inventory:
                inventory = p
                
            obj = {
                'code': 200, 
                'price': inventory.prod.prod_price,
                'desc': inventory.prod.prod_desc,
                'qty': inventory.in_qty,
                'brand': inventory.prod.prod_br.prod_br_name
            }
            
            return JsonResponse(obj)
        
        return JsonResponse({ 'code': 204 })
    
@csrf_exempt
def submit_invoice(request: HttpRequest):
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
            
        # validate if customer information exist
        if (not request.POST['cus_name'] or not request.POST['phone'] or not request.POST['addr']) and int(request.POST['type']) == 2:
            return JsonResponse({
                'code': 204,
                'message': 'Error: Customer details incomplete!'
            })
        
        inventory = Inventory.objects.select_related('prod')
        invoice = Invoice.objects.create(inv_type_id=request.POST['type'], emp_id=request.user.emp_id)
        invoice.save()
        
        total = 0
        for r in j['result']:
            data = inventory.get(prod_id= r['id'])
            
            order = OrderList.objects.create(
                ord_price = data.prod.prod_price,
                ord_qty = r['qty'],
                ord_amount= "{:.2f}".format(float(data.prod.prod_price) * float(r['qty'])),
                inv_id = invoice.inv_id,
                prod_id = data.prod.prod_id
            )
            order.save()
            
            # Qty deduction
            data.in_qty = data.in_qty - int(r['qty']) if data.in_qty > 0 else 0
            data.in_status = 'Available' if data.in_qty else 'Out of Stock'
            data.save()
            
            total += float(data.prod.prod_price) * float(r['qty'])
            
        invoice.inv_amount = "{:.2f}".format(total)
        invoice.inv_balance = 0 if invoice.inv_type == 1 else "{:.2f}".format(total)
        invoice.inv_status = 'Paid' if invoice.inv_type.inv_type_id == 1 else 'Unpaid'
        
        # default as boolean if customer is excluded (for walk-in)
        customer = True

        # Save customer details if project-based is selected with 30 days term
        if invoice.inv_type.inv_type_id == 2 and request.POST['cus_name'] and request.POST['phone'] and request.POST['addr']:
            customer = Customer.objects.create(cus_name=request.POST['cus_name'], cus_phone=request.POST['phone'], cus_address = request.POST['addr'])
            customer.save()
            invoice.inv_term_date = timezone.now() + timezone.timedelta(days=30)
            invoice.cus_id = customer.cus_id

        invoice.save()
            
        obj = {
            'code': 200 if invoice and customer else 204,
            'message': 'Invoice is successfuly created!' if invoice and customer else 'Error',
            'id': invoice.inv_id if invoice and customer else ''
        }
            
        return JsonResponse(obj)

    return redirect('/')

def view_invoice(request: HttpRequest, id: int):
    if not request.user.is_authenticated:
        return redirect('/')
    
    invoice = Invoice.objects.select_related('emp', 'cus', 'inv_type').filter(inv_id = id)
    
    if invoice:
        for i in invoice:
            invoice = i
        
        inventory = Inventory.objects.select_related('prod').filter(in_status='Available')
        order = OrderList.objects.select_related('prod').filter(inv_id = id, ord_status='Active')
    
        if invoice.inv_status != 'Removed':
            obj = {
                'invoice': invoice,
                'inventory': inventory,
                'order': order
            }
            
            return render(request, 'main/view_invoice.html', obj)

    return render(request, 'main/view_invoice.html', {
            'error': 'Invoice not found!'
        })

def print_invoice(request: HttpRequest, id: int):
    if not request.user.is_authenticated:
        return redirect('/')
    
    invoice = Invoice.objects.select_related('emp', 'cus', 'inv_type').filter(inv_id = id)

    if invoice:
        for i in invoice:
            invoice = i
        
        order = OrderList.objects.select_related('prod').filter(inv_id = id)
        if invoice.inv_status != 'Removed':
            obj = {
                'invoice': invoice,
                'order': order
            }
            
            return render(request, 'print/invoice.html', obj)
        else:
            return render(request, 'main/view_invoice.html', {
                'error': 'Invoice not found!'
            })

    return redirect('/')

@csrf_exempt
def update_invoice(request: HttpRequest):
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
            
        invoice = Invoice.objects.select_related('inv_type').get(inv_id=request.POST['inv_id'])
            
        # validate if customer information exist
        if (not request.POST['cus_name'] or not request.POST['phone'] or not request.POST['addr']) and invoice.inv_type.inv_type_id == 2:
            return JsonResponse({
                'code': 204,
                'message': 'Error: Customer details incomplete!'
            })
        
        inventory = Inventory.objects.select_related('prod')
        # old_order = OrderList.objects.get(inv_id=invoice.inv_id)
        total = 0
        for r in j['result']:
            data = inventory.get(prod_id= r['id'])
            
            order, created = OrderList.objects.get_or_create(
                inv_id = invoice.inv_id,
                prod_id = data.prod.prod_id
            )
            
            order.ord_status = 'Removed' if r['remove'] else 'Active'
            
            if not r['remove']:
                old_qty = 0 if created else order.ord_qty
                price = order.ord_price if not created else data.prod.prod_price
                order.ord_price = order.ord_price if not created else data.prod.prod_price
                order.ord_qty = r['qty']
                order.ord_amount = float("{:.2f}".format(price * float(r['qty'])),)
                order.save()
                
                if created:
                    data.in_qty = data.in_qty - int(r['qty']) if data.in_qty > 0 else 0
                else:
                    data.in_qty = data.in_qty + (old_qty - int(r['qty'])) if old_qty < int(r['qty']) else data.in_qty - (int(r['qty']) - old_qty)

                total += float(price * float(r['qty']))
            else:
                order.ord_status = 'Removed'
                order.ord_qty = 0
                data.in_qty += int(r['qty'])
                order.save()
                
            data.in_status = 'Available' if data.in_qty else 'Out of Stock'
            data.save()
            
        
        invoice.inv_amount = "{:.2f}".format(total)
        invoice.inv_status = request.POST['inv_status']
        
        # default as boolean if customer is excluded (for walk-in)
        customer = True

        # Save customer details if project-based is selected with 30 days term
        if invoice.inv_type.inv_type_id == 2 and request.POST['cus_name'] and request.POST['phone'] and request.POST['addr']:
            customer = Customer.objects.get(cus_id=request.POST['cus_id'])
            customer.cus_name=request.POST['cus_name']
            customer.cus_phone=request.POST['phone']
            customer.cus_address = request.POST['addr']
            customer.save()

        invoice.save()
            
        obj = {
            'code': 200 if invoice and customer else 204,
            'message': 'Invoice is successfuly updated!' if invoice and customer else 'Error',
            'id': invoice.inv_id if invoice and customer else ''
        }
            
        return JsonResponse(obj)
    
@csrf_exempt
def delete_invoice(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect('/')
    
    if request.user.acc_type_id != 3:
        if request.method == 'POST':
            id = request.POST['id']
            inv = Invoice.objects.filter(inv_id=id) # results in multiple query
            
            code = None
            message = None
            if inv:
                for u in inv:
                    inv = u
                    
                inv.inv_status = 'Deleted'
                inv.save()
                
                code = 200
                message = 'Invoice is successfully deleted!'
                
                # Return item to inventory if cancelled or deleted
                order = OrderList.objects.get(inv_id=inv.inv_id)
                inventory = Inventory.objects.select_related('prod').all()
                
                for ord in order:
                    data = inventory.get(prod_id= ord.prod_id)
                    
                    data.in_qty += ord.ord_qty
                    data.in_status = 'Available'
                    data.save()
                    

            obj = {
                    'code': code if code else 204,
                    'message': message if message else 'Error!',
                    'status': 'success' if code else 'warning',
                }
            return JsonResponse(obj)
        
    raise redirect('/')

@csrf_exempt
def cancel_invoice(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect('/')
    
    if request.user.acc_type_id != 3:
        if request.method == 'POST':
            id = request.POST['id']
            inv = Invoice.objects.filter(inv_id=id) # results in multiple query
            
            code = None
            message = None
            if inv:
                for u in inv:
                    inv = u
                    
                inv.inv_status = 'Cancelled'
                inv.save()
                
                code = 200
                message = 'Invoice is successfully cancelled!'
                
                # Return item to inventory if cancelled or deleted
                order = OrderList.objects.filter(inv_id=inv.inv_id)
                inventory = Inventory.objects.select_related('prod').all()
                
                for ord in order:
                    data = inventory.get(prod_id= ord.prod.prod_id)
                    
                    data.in_qty += ord.ord_qty
                    data.in_status = 'Available'
                    data.save()
                    

            obj = {
                    'code': code if code else 204,
                    'message': message if message else 'Error!',
                    'status': 'success' if code else 'warning',
                }
            return JsonResponse(obj)
        
    raise redirect('/')