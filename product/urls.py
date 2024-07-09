from django.urls import path
from product.views import *  # (index, product_details, add_product)


urlpatterns = [
    path('', index, name='index'),
    path('product_details/int<product_id>', product_details, name='product_details'),
    path('add_product/', add_product, name='add_product'),
]
