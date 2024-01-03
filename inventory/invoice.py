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
        inv = Invoice.objects.all()
        inventory = Inventory.objects.select_related('prod').all()

        obj = {
            'type': inv_type,
            'invoice': inv,
            'inventory': inventory 
            
        }
        return render(request, 'main/create_invoice.html', obj)
    
    raise PermissionDenied()




@csrf_exempt
def product_details(request: HttpRequest):
    if request.user.is_authenticated:
        if request.user.acc_type_id == 1:
            if request.method == "POST":
                selected_product_name = request.POST.get('selected_product')

                if selected_product_name:
                    inventory_items = Inventory.objects.filter(prod__prod_name=selected_product_name)

                    if inventory_items.exists():
                        inventory_item = inventory_items.first()
                        obj = {
                            'description': inventory_item.prod.prod_desc,
                            'price': str(inventory_item.prod.prod_price),
                            'stock': str(inventory_item.in_qty),
                    
                        }
                    return JsonResponse(obj)

                return redirect('/')
                    

def calculate_amount(request: HttpRequest):
    if request.user.is_authenticated:
        if request.user.acc_type_id == 1:
            if request.method == 'POST':
                data = request.POST  # Assuming the data is sent via POST request
        
        product_name = data.get('product_name')
        quantity = int(data.get('quantity', 0))

        product = Inventory.objects.filter(prod_name=product_name).first()

        if product is None:
            return JsonResponse({"error": "Product not found"}, status=404)
        
        price = product.prod_price
        amount = quantity * price

        return JsonResponse({amount})
    
     
             













@csrf_exempt
def submit_invoice(request: HttpRequest):
    if request.user.is_authenticated:
        if request.user.acc_type_id == 1:
            if request.method == "POST":
                it = request.POST.get('inv_type')
                pn = request.POST.get('product_name')
                pd = request.POST.get('productDesc')
                q = request.POST.get('qty')
                p = request.POST.get('productPrices')
                a = request.POST.get('amountLabelPlaceholder')
                s = request.POST.get('productStock')

               

                inv = Invoice.objects.filter(
                    inv_name_type=it,
                    prod_id=pn,
                    prod_desc=pd,
                    prod_price=p,
                    ord_qty=q,
                    inv_amount=a,
                    in_qty=s
                ).first()

                if not inv:
                    # Create a new Inventory object if it doesn't exist
                    inv = Invoice(
                        inv_name_type=it,
                        prod_id=pn,
                        prod_desc=pd,
                        prod_price=p,
                        ord_qty=q,
                        inv_amount=a,
                        in_qty=s
                    )
                    # Save the new Inventory object
                    inv.save()


                obj = {
                    'code': 200 if inv else 204,
                    'message': 'Invoice is successfully added!' if inv else 'Error!',
                }
                return JsonResponse(obj)
                
    return redirect('/')





@csrf_exempt
def update_invoice(request: HttpRequest):
    if request.user.is_authenticated:
        if request.user.acc_type_id != 3:
            if request.method == "POST":
                id = request.POST['id']
                it = request.POST['inv_type']
                pn = request.POST ['Epson']
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










    

    


