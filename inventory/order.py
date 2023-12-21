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
    order = OrderList.objects.select_related('inv','prod')
    obj = {
        'result' : order,
    }
    
    return render(request, 'main/orders.html', obj)

def add_order(request):
    products = Product.objects.all()
    
    if not request.user.is_authenticated:
        return redirect('/')
    
    if request.user.acc_type_id != 3:
        # Generate or retrieve the latest invoice ID here
        invoice_id = Invoice.objects.latest('id').id if Invoice.objects.exists() else 1
        
        return render(request, 'main/add_order.html', {'products': products, 'invoice_id': invoice_id})
    
    raise PermissionDenied()


def view_order(request: HttpRequest, id: int):
    if not request.user.is_authenticated:
        return redirect('/')
    
    order = OrderList.objects.filter(ord_id=id)


    if order:
        for u in order:
            order = u

        obj ={
            'order': order
        }
        return render(request, 'main/view_order.html', obj) 
    
    return render(request, 'main/view_order.html', {
            'error': 'Order not found!'
        })

@csrf_exempt
def submit_order(request):
    if request.user.is_authenticated:
        if request.user.acc_type_id != 3:
            if request.method == "POST":
                p = request.POST['price']
                q = request.POST['qty']
                i = request.POST['invoice_id']
                pro_id = request.POST['products']  # Assuming this is the ID of the product

                # Fetch the Invoice instance based on the provided ID
                invoice = Invoice.objects.get(pk=i)

                # Fetch the Product instance based on the provided ID
                product = Product.objects.get(pk=pro_id)

                # Create the OrderList instance with the fetched instances
                ord = OrderList.objects.create(ord_price=p, ord_qty=q, inv=invoice, prod=product)
                
                obj = {
                    'code': 200 if ord else 204,
                    'message': 'Order is successfully added!' if ord else 'Error!',
                }

                return JsonResponse(obj)
                
    return redirect('/')


@csrf_exempt
def update_order(request):
    if request.user.is_authenticated:
        if request.user.acc_type_id != 3:
            if request.method == "POST":
                id = request.POST['id']
                p = request.POST['price']
                q = request.POST['qty']
                i = request.POST['invoice_id']
                pro_id = request.POST['products']  # Assuming this is the ID of the product

                # Fetch the OrderList instance based on the provided ID
                ord = OrderList.objects.get(ord_id=id)

                # Fetch the Invoice instance based on the provided ID
                invoice = Invoice.objects.get(pk=i)

                # Fetch the Product instance based on the provided ID
                product = Product.objects.get(pk=pro_id)

                # Update the OrderList instance with fetched instances
                ord.ord_price = p
                ord.ord_qty = q
                ord.inv = invoice
                ord.prod = product
                ord.save()

                obj = {
                    'code': 200,
                    'message': 'Order is successfully updated!' if ord else 'Error!',
                }
                return JsonResponse(obj)

    return redirect('/')