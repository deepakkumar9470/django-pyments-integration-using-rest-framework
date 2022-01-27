from django.contrib import admin

from .models import Producst


# Register your models here.

@admin.register(Producst)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'email','paid', 'amount', 'description']

