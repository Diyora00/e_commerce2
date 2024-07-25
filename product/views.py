from django.core.mail import BadHeaderError, send_mail
from django.shortcuts import render, redirect
from django.db.models import Q, Sum, Avg, Max, Min, Count, F
from product.forms import *  # ProductForm, ProductModelForm
from product.models import *
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.contrib import messages
import datetime
from django import forms
from django.utils import timezone
from datetime import timedelta



# Create your views here.


# def index(request):
#     search_post = request.GET.get('search')
#     if search_post:
#         products = Product.objects.filter(Q(title__icontains=search_post) | Q(description__icontains=search_post))
#     else:
#         products = Product.objects.all().order_by('-id')
#
#     # pagination
#     paginator = Paginator(products, 2)
#     page_number = request.GET.get('page')
#     try:
#         page_obj = paginator.get_page(page_number)
#     except PageNotAnInteger:
#         page_obj = paginator.page(1)
#     except EmptyPage:
#         page_obj = paginator.page(paginator.num_pages)
#     context = {'products': products, 'page_obj': page_obj}
#
#     return render(request, 'product/product-list.html', context)

class ProductListView(View):
    def get(self, request):
        search_post = request.GET.get('search')
        if search_post:
            products = Product.objects.filter(Q(title__icontains=search_post) | Q(description__icontains=search_post))
        else:
            products = Product.objects.all().order_by('-id')

        # pagination
        paginator = Paginator(products, 2)
        page_number = request.GET.get('page')
        try:
            page_obj = paginator.get_page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        context = {'products': products, 'page_obj': page_obj}

        return render(request, 'product/product-list.html', context)


def product_details(request, product_id):
    product = Product.objects.get(pk=product_id)
    attributes = product.get_attributes()
    context = {
        'product': product,
        'attributes': attributes
    }
    return render(request, 'product/product-details.html', context)


# def add_product(request):
#     form = ProductForm()
#
#     if request.method == 'POST':
#         title = request.POST['title']
#         description = request.POST['description']
#         price = request.POST['price']
#         stock = request.POST['stock']
#         rating = request.POST['rating']
#         discount = request.POST['discount']
#         quantity = request.POST['quantity']
#         form = ProductForm(request.POST)
#
#         product = Product(title=title, description=description, price=price, stock=stock, rating=rating,
#                           discount=discount, quantity=quantity)
#
#         if form.is_valid():
#             product.save()
#             return redirect('index')
#
#     context = {
#         'form': form
#         }
#     return render(request, 'product/add-product.html', context)

def add_product(request):

    form = ProductModelForm()

    if request.method == 'POST':
        form = ProductModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')

    context = {'form': form}

    return render(request, 'product/add-product.html', context)


class DeleteProductView(View):
    def get(self, request, product_id):
        product = Product.objects.get(id=product_id)
        return render(request, 'product/delete_product.html', {'product': product})

    def post(self, request, product_id):
        product = Product.objects.get(id=product_id)
        product.delete()
        return redirect('index')


def send_messages(request):
    m = ''
    if request.method == 'POST':
        subject = request.POST['subject']
        message = request.POST['message']
        from_email = 'bdiyora008@gmail.com'
        to = [request.POST['to'], ]
        if subject and message and from_email:
            try:
                send_mail(subject, message, from_email, to)
                messages.add_message(request, messages.SUCCESS, 'Message is sent.')
            except BadHeaderError:
                return HttpResponse("Invalid header found.")
            return redirect('customers')
        else:
            m = 'Unfilled field detected'
    return render(request, 'email/message.html', {'m': m})


def sorting(request):
    klab = Product.objects.filter(title='Klab').aggregate(quantity_of_ordered_klab=Sum('order__quantity'))
    products = Product.objects.all()
    orders = Order.objects.all()
    total_orders_per_product = Product.objects.annotate(total=Sum('order__quantity'))

    total = Product.objects.aggregate(total_sum_of_orders=Sum(F('price')*F('order__quantity')))
    total_sum_per_product = Product.objects.annotate(total=Sum(F('price')*F('order__quantity')))

    today = datetime.datetime.today()
    start_date = datetime.datetime(year=today.year, month=today.month, day=today.day, hour=0, minute=0,
                                   second=0)  # represents 00:00:00
    end_date = datetime.datetime(year=today.year, month=today.month, day=today.day, hour=23, minute=59,
                                 second=59)  # represents 23:59:59
    ordered_today = Order.objects.filter(date_of_order__range=(start_date, end_date))

    ten_days_ago = timezone.now() - timedelta(days=10)
    orders_last_10_days = Order.objects.filter(date_of_order__gte=ten_days_ago)

    order_per_customer = Customer.objects.annotate(total=Sum('order__quantity'))

    bills = Customer.objects.annotate(total=Sum(F('order__quantity')*F('order__product__price')))
    min_bill = order_per_customer.aggregate(minmumm_bill=Min('total'))
    max_bill = order_per_customer.aggregate(maximum_bill=Max('total'))
    average_bill = order_per_customer.aggregate(average_bill=Avg('total'))
    average_bill = round(average_bill['average_bill'], 2)

    context = {
        'klab': klab,
        'products': products,
        'orders': orders,
        'total': total,

        'today': ordered_today,
        'ten': orders_last_10_days,

        'order_per_customer': order_per_customer,

        'bills': bills,
        'min_bill': min_bill,
        'max_bill': max_bill,
        'average_bill': average_bill,

        'total_orders_per_product': total_orders_per_product,
        'total_sum_per_product': total_sum_per_product,
    }
    return render(request, 'aggregate_annotate.html', context)
