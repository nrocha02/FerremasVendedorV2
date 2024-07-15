# FerremasVendedorV2/views.py
from django.shortcuts import render
from .services import get_products

def products_view(request):
    products = get_products()
    return render(request, "products.html", {"products": products["documents"]})
