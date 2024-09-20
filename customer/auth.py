from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib import messages
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
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
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return redirect('verify-email')
    else:
        form = RegisterForm()
    context = {'form': form}
    return render(request, 'auth/register.html', context)


User = get_user_model()


def verify_email(request):
    if request.method == "POST":
        if not request.user.email_is_verified:
            current_site = get_current_site(request)
            user = request.user
            # email = request.user.email
            subject = "Verify Email"
            message = render_to_string('email/verify_email_message.html', {
                'request': request,
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            email = EmailMessage(
                subject, message, to=[request.user.email]
            )
            email.content_subtype = 'html'
            email.send()
            return redirect('verify-email-done')
        else:
            return redirect('register')
    return render(request, 'email/verify_email.html')


def verify_email_done(request):
    return render(request, 'email/verify_email_done.html')


def verify_email_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.email_is_verified = True
        user.save()
        messages.success(request, 'Your email has been verified.')
        return redirect('verify-email-complete')
    else:
        messages.warning(request, 'The link is invalid.')
    return render(request, 'email/verify_email_confirm.html')


def verify_email_complete(request):
    return render(request, 'email/verify_email_complete.html')


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
