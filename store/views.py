from django.shortcuts import get_object_or_404, render
from store.models import Product
from category.models import Category



def store(request,category_slug=None):
    category = None
    product = None
    if category_slug != None:
        category = get_object_or_404(Category,slug=category_slug)
        product  = Product.objects.all().filter(category=category,is_available=True)
        product_count = product.count()
    else:    
        product = Product.objects.all().filter(is_available=True)
        product_count = product.count()
    return render(request, 'store/store.html', {'product': product, 'count': product_count})

def product_details(request,category_slug,product_slug):
    try: 
        single_product = Product.objects.get(category__slug=category_slug,slug=product_slug)
    except Exception as e:
        return e
    return render(request,'store/product_details.html',{'single_product':single_product})