from django.urls import path
from . import views

urlpatterns = [
    path('supplier_login/', views.supplier_login, name='supplier_login'),
    path('', views.dashboard, name='dashboard'),
    path("com/<int:id>/", views.com, name='com'),
    path("product/<int:product_id>/", views.product_detail, name='product_detail'),
    path('add_product/<int:supplier_id>/', views.add_product, name='add_product'),
    path('manage-products/', views.manage_products, name='manage_products'),
    path('delete-product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('login/', views.supplier_login, name='supplier_login'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
