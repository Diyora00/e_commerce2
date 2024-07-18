from django.urls import path
from customer.views import *
from customer.auth import *
from customer.auth import login_user, logout_user, register, RegisterView, LoginUserView


urlpatterns = [
    path('customers/', CustomerListView.as_view(), name='customers'),
    path('customer_details/int<customer_id>', CustomerDetailTemplateView.as_view(), name='customer_details'),
    path('add_customer/', AddCustomerTemplateView.as_view(), name='add_customer'),
    path('delete_customer/<customer_id>', DeleteCustomerTemplateView.as_view(), name='delete_customer'),
    path('update_customer/<customer_id>', UpdateCustomerTemplateView.as_view(), name='update_customer'),

    path('login/', LoginUserView.as_view(), name='login',),
    path('logout/', logout_user, name='logout'),
    path('register/', register, name='register'),
    path('export_data', export_data, name='export_data'),

    path('verify-email/', verify_email, name='verify-email'),
    path('verify-email/done/', verify_email_done, name='verify-email-done'),
    path('verify-email-confirm/<uidb64>/<token>/', verify_email_confirm, name='verify-email-confirm'),
    path('verify-email/complete/', verify_email_complete, name='verify-email-complete'),
]
