from django.contrib import admin

# Register your models here.

from .models import Order

@admin.register(Order)

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'order_product', 'order_amount','order_payment_id' ,'isPaid', 'order_date']

#    order_product = models.CharField(max_length=100)
#     order_amount = models.CharField(max_length=25)
#     order_payment_id = models.CharField(max_length=100)
#     isPaid = models.BooleanField(default=False)
#     order_date = models.DateTimeField(auto_now=True)