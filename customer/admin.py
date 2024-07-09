from django.contrib import admin
from customer.models import User, Customer


admin.site.register(Customer)


class CustomModelAdmin(admin.ModelAdmin):

    def has_delete_permission(self, request, obj=None):
        if request.user.email == 'suzy@gmail.com':
            return False
        return super().has_delete_permission(request, obj)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)


# Register your model with the custom admin class
admin.site.register(User, CustomModelAdmin)
# Register your models here.
