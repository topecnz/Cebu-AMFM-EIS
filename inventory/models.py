from django.contrib.auth.models import UserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

class CustomUserManager(UserManager):
    def _create_user(self, username, password, acc_type):
        if not username:
            raise ValueError("You are not provided a valid username.")
        if not password:
            raise ValueError("You are not provided a valid password.")

        username = self.model.normalize_username(username)
        user = self.model(username=username, acc_type_id=acc_type)
        user.set_password(password)
        user.save()
        
        return user
    
    def create_user(self, username, password):
        return self._create_user(username, password, 3)
    
    def create_superuser(self, username, password):
        return self._create_user(username, password, 1)

class AccountType(models.Model):
    acc_type_id = models.AutoField(primary_key=True)
    acc_type_name = models.CharField(max_length=64)

    class Meta:
        managed = True
        db_table = 'account_type'


class ProductType(models.Model):
    prod_type_id = models.AutoField(primary_key=True)
    prod_type_name = models.CharField(max_length=1024)

    class Meta:
        managed = True
        db_table = 'product_type'


class ProductBrand(models.Model):
    prod_br_id = models.AutoField(primary_key=True)
    prod_br_name = models.CharField(max_length=1024)

    class Meta:
        managed = True
        db_table = 'product_brand'


class Employee(models.Model):
    emp_id = models.AutoField(primary_key=True)
    emp_fname = models.CharField(max_length=1024)
    emp_mname = models.CharField(max_length=1024, blank=True, null=True)
    emp_lname = models.CharField(max_length=1024)
    emp_birthdate = models.DateField(blank=True, null=True)
    emp_phone = models.CharField(max_length=12, blank=True, null=True)
    emp_email = models.CharField(max_length=255, blank=True, null=True, unique=True)
    emp_created_at = models.DateTimeField(default=timezone.now)
    emp_updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = True
        db_table = 'employee'


class Customer(models.Model):
    cus_id = models.AutoField(primary_key=True)
    cus_name = models.CharField(max_length=1024)
    cus_phone = models.CharField(max_length=12)
    cus_address = models.CharField(max_length=1024, blank=True, null=True)
    cus_city = models.CharField(max_length=1024, blank=True, null=True)
    cus_created_at = models.DateTimeField(default=timezone.now)
    cus_updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = True
        db_table = 'customer'


class Supplier(models.Model):
    sup_id = models.AutoField(primary_key=True)
    sup_name = models.CharField(max_length=1024)
    sup_phone = models.CharField(max_length=12, blank=True, null=True)
    sup_address = models.CharField(max_length=1024)
    sup_city = models.CharField(max_length=1024, blank=True, null=True)
    sup_status = models.CharField(max_length=32, default='Active')
    sup_created_at = models.DateTimeField(default=timezone.now)
    sup_updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = True
        db_table = 'supplier'

class Product(models.Model):
    prod_id = models.AutoField(primary_key=True)
    # prod_name = models.CharField(max_length=1024)
    prod_desc = models.CharField(max_length=1024, blank=True, null=True)
    prod_price = models.FloatField(blank=True, null=True)
    prod_remarks = models.CharField(max_length=1024, blank=True, null=True)
    prod_status = models.CharField(max_length=1024, default='Active')
    prod_created_at = models.DateTimeField(default=timezone.now)
    prod_updated_at = models.DateTimeField(default=timezone.now)
    prod_type = models.ForeignKey(ProductType, models.DO_NOTHING, blank=True, null=True)
    prod_br = models.ForeignKey(ProductBrand, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'product'


class Inventory(models.Model):
    in_id = models.AutoField(primary_key=True)
    in_qty = models.IntegerField(blank=True, null=True)
    in_status = models.CharField(max_length=13, default='Available', blank=True, null=True)
    in_created_at = models.DateTimeField(default=timezone.now)
    in_updated_at = models.DateTimeField(default=timezone.now)
    prod = models.OneToOneField(Product, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'inventory'

class PurchaseOrder(models.Model):
    po_id = models.AutoField(primary_key=True)
    po_date = models.DateTimeField(default=timezone.now)
    po_amount = models.FloatField(blank=True, null=True)
    po_del_name = models.CharField(max_length=1024)
    po_del_phone = models.CharField(max_length=1024)
    po_del_address = models.CharField(max_length=1024)
    po_del_city = models.CharField(max_length=1024, blank=True, null=True)
    po_status = models.CharField(default="Pending", max_length=32)
    po_qrcode = models.CharField(blank=True, null=True, max_length=1024)
    sup = models.ForeignKey(Supplier, models.DO_NOTHING)
    emp = models.ForeignKey(Employee, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'purchase_order'

class SupplierItem(models.Model):
    sup_itm_id = models.AutoField(primary_key=True)
    sup_itm_qty = models.IntegerField(blank=True, null=True)
    sup_itm_price = models.FloatField(blank=True, null=True)
    sup_itm_amount = models.FloatField(blank=True, null=True)
    sup_itm_status = models.CharField(max_length=9, default='Active')
    sup_itm_created_at = models.DateTimeField(default=timezone.now)
    sup_itm_updated_at = models.DateTimeField(default=timezone.now)
    prod = models.ForeignKey(Product, models.DO_NOTHING)
    po = models.ForeignKey(PurchaseOrder, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'supplier_item'


class OrderList(models.Model):
    ord_id = models.AutoField(primary_key=True)
    ord_price = models.FloatField(blank=True, null=True)
    ord_qty = models.IntegerField(blank=True, null=True)
    ord_amount = models.FloatField(blank=True, null=True)
    ord_status = models.CharField(max_length=16, default="Active")
    ord_created_at = models.DateTimeField(default=timezone.now)
    ord_updated_at = models.DateTimeField(default=timezone.now)
    prod = models.ForeignKey(Product, models.DO_NOTHING)
    inv = models.ForeignKey('Invoice', models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'order_list'

class InvoiceType(models.Model):
    inv_type_id = models.AutoField(primary_key=True)
    inv_type_name = models.CharField(max_length=32, blank=True, null=True)
    
    class Meta:
        managed = True
        db_table = 'invoice_type'

class Invoice(models.Model):
    inv_id = models.AutoField(primary_key=True)
    inv_date = models.DateTimeField(default=timezone.now)
    inv_amount = models.FloatField(blank=True, null=True)
    inv_type = models.ForeignKey(InvoiceType, models.DO_NOTHING, blank=True, null=True)
    inv_status = models.CharField(default="Unpaid", max_length=32)
    inv_qrcode = models.CharField(blank=True, null=True, max_length=1024)
    inv_term_date = models.DateTimeField(blank=True, null=True)
    inv_balance = models.FloatField(blank=True, null=True)
    inv_updated_at = models.DateTimeField(default=timezone.now)
    cus = models.ForeignKey(Customer, models.DO_NOTHING, blank=True, null=True)
    emp = models.ForeignKey(Employee, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'invoice'

class Account(AbstractBaseUser, PermissionsMixin):
    acc_id = models.AutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=32, verbose_name='Username')
    last_login = models.DateTimeField(blank=True, null=True)
    acc_is_active = models.BooleanField(default=True)
    acc_created_at = models.DateTimeField(default=timezone.localtime)
    acc_updated_at = models.DateTimeField(default=timezone.localtime)
    acc_type = models.ForeignKey(AccountType, models.DO_NOTHING, null=True, blank=True)
    emp = models.OneToOneField(Employee, models.DO_NOTHING, null=True, blank=True)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        managed = True
        db_table = 'account'

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def __str__(self):
        return self.username
    