from django.contrib.auth.views import LoginView
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from customer.forms import *
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy


""" Function-based views"""


def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            user = authenticate(request, phone_number=phone_number, password=password)
            if user:
                login(request, user)
                return redirect('customers')
    else:
        form = LoginForm()

    return render(request, 'auth/login.html', {'form': form})


def logout_user(request):
    logout(request)
    return render(request, 'auth/logout.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            form.save()
            login(request, user)
            return redirect('customers')
    else:
        form = RegisterForm()

    context = {'form': form}
    return render(request, 'auth/register.html', context)


""" Class-based views"""


class LoginUserView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'auth/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            user = authenticate(request, phone_number=phone_number, password=password)
            if user:
                login(request, user)
                return redirect('customers')
        return render(request, 'auth/login.html', context)


class RegisterView(SuccessMessageMixin, CreateView):
    template_name = 'auth/register.html'
    success_url = reverse_lazy('login')
    form_class = RegisterForm
    success_message = "Your profile was created successfully"