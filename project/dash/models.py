from django.db import models
from django.contrib.auth.models import User

class Supplier(models.Model):
    id = models.AutoField(primary_key=True) 
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  
    

    def __str__(self):
        return self.name

class Product(models.Model):

    STATUS_CHOICES = [
        ('ordered', 'Ordered'),
        ('dispatched', 'Dispatched'),
        ('returned', 'Returned'),
        ('delivered', 'Delivered'),
    ]

    id = models.AutoField(primary_key=True)  
    name = models.CharField(max_length=200)
    clicks = models.IntegerField(default=0)  
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ordered')
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    stock = models.IntegerField(null=True, blank=True)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2)  
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='products')
     

    def __str__(self):
        return self.name
