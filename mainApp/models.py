from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserData(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    permission = models.CharField(max_length=100)


payment_status_options = (
    ('Approved','Approved'),
    ('Not Approved','Not Approved'),
)

class Order(models.Model):
    sales_order = models.CharField(max_length=400)
    customer_name = models.CharField(max_length=400)
    order_date = models.DateField()
    project = models.CharField(max_length=400,blank=True,null=True)
    item_code = models.CharField(max_length=400)
    description = models.CharField(max_length=1000)
    order_qty = models.IntegerField()
    order_type = models.CharField(max_length=100,blank=True,null=True)
    delivered_qty = models.IntegerField(blank=True,null=True)
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
    total_processed_qty = models.IntegerField(blank=True,null=True)
    partially_dispatched_qty = models.IntegerField(blank=True,null=True)
    latest_partially_dispatched_qty = models.IntegerField(blank=True,null=True)
    qty_in_engineering = models.IntegerField(blank=True,null=True)
    qty_in_buffing = models.IntegerField(blank=True,null=True)
    qty_in_provisionally_schedule = models.IntegerField(blank=True,null=True)
    qty_in_plating = models.IntegerField(blank=True,null=True)
    qty_in_4sbuffing = models.IntegerField(blank=True,null=True)
    qty_in_laquer = models.IntegerField(blank=True,null=True)
    qty_in_packaging = models.IntegerField(blank=True,null=True)
    latest_packaging_date = models.DateField(blank=True,null=True)
    total_packaged_qty = models.IntegerField(blank=True,null=True)
    cumulated_invoice_qty = models.IntegerField(blank=True,null=True)
    latest_invoice_date = models.DateField(blank=True,null=True)
    remaining_qty = models.IntegerField(blank=True,null=True)
    remarks = models.CharField(max_length=1000,blank=True,null=True)
    def __str__(self):
        return self.sales_order

class Inventory(models.Model):
    item_code = models.CharField(max_length=200,null=True,blank=True)
    opening_qty = models.IntegerField(null=True,blank=True)
    added_qty = models.IntegerField(null=True,blank=True)
    issued_dispatched_qty = models.IntegerField(null=True,blank=True)
    balanced_qty = models.IntegerField(null=True,blank=True)
    def __str__(self):
        return self.item_code

    



    


    