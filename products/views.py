from django.http import HttpRequest
from django.shortcuts import render

from products.models import Product

def list_products(request: HttpRequest):
    products = Product.objects.all()

    if (request.GET.get("free-shipping")):
        products = products.filter(free_shipping=True)
    if (request.GET.get("full")):
        products = products.filter(delivery_type='Full')

    return render(request, "list.html", {"products": products})
