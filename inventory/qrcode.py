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
from .models import Employee, AccountType, Product, ProductBrand, ProductType, Inventory, Invoice, InvoiceType, OrderList, Customer, PurchaseOrder

import json
from datetime import timedelta, datetime

@login_required(login_url='/login')
def qrcode(request: HttpRequest):
    return render(request, 'main/qrcode_scanner.html')

@csrf_exempt
def scanner(request: HttpRequest):
    if request.user.is_authenticated:
        if request.method == "POST":
            uuid = request.POST['result']
            
            # check if uuid result belongs to invoice
            invoice = Invoice.objects.filter(inv_qrcode=uuid).first()
            
            if invoice:
                obj = {
                    'id': invoice.inv_id,
                    'data': 'invoice',
                    'code': 200
                }
                
                return JsonResponse(obj)
            
            # check if uuid result belongs to PO
            
            po = PurchaseOrder.objects.filter(po_qrcode=uuid).first()
            
            if po:
                obj = {
                    'id': po.po_id,
                    'data': 'po',
                    'code': 200
                }
                
                return JsonResponse(obj)
            
            # if none of them
            
            obj = {
                'code': 204
            }
            
            return JsonResponse(obj)
        
    return redirect('/')