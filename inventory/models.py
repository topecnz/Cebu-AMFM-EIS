from django.db import models

# Create your models here.

class Account(models.Model):
    acc_id = models.AutoField(primary_key=True)
    acc_username = models.CharField(unique=True, max_length=32)
    acc_password = models.CharField(max_length=32)
    acc_type_id = models.IntegerField()
    emp = models.ForeignKey('Employee', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'account'


class AccountType(models.Model):
    acc_type_id = models.IntegerField(primary_key=True)
    acc_type_name = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'account_type'


class Customer(models.Model):
    cus_id = models.AutoField(primary_key=True)
    cus_fname = models.CharField(max_length=1024)
    cus_mname = models.CharField(max_length=1024, blank=True, null=True)
    cus_lname = models.CharField(max_length=1024)
    cus_phone = models.CharField(max_length=12)
    cus_created_at = models.DateTimeField()
    cus_updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'customer'


class Employee(models.Model):
    emp_id = models.AutoField(primary_key=True)
    emp_fname = models.CharField(max_length=1024)
    emp_mname = models.CharField(max_length=1024, blank=True, null=True)
    emp_lname = models.CharField(max_length=1024)
    emp_birthdate = models.DateField()
    emp_phone = models.CharField(max_length=12)
    emp_email = models.CharField(max_length=1024)
    emp_address = models.CharField(max_length=1024)
    emp_status = models.CharField(max_length=7, blank=True, null=True)
    emp_created_at = models.DateTimeField()
    emp_updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'employee'


class Product(models.Model):
    prod_id = models.AutoField(primary_key=True)
    prod_name = models.CharField(max_length=1024)
    prod_desc = models.CharField(max_length=1024, blank=True, null=True)
    prod_price = models.FloatField(blank=True, null=True)
    prod_created_at = models.DateTimeField()
    prod_updated_at = models.DateTimeField()
    prod_type = models.ForeignKey('ProductType', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'product'


class ProductBrand(models.Model):
    prod_br_id = models.IntegerField(primary_key=True)
    prod_br_name = models.CharField(max_length=1024)

    class Meta:
        managed = False
        db_table = 'product_brand'


class ProductType(models.Model):
    prod_type_id = models.IntegerField(primary_key=True)
    prod_type_name = models.CharField(max_length=1024)

    class Meta:
        managed = False
        db_table = 'product_type'


class Supplier(models.Model):
    sup_id = models.IntegerField(primary_key=True)
    sup_name = models.CharField(max_length=1024)
    sup_phone = models.CharField(max_length=12)
    sup_email = models.CharField(max_length=1024)
    sup_created_at = models.DateTimeField()
    sup_updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'supplier'


class SupplierItem(models.Model):
    sup_itm_id = models.IntegerField(primary_key=True)
    sup_itm_qty = models.IntegerField(blank=True, null=True)
    sup_itm_dr = models.CharField(max_length=1024)
    sup_itm_status = models.CharField(max_length=9, blank=True, null=True)
    sup_itm_created_at = models.DateTimeField()
    sup_itm_updated_at = models.DateTimeField()
    prod = models.ForeignKey(Product, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'supplier_item'


class Inventory(models.Model):
    in_id = models.IntegerField(primary_key=True)
    in_qty = models.IntegerField(blank=True, null=True)
    int_status = models.CharField(max_length=13, blank=True, null=True)
    in_created_at = models.DateTimeField()
    in_updated_at = models.DateTimeField()
    prod = models.ForeignKey(Product, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'inventory'


class OrderList(models.Model):
    ord_id = models.AutoField(primary_key=True)
    ord_price = models.FloatField(blank=True, null=True)
    ord_qty = models.IntegerField(blank=True, null=True)
    prod = models.ForeignKey(Product, models.DO_NOTHING)
    inv = models.ForeignKey('Invoice', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'order_list'


class Invoice(models.Model):
    inv_id = models.AutoField(primary_key=True)
    inv_date = models.DateTimeField()
    inv_amount = models.FloatField(blank=True, null=True)
    cus = models.ForeignKey(Customer, models.DO_NOTHING, blank=True, null=True)
    emp = models.ForeignKey(Employee, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'invoice'
