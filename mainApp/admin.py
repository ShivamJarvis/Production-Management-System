from django.contrib import admin
from mainApp.models import Invoice, Job, ProvisionalSchedule, StockRequirement, Supplier, Transaction, UserData,Order,Inventory
# Register your models here.

admin.site.register(UserData)
admin.site.register(Order)
admin.site.register(Inventory)
admin.site.register(StockRequirement)
admin.site.register(Supplier)
admin.site.register(Job)
admin.site.register(ProvisionalSchedule)
admin.site.register(Transaction)
admin.site.register(Invoice)