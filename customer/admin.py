from django.contrib import admin
from customer.models import User, Customer
from customer.forms import UserModelForm
from adminsortable2.admin import SortableAdminMixin


@admin.register(Customer)
class CustomCustomerAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('fullname', 'email', 'phone', 'address', 'is_active')
    ordering = ('my_order',)
    list_editable = ['is_active']


# Register your model with the custom admin class
@admin.register(User)
class CustomUserAdmin(SortableAdminMixin, admin.ModelAdmin):
    form = UserModelForm

    list_display = ['email', 'username', 'date_of_birth', 'is_superuser']
    ordering = ('my_order',)
    list_editable = ['is_superuser']

    def has_delete_permission(self, request, obj=None):
        if request.user.email == 'suzy@gmail.com':
            return False
        return super().has_delete_permission(request, obj)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
