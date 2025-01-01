from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path("com/<int:id>/", views.com, name='com'),
    path("product/<int:product_id>/", views.product_detail, name='product_detail'),
    path('add_product/<int:supplier_id>/', views.add_product, name='add_product'),
]
