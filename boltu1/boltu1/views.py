from django.shortcuts import render


from django.shortcuts import render, get_object_or_404
from .models import Product, Supplier



def dashboard(request):
    supplier = get_object_or_404(Supplier, id=0)
    
    # Fetch all products belonging to the specific supplier
    products = Product.objects.filter(supplier=supplier)
    
    
    # Pass the supplier and products to the template
    context = {
        'supplier': supplier,
        'products': products,
    }
    return render(request, 'dashboard.html', context)
