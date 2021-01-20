from django.contrib import admin
from mainApp.models import UserData,Order,Inventory
# Register your models here.

admin.site.register(UserData)
admin.site.register(Order)
admin.site.register(Inventory)