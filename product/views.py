from django.shortcuts import render, redirect
from django.db.models import Q
from product.forms import *  # ProductForm, ProductModelForm
from product.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.


def index(request):
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
