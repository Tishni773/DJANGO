from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'selling_price', 'cost_price', 'status']  # Adjust the fields as needed
