from django.urls import path
from product.views import *  # (index, product_details, add_product)
from product.plus_view import middleware_view


urlpatterns = [
    path('', ProductListView.as_view(), name='index'),
    path('product_details/int<product_id>', product_details, name='product_details'),
    path('add_product/', add_product, name='add_product'),
    path('delete-product/int<product_id>', DeleteProductView.as_view(), name='delete-product'),

    path('message/', send_messages, name='message'),
    path('test/', middleware_view, name='test'),
    path('list/', sorting, name='list'),

]
