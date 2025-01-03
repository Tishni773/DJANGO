import plotly.graph_objs as go
from django.shortcuts import render, get_object_or_404, redirect
from decimal import Decimal
from .forms import ProductForm, Product
from .models import Supplier
from .models import Product
from .forms import SupplierLoginForm
from django.contrib.auth import authenticate, login

def dashboard(request):
    supplier = get_object_or_404(Supplier, id=0)  # Replace `0` with the appropriate supplier ID
    products = Product.objects.filter(supplier=supplier)

    # Prepare data for the graph
    clicks = []
    commissions = []
    product_names = []

    for product in products:
        product_names.append(product.name)
        clicks.append(product.clicks)
        commissions.append(product.selling_price - product.cost_price)

    # Create the graph using Plotly
    graph = go.Figure()
    graph.add_trace(go.Scatter(x=product_names, y=clicks, mode='lines+markers', name='Clicks'))
    graph.add_trace(go.Scatter(x=product_names, y=commissions, mode='lines+markers', name='Commission'))

    # Convert the graph to HTML
    graph_json = graph.to_html(full_html=False)

    # Calculate summary data
    click = sum(product.clicks for product in products)
    total_returned_value = sum(product.selling_price for product in products.filter(status='returned'))

    delivered_items_count = products.filter(status="delivered").count()
    delivered_items_value = delivered_items_count * 100


    delivered = products.filter(status='delivered')
    profit = sum((p.selling_price - p.cost_price) for p in delivered)
    commission = sum(((p.selling_price - p.cost_price) * (p.commission_rate / 100)) for p in delivered)

    shipped_products = delivered
    total_shipped_revenue = sum(p.selling_price for p in shipped_products)
    transaction_fee_percentage = Decimal(0.005)
    shipping_fee_per_product = 2
    total_fees = sum(
        (p.selling_price * transaction_fee_percentage) + shipping_fee_per_product for p in shipped_products
    )
    pie_data = {
        'labels': ['Commission', 'Bounties', 'Profit'],
        'values': [commission, total_fees, profit],  # Use relevant data
        'type': 'pie'
    }
    pie_chart = go.Figure(data=[pie_data])
    pie_chart_json = pie_chart.to_html(full_html=False)
    
    context = {
        'supplier': supplier,
        'supplier_id' : supplier.id,
        'products': products,
        'delivered_items_value': delivered_items_value,
        'profit': profit,
        'click': click,
        'commission': commission,
        'total_shipped_revenue': total_shipped_revenue,
        'total_returned_items': total_returned_value,
        'total_fees': total_fees,
        'graph': graph_json,
        'pie_chart': pie_chart_json,  
        
    }
    return render(request, 'dashboard.html', context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Calculate total clicks
    total_clicks = product.clicks  # This is directly available in the product model

    # Calculate total sales (products delivered)
    total_sales = Product.objects.filter(id=product_id, status='delivered').count() * product.selling_price*100

    # Calculate total earnings (profit from delivered products)
    total_earnings = sum((p.selling_price - p.cost_price) for p in Product.objects.filter(id=product_id, status='delivered'))*100

    context = {
        'product': product,
        'total_clicks': total_clicks,
        'total_sales': total_sales,
        'total_earnings': total_earnings,
    }

    return render(request, 'product_detail.html', context)


def com(request, id):
    supplier = get_object_or_404(Supplier, id=id)
    products = Product.objects.filter(supplier=supplier)

    total_commission = 0
    total_bounties = 0
    total_profit = 0
    product_details = []

    for product in products:
        profit = product.selling_price - product.cost_price
        commission = profit * (product.commission_rate / 100)
        total_commission += commission
        total_profit += profit
        bounty = commission * Decimal(0.1)
        total_bounties += bounty

        product_details.append({
            'name': product.name,
            'commission': round(commission, 2),
            'bounty': round(bounty, 2),
        })

    context = {
        'supplier': supplier,
        'total_commission': round(total_commission, 2),
        'total_bounties': round(total_bounties, 2),
        'total_profit': round(total_profit, 2),
        'products': product_details,
    }

    return render(request, 'com.html', context)


def add_product(request, supplier_id):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            # Save the form, creating the product in the database
            form.save()
            return redirect('product_list')  # Or redirect to a success page
    else:
        form = ProductForm()

    return render(request, 'add_product.html', {'form': form})
def manage_products(request):
    # Fetch all products from the database
    products = Product.objects.all()
    
    # Render the products management page
    return render(request, 'manage_products.html', {'products': products})

def delete_product(request, product_id):
    # Find and delete the product
    product = Product.objects.get(id=product_id)
    product.delete()
    
    # Redirect to the manage products page after deletion
    return redirect('manage_products')

def supplier_login(request):
    if request.method == "POST":
        form = SupplierLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # Check if the supplier exists with the provided email
            try:
                supplier = Supplier.objects.get(email=email)
            except Supplier.DoesNotExist:
                return render(request, 'supplier_login.html', {'form': form, 'error': 'Supplier not found'})

            # Check if the password matches (you can use custom password validation if needed)
            if supplier.password == password:  # Or use `make_password` to verify against a hashed password
                login(request, supplier)  # Log the supplier in (you can modify this to your preferred authentication method)
                return redirect('dashboard')  # Redirect to the dashboard page
            else:
                return render(request, 'supplier_login.html', {'form': form, 'error': 'Invalid password'})
        else:
            return render(request, 'supplier_login.html', {'form': form})
    else:
        form = SupplierLoginForm()
    return render(request, 'supplier_login.html', {'form': form})