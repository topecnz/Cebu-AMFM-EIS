from django.urls import path 
from . import views, accounts, products, inventory, supplier

urlpatterns = [
    path('', views.home, name="Home"),
    path('login/', views.user_login, name="Login"),
    path('logout/', views.user_logout, name="Logout"),    
    path('accounts/', accounts.all_accounts, name="Account Management"),
    path('accounts/add/', accounts.add_account, name="Add Account"),
    path('accounts/check_username/', accounts.check_username, name="Check Username"),
    path('accounts/submit_account/', accounts.submit_account, name="Submit Account"),
    path('accounts/<int:id>/', accounts.view_account, name="View Account"),
    path('products/', products.products, name="Products"),
    path('products/add/', products.add_product, name="Add Product"),
    path('products/submit_product/', products.submit_product, name="Submit Product"),
    path('products/<int:id>/', products.view_product, name="View Product"),
    path('products/update_product/', products.update_product, name="Update Product"),
    path('products/delete_product/', products.delete_product, name="Delete Product"),
    path('inventory/', inventory.inventory, name="Inventory"),
    path('inventory/add', inventory.add_inventory, name="Add Inventory"),
    path('inventory/submit_inventory', inventory.submit_inventory, name="Submit Inventory"),
    path('inventory/update_product/', inventory.update_inventory, name="Update Inventory"),
    path('inventory/<int:id>/', inventory.view_inventory, name="View Inventory"),
    path('suppliers/', supplier.suppliers, name="Suppliers"),
    path('suppliers/add', supplier.add_supplier, name="Add Supplier"),
    path('suppliers/submit_supplier/', supplier.submit_supplier, name="Submit Supplier"),
    path('suppliers/<int:id>/', supplier.view_supplier, name="View Supplier"),
    path('suppliers/update_supplier/', supplier.update_supplier, name="Update Supplier"),
    path('suppliers/delete_supplier/', supplier.delete_supplier, name="Delete Supplier"),
]
