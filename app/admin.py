from django.contrib import admin
from .models import *

# Register your models here.

class ProductImageAdmin(admin.TabularInline):
    model = ProductImage

class AdditionalInfoAdmin(admin.TabularInline):
    model = AdditionalInfo

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin, AdditionalInfoAdmin]
    list_display = ('product_name','price','category','color','section')
    list_editable = ('category','section', 'color')

admin.site.register(Slider)
admin.site.register(BannerArea)
admin.site.register(MainCategoty)
admin.site.register(Category)
admin.site.register(Section)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(AdditionalInfo)
admin.site.register(Color)
admin.site.register(Brand)
admin.site.register(CouponCode)