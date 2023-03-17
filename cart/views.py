from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
from .models import Cart, Cart_item
from django.core.exceptions import ObjectDoesNotExist


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    if request.method == "POST":
        for item in request.POST:
            key = item
            value = request.POST[key]
            print(key,value)
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
    cart.save()

    try:
        cart_item = Cart_item.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except Cart_item.DoesNotExist:
        cart_item = Cart_item.objects.create(
            product=product, quantity=1, cart=cart)
        cart_item.save()

    # return HttpResponse(cart_item.quantity)
    # exit()
    return redirect('cart')
# Create your views here.


def remove_cart(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = Cart_item.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')


def remove_cart_item(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = Cart_item.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart')


def cart(request, total=0, quantity=0, cart_item=None):
    try:
        tax = 0
        cart_items = 0
        grandtotal = 0
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = Cart_item.objects.filter(cart=cart, is_active=True)
        # print(cart_items)
        for cart_item in cart_items:
            total += (cart_item.product.price*cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2*total)/100
        grandtotal = tax + total
    except ObjectDoesNotExist:
        pass

    return render(request, 'store/cart.html', {'total': total, 'quantity': quantity, 'cart_items': cart_items, 'grandtotal': grandtotal, "tax": tax})
