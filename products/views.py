from django.http import HttpRequest
from django.shortcuts import render

from products.models import Product

def list_products(request: HttpRequest):
    products = Product.objects.all()

    free_shipping = request.GET.get("free-shipping") == "on"
    full = request.GET.get("full") == "on"

    if (free_shipping):
        products = products.filter(free_shipping=True)
    if (full):
        products = products.filter(delivery_type='Full')

    order = request.GET.get("order")
    if order == "price_asc":
        products = products.order_by('price')
    elif order == "price_desc":
        products = products.order_by('-price')
    elif order == "discount_desc":
        products = products.order_by('discount_percentage')

    return render(request, "list.html", {
        "products": products,
        "free_shipping": free_shipping,
        "full": full
    })
