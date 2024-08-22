from django.contrib import admin
from ecomapp.models import Product

# in order to view database tables created in model.py inside "ADMIN" panrl
# Register them (your models) here.
#admin.site.register(Product)  --> it only disply one column on admin panel for product

class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','name','cat','price','is_active'] # --> it disply's all columns from list on admin panel for product

    # to add filter on admin prodct table's panel add below list
    list_filter=['cat','is_active']

admin.site.register(Product, ProductAdmin)