from django.db import models

from customer.models import Customer


# title, description, price, rating, discount, discounted_price, quantity
class Product(models.Model):
    class Meta:
        ordering = ['-id']
    title = models.CharField(max_length=100)
    description = models.TextField(null=True)
    # price = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.FloatField(default=0)
    rating = models.FloatField()
    discount = models.PositiveIntegerField(default=0, null=True)
    quantity = models.PositiveIntegerField(default=0, null=True)
    my_order = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False,
    )

    def get_attributes(self) -> list[dict]:
        product_attributes = ProductAttributeValue.objects.filter(product=self)
        attributes = []
        for pa in product_attributes:
            attributes.append({
                'attribute_key': pa.attribute_key.key_name,
                'attribute_value': pa.attribute_value.value_name
            })  # [ {},{},{}]
        return attributes

    def __str__(self):
        return self.title

    @property
    def discounted_price(self):
        if self.discount > 0:
            return self.price*(1 - self.discount/100)
        return self.price


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(default=0)
    date_of_order = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.product.title

    @property
    def total_price(self):
        if self.quantity > 0:
            return self.quantity * self.product.price
        return 0


class Image(models.Model):
    image = models.ImageField(upload_to='products', null=True, blank=True)
    product_id = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='images')


class Attribute(models.Model):
    key_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.key_name


class AttributeValue(models.Model):
    value_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.value_name


class ProductAttributeValue(models.Model):
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    attribute_key = models.ForeignKey('product.Attribute', on_delete=models.CASCADE)
    attribute_value = models.ForeignKey('product.AttributeValue', on_delete=models.CASCADE)
