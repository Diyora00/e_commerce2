from django import forms
from django.contrib.auth.forms import UserCreationForm
from customer.models import Customer, User


class CustomerModelForm(forms.ModelForm):
    class Meta:
        model = Customer
        exclude = ()


class LoginForm(forms.Form):
    # username = forms.CharField()
    phone_number = forms.CharField()
    password = forms.CharField()

    #  the difference between get and filter
    """ get() returns DoesNotExists when nothing is found,
        filter() returns None when nothing is found"""
    def clean_phone_number(self):
        phone_number = self.data.get('phone_number')
        if not User.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError(f'{phone_number} does not exist.')
        return phone_number

    # def clean_email(self):
    #     email = self.data.get('email')
    #     if not User.objects.filter(email=email).exists():
    #         raise forms.ValidationError('Email does not exist')
    #     return email

    def clean_password(self):
        phone_number = self.cleaned_data.get('phone_number')
        password = self.data.get('password')
        try:
            user = User.objects.get(phone_number=phone_number)
            if not user.check_password(password):
                raise forms.ValidationError('Password did not match')
        except User.DoesNotExist:
            raise forms.ValidationError(f'{phone_number} does not exists')
        return password


# class RegisterForm(UserCreationForm):
#     class Meta:
#         model = User
#         model.phone_number = forms.CharField()
#         fields = ('username', 'email', 'password1', 'password2', 'phone_number')

class RegisterForm(forms.ModelForm):

    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '+998.........'}))

    class Meta:
        model = User
        fields = ('username', 'phone_number', 'email', 'date_of_birth', 'password')

    def clean_password(self):
        password = self.cleaned_data.get('password')
        password2 = self.data.get('password2')
        if password2 != password:
            raise forms.ValidationError(f'Passwords did not match {password}, {password2}')

        return password2

    def clean_phone_number(self):
        phone_number = str(self.cleaned_data.get('phone_number'))
        if len(phone_number) != 13 and phone_number[0] != '+':
            raise forms.ValidationError('Invalid phone number')
        return phone_number

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

