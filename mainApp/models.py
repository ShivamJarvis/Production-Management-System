from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import redirect
# Create your models here.


class UserData(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    permission = models.CharField(max_length=100)


payment_status_options = (
    ('Approved','Approved'),
    ('Not Approved','Not Approved'),
)
class Inventory(models.Model):
    item_code = models.CharField(max_length=200,null=True,blank=True)
    opening_qty = models.IntegerField(null=True,blank=True)
    added_qty = models.IntegerField(null=True,blank=True)
    issued_dispatched_qty = models.IntegerField(null=True,blank=True)
    reserve_qty = models.IntegerField(null=True,blank=True)
    balanced_qty = models.IntegerField(null=True,blank=True)
    def __str__(self):
        return self.item_code

class Order(models.Model):
    sales_order = models.CharField(max_length=400)
    customer_name = models.CharField(max_length=400)
    order_date = models.DateField()
    project = models.CharField(max_length=400,blank=True,null=True)
    item_code = models.CharField(max_length=400)
    description = models.CharField(max_length=1000)
    order_qty = models.IntegerField()
    order_type = models.CharField(max_length=100,blank=True,null=True)
    delivered_qty = models.IntegerField(blank=True,null=True,default=0)
    rate = models.IntegerField(blank=True,null=True)
    amount = models.IntegerField(blank=True,null=True)
    amount_to_deliver = models.IntegerField(blank=True,null=True)
    available = models.IntegerField(blank=True,null=True)
    projected = models.IntegerField(blank=True,null=True)
    item_delivery_date = models.DateField(blank=True,null=True)
    delay_days = models.IntegerField(blank=True,null=True)
    item_name = models.CharField(max_length=400,blank=True,null=True)
    description_b = models.CharField(max_length=1000,blank=True,null=True)
    item_group = models.CharField(max_length=400,blank=True,null=True)
    warehouse = models.CharField(max_length=400,blank=True,null=True)
    status = models.CharField(max_length=1000,blank=True,null=True)
    remaining_days_delivery = models.IntegerField(blank=True,null=True)
    payment_staus = models.CharField(max_length=200,choices=payment_status_options,blank=True,null=True)
    total_processed_qty = models.IntegerField(blank=True,null=True,default=0)
    partially_dispatched_qty = models.IntegerField(blank=True,null=True,default=0)
    latest_partially_dispatched_qty = models.IntegerField(blank=True,null=True,default=0)
    latest_partially_dispatched_date = models.DateField(blank=True,null=True)
    qty_in_engineering = models.IntegerField(blank=True,null=True,default=0)
    qty_in_buffing = models.IntegerField(blank=True,null=True,default=0)
    qty_in_provisionally_schedule = models.IntegerField(blank=True,null=True,default=0)
    qty_in_plating = models.IntegerField(blank=True,null=True,default=0)
    qty_in_4sbuffing = models.IntegerField(blank=True,null=True,default=0)
    qty_in_laquer = models.IntegerField(blank=True,null=True,default=0)
    qty_in_packaging = models.IntegerField(blank=True,null=True,default=0)
    latest_packaging_date = models.DateField(blank=True,null=True)
    total_packaged_qty = models.IntegerField(blank=True,null=True,default=0)
    cumulated_invoice_qty = models.IntegerField(blank=True,null=True,default=0)
    latest_invoice_date = models.DateField(blank=True,null=True)
    remaining_qty = models.IntegerField(blank=True,null=True,default=0)
    remarks = models.CharField(max_length=1000,blank=True,null=True)
    completed_date = models.DateField(null=True,blank=True)
    completed = models.BooleanField(default=False)
    for_dispatch = models.IntegerField(default=0)
    inventory = models.ForeignKey(Inventory,null=True,blank=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.sales_order

class StockRequirement(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='OrderDetails')
    item_code = models.CharField(max_length=200,null=True,blank=True)
    required_qty = models.IntegerField(null=True,blank=True)
    stock_category = models.CharField(max_length=500,null=True,blank=True)
    po_number = models.CharField(max_length=300,null=True,blank=True)
    supplier_name = models.CharField(max_length=500,null=True,blank=True)
    stock_inward_estimate_date = models.DateField(null=True,blank=True)
    latest_stock_inward_actual_date = models.DateField(null=True,blank=True)
    recieved_qty = models.IntegerField(null=True,blank=True)
    pending_qty = models.IntegerField(null=True,blank=True)
    color = models.CharField(max_length=20,null=True,blank=True)
    created_on = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    remaining_days = models.IntegerField(null=True,blank=True)
    def __str__(self):
        return self.order.customer_name


class Supplier(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=500, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    gst_no = models.CharField(max_length=200, null=True, blank=True)
    pan_no = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return self.name

class Job(models.Model):
    job_id = models.CharField(max_length=400)
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    finish_type = models.CharField(max_length=300,null=True,blank=True)
    department = models.CharField(max_length=300)
    qty = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    message = models.CharField(max_length=300,null=True,blank=True)
    status = models.BooleanField(default=True)
    def __str__(self):
        return self.job_id


class ProvisionalSchedule(models.Model):
    job = models.ForeignKey(Job,on_delete=models.CASCADE,related_name='job_data',null=True,blank=True)
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='order_data')
    stock = models.ForeignKey(StockRequirement,on_delete=models.CASCADE,related_name='stock_required',null=True,blank=True)
    provision_date = models.DateField()
    final_date = models.DateField(null=True,blank=True)
    qty = models.IntegerField()
    is_finalised = models.BooleanField(default=False)
    is_canceled = models.BooleanField(default=False)
    is_material_required = models.BooleanField(default=False)
    from_inventory = models.BooleanField(default=False)
    color = models.CharField(max_length=20,null=True,blank=True)
    def __str__(self):
        return str(self.id)+". "+self.order.sales_order


class Comment(models.Model):
    comment = models.CharField(max_length=1000)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_details")
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name="order_details")
    created_on = models.DateTimeField(auto_now_add=True)


class Transaction(models.Model):
    transaction_id = models.CharField(max_length=40)
    message = models.CharField(max_length=500)
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name="order_data_txn",null=True,blank=True)
    stock = models.ForeignKey(StockRequirement,on_delete=models.CASCADE,related_name="stock_data_txn",null=True,blank=True)
    job = models.ForeignKey(Job,on_delete=models.CASCADE,related_name="job_data_txn",null=True,blank=True)
    provision = models.ForeignKey(ProvisionalSchedule,on_delete=models.CASCADE,related_name="provision_data_txn",null=True,blank=True)
    inventory = models.ForeignKey(Inventory,on_delete=models.CASCADE,related_name="inventory_data_txn",null=True,blank=True)
    date = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="create_by_user",null=True,blank=True)
    

class Invoice(models.Model):
    invoice_id = models.CharField(max_length=200)
    invoice_date = models.DateField(null=True,blank=True)
    order = models.ForeignKey(Order,on_delete=models.CASCADE)

    def __str__(self):
        return self.order.sales_order