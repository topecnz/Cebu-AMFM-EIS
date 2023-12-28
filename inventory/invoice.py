from django.shortcuts import render, redirect
from django.http import HttpRequest, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist, SuspiciousOperation
from .forms import *
from .models import Employee, AccountType, Product, ProductBrand, ProductType, Inventory, Invoice, InvoiceType, Customer
from django.utils import timezone

@login_required(login_url = '/login')
def invoices(request: HttpRequest):
    invoice = Invoice.objects.select_related('inv_type')
    obj ={
        'result': invoice
    }
    return render(request, 'main/invoices.html', obj)

def create_invoice(request: HttpRequest):
    if not request.user.is_authenticated:
       
        return redirect('/')
    
    if request.user.acc_type_id != 3:

        inv_type = InvoiceType.objects.all()
        inventory = Inventory.objects.select_related('prod')

        obj = {
            'type': inv_type,
            'item': inventory
        }
        return render(request, 'main/create_invoice.html', obj)
    
    raise PermissionDenied()

@csrf_exempt
def submit_invoice(request: HttpRequest):
    if request.user.is_authenticated:
        if request.user.acc_type_id == 1:
            if request.method == "POST":
                it = request.POST['inv_type']
                pn = request.POST ['Genshin Toy', 'ggg', 'kazuha wafer card', 'huawei']
                pd = request.POST ['productDesc']
                p = request.POST ['priceLabel']
                q = request.POST ['qty']

                inv = Invoice.objects.create(inv_type = it, )





@csrf_exempt
def update_invoice(request: HttpRequest):
    if request.user.is_authenticated:
        if request.user.acc_type_id != 3:
            if request.method == "POST":
                id = request.POST['id']
                it = request.POST['inv_type']
                pn = request.POST ['Genshin Toy', 'ggg', 'kazuha wafer card', 'huawei']
                pd = request.POST ['productDesc']
                p = request.POST ['priceLabel']
                q = request.POST ['qty']

                inv = Invoice.objects.get(inv_id=id)
                
                
                obj = {
                    'code': 200 if inv else 204,
                    'message': 'invoice is successfully updated!' if inv else 'Error!',
                }
                return JsonResponse(obj)
                
    return redirect('/')










    

    


