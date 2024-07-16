from django import forms
from product.models import Product


class ProductForm(forms.Form):
    title = forms.CharField(max_length=120)
    description = forms.CharField(widget=forms.Textarea)
    price = forms.FloatField()
    rating = forms.FloatField()
    discount = forms.IntegerField()
    quantity = forms.IntegerField()


class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'rating', 'discount', 'quantity']
        # exclude = () or []  will exclude any field
        # empty exclude = () can be used instead of fields


class MessageForm(forms.Form):
    subject = forms.CharField(max_length=300)
    body = forms.CharField(widget=forms.Textarea(attrs={'size': '30'}))
    from_email = 'bdiyora008@gmail.com'
    to = forms.EmailField()
