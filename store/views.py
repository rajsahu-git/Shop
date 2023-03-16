from django.shortcuts import get_object_or_404, render
from store.models import Product
from category.models import Category
from cart.views import _cart_id
from cart.models import Cart_item
from django.http import HttpResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


def store(request, category_slug=None):
    category = None
    product = None
    if category_slug != None:
        category = get_object_or_404(Category, slug=category_slug)
        product = Product.objects.all().filter(category=category, is_available=True)
        paginator = Paginator(product, 2)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = product.count()
    else:
        product = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(product, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = product.count()
    return render(request, 'store/store.html', {'product': paged_products, 'count': product_count})


def product_details(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(
            category__slug=category_slug, slug=product_slug)
        in_cart = Cart_item.objects.filter(cart__cart_id=_cart_id(
            request), product=single_product).exists()
    except Exception as e:
        return e
    return render(request, 'store/product_details.html', {'single_product': single_product, 'in_cart': in_cart})
