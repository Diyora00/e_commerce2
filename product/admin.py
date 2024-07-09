from django.contrib import admin
from product.models import *


# Register your models here.
# admin.site.register(Product)
admin.site.register(Image)
admin.site.register(Attribute)
admin.site.register(AttributeValue)
admin.site.register(ProductAttributeValue)


# @admin.register(Product)
# class ProductModelAdmin(admin.ModelAdmin):
#     list_display = ('title', 'price',)
#     search_fields = ('title', )
#     list_filter = ('price', )


class CustomModelAdmin(admin.ModelAdmin):

    list_display = ('title', 'price', 'quantity')

    # def has_add_permission(self, request):
    #     return False

    def has_delete_permission(self, request, obj=None):
        if request.user.email == 'suzy@gmail.com':
            return False
        return super().has_delete_permission(request, obj)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)


# Register your model with the custom admin class
admin.site.register(Product, CustomModelAdmin)
