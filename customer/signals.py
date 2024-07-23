import os
from customer.models import Customer, User
from root.settings import BASE_DIR
from django.core.mail import EmailMessage
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
import json


@receiver(pre_delete, sender=Customer)
def save_deleted_customer(sender, instance, **kwargs):
    file_name = os.path.join(BASE_DIR, 'customer/deleted_customers', f'customer_{instance.id}.json')
    print(f'{instance.fullname} has been deleted')
    data = {
        'fullname': instance.fullname,
        'email': instance.email,
        'phone_number': instance.phone,
        'address': instance.address,
        'joined_date': instance.joined_time_format
            }

    with open(str(file_name), 'a') as file:
        json.dump(data, file, indent=4)


@receiver(post_save, sender=User)
def user_created(sender, instance, created, **kwargs):
    if created:
        subject = 'New User Created'
        message = 'Congratulate you with becoming the new user of Falcon! 😄'
        to = instance.email
        email = EmailMessage(subject, message, to=[to])
        email.send()
