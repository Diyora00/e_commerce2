from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from product.models import *

# Register your models here.
# admin.site.register(Product)
admin.site.register(Image)
admin.site.register(Attribute)
admin.site.register(AttributeValue)
admin.site.register(ProductAttributeValue)
admin.site.register(Order)


class ProductRecourse(resources.ModelResource):
    class Meta:
        model = Product


@admin.register(Product)
class ProductModelAdmin(SortableAdminMixin, ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'discount', 'quantity')
    search_fields = ('title',)
    list_filter = ('price',)
    ordering = ('my_order',)
    resource_class = ProductRecourse

    # def has_add_permission(self, request):
    #     return False

    def has_delete_permission(self, request, obj=None):
        if request.user.email == 'suzy@gmail.com':
            return False
        return super().has_delete_permission(request, obj)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)


# class CustomModelAdmin(admin.ModelAdmin):
#     list_display = ('title', 'price', 'quantity')
#
#     # def has_add_permission(self, request):
#     #     return False
#
#     def has_delete_permission(self, request, obj=None):
#         if request.user.email == 'suzy@gmail.com':
#             return False
#         return super().has_delete_permission(request, obj)
#
#     def save_model(self, request, obj, form, change):
#         super().save_model(request, obj, form, change)

# Register your model with the custom admin class
# admin.site.register(Product, CustomModelAdmin)
