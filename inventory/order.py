from datetime import timezone
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist, SuspiciousOperation

from inventory import customer
from .forms import *
from .models import Customer, Employee, AccountType, Product, ProductBrand, ProductType, Inventory, Invoice, OrderList

@login_required(login_url = '/login')
def orders(request: HttpRequest):
    orders = OrderList.objects.all()
    obj = {
        'result' : orders,
    }
    
    return render(request, 'main/orders.html', obj)

def add_order(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect('/')
    
    if request.user.acc_type_id != 3:
     

     return render(request, 'main/add_order.html')
    
    raise PermissionDenied()

def view_order(request: HttpRequest, id: int):
    if not request.user.is_authenticated:
        return redirect('/')
    
    invoice = Invoice.objects.filter(inv_id=id)


    if invoice:
        for u in invoice:
            invoice = u

        obj ={
            'invoice': invoice
        }
        return render(request, 'main/view_order.html', obj) 
    
    return render(request, 'main/view_order.html', {
            'error': 'Invoice not found!'
        })

@csrf_exempt
def submit_order(request: HttpRequest):
    if request.user.is_authenticated:
        if request.user.acc_type_id != 3:
            if request.method == "POST":
                i = request.POST['invDateLabel']
                a = request.POST['amount']
                c =  request.POST['custid']
                e =  request.POST['empIdLabel']

                inv = Invoice.object.create(inv_date = i, inv_amount=a)
                inv.save()

                obj = {
                    'code': 200 if inv else 204,
                    'message': 'Product is successfully added!' if inv else 'Error!',
                }
                return JsonResponse(obj)
                
    return redirect('/')





