from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from customer.managers import CustomUserManager


class Customer(models.Model):
    fullname = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=100, unique=True)
    address = models.CharField(max_length=250)
    joined = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='customer/', null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def joined_time_format(self):
        return self.joined.strftime('%B %d, %Y at %I:%M %p')

    def __str__(self):
        return self.email

    class Meta:
        ordering = ('-id',)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=True, blank=True)
    username = models.CharField(unique=True, null=True, blank=True, max_length=50)
    phone_number = models.CharField(unique=True, null=True, blank=True, max_length=15)
    date_of_birth = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # this method must return what is assigned to USERNAME_FIELD (in this case 'email)
    # if anything else is returned it arises an ERROR
    def __str__(self):
        return self.email
