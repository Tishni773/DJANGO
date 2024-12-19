from django.db import models

class Supplier(models.Model):
    id = models.AutoField(primary_key=True)  # Primary ID for Supplier
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Use Django's hashing mechanism when storing

    def __str__(self):
        return self.name

class Product(models.Model):
    STATUS_CHOICES = [
        ('ordered', 'Ordered'),
        ('dispatched', 'Dispatched'),
        ('returned', 'Returned'),
        ('delivered', 'Delivered'),
    ]

    id = models.AutoField(primary_key=True)  # Primary ID for Product
    name = models.CharField(max_length=200)
    clicks = models.IntegerField(default=0)  # Number of clicks
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ordered')
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    stock = models.PositiveIntegerField()  # Stock quantity
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2)  # Commission rate as percentage
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='products')  # Foreign key to Supplier

    def __str__(self):
        return self.name
