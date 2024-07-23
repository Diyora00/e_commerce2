import os
import json
from pathlib import Path
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from product.models import Product

BASE_DIR = Path(__file__).resolve().parent.parent


@receiver(pre_delete, sender=Product)
def delete_product(sender, instance, **kwargs):
    print(f'{instance.title} deleted')
    file_name = os.path.join(BASE_DIR, 'product/deleted_products', f'product_{instance.id}.json')
    product_data = {
        'id': instance.id,
        'name': instance.title,
        'price': instance.price,
        'description': instance.description,
        'discount': instance.discount,
        'quantity': instance.quantity,
    }
    with open(str(file_name), 'a') as f:
        json.dump(product_data, f, indent=4)
