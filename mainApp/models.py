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
    customer = models.CharField(max_length=400)
    customer_name = models.CharField(max_length=400)
    date = models.DateField()
    project = models.CharField(max_length=400)
    item = models.CharField(max_length=400)
    description = models.CharField(max_length=1000)
    qty = models.IntegerField(max_length=6)
    order_type = models.CharField(max_length=100)
    delivered_qty = models.IntegerField(max_length=6)
    rate = models.IntegerField(max_length=6)
    amount = models.IntegerField(max_length=6)
    amount_to_deliver = models.IntegerField(max_length=6)
    available = models.IntegerField(max_length=6)
    projected = models.IntegerField(max_length=6)
    item_delivery_date = models.DateField()
    delay_days = models.IntegerField(max_length=6)
    item_name = models.CharField(max_length=400)
    description_b = models.CharField(max_length=1000)
    item_group = models.CharField(max_length=400)
    warehouse = models.CharField(max_length=400)
    status = models.CharField(max_length=1000)
    remaining_days_delivery = models.IntegerField(max_length=6)
    payment_staus = models.CharField(max_length=200,choices=payment_status_options)
    total_processed_qty = models.IntegerField(max_length=10)
    partially_dispatched_qty = models.IntegerField(max_length=10)
    latest_partially_dispatched_qty = models.IntegerField(max_length=10)
    qty_in_engineering = models.IntegerField(max_length=10)
    qty_in_buffing = models.IntegerField(max_length=10)
    qty_in_provisionally_schedule = models.IntegerField(max_length=10)
    qty_in_plating = models.IntegerField(max_length=10)
    qty_in_4sbuffing = models.IntegerField(max_length=10)
    qty_in_laquer = models.IntegerField(max_length=10)
    qty_in_packaging = models.IntegerField(max_length=10)
    latest_packaging_date = models.DateField()
    total_packaged_qty = models.IntegerField(max_length=10)
    cumulated_invoice_qty = models.IntegerField(max_length=10)
    latest_invoice_date = models.DateField()
    remaining_qty = models.IntegerField(max_length=10)
    remarks = models.CharField(max_length=1000)
    

    



    


    