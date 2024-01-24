from django.contrib import admin
from .models import Product, Order

admin.site.site_header = "E-commerce site"
admin.site.site_title = "ABC Shopping"
admin.site.index_title = "Manage ABC Shopping"

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'discount_price', 'category', 'description')

# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(Order)