from django.shortcuts import render, redirect
from customer.models import Customer
from customer.forms import *
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def add_customer(request):
    form = CustomerModelForm()

    if request.method == 'POST':
        form = CustomerModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Customer successfully added!.')
            return redirect('customers')

    context = {'form': form}
    return render(request, 'customer/add-customer.html', context)


def show_customers(request):
    search_post = request.GET.get('search')
    if search_post:
        customers = Customer.objects.filter(Q(fullname__icontains=search_post) | Q(email__icontains=search_post))
    else:
        customers = Customer.objects.all().order_by('-id')

    paginator = Paginator(customers, 2)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {'customers': customers, 'page_obj': page_obj}
    return render(request, 'customer/customers.html', context)


def customer_details(request, customer_id):
    customer = Customer.objects.get(pk=customer_id)
    context = {'customer': customer}
    return render(request, 'customer/customer-details.html', context)


def delete_customer(request, customer_id):
    customer = Customer.objects.get(id=customer_id)

    if request.method == 'POST':
        customer.delete()
        messages.add_message(request, messages.SUCCESS, 'Customer successfully deleted.')
        return redirect('customers')
    return render(request, 'customer/delete-customer.html', {'customer': customer})


def update_customer(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    form = CustomerModelForm(instance=customer)
    if request.method == 'POST':
        form = CustomerModelForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Customer successfully updated.')
            return redirect('customers')

    context = {'form': form}
    return render(request, 'customer/update-customer.html', context)
