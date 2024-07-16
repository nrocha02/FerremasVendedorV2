"""
URL configuration for FerremasVendedorV2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# FerremasVendedorV2/urls.py
from django.urls import path
from . import views

# urls.py
from django.urls import path
from .views import products_view, comprar_producto, pago_exitoso

urlpatterns = [
    path('products/', products_view, name='products'),
    path('comprar/<str:product_id>/', comprar_producto, name='comprar_producto'),
    path('pago_exitoso/', pago_exitoso, name='pago_exitoso'),
]
