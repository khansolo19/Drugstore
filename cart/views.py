from django.shortcuts import (
    render,
    get_object_or_404,
    redirect
)
from django.views.decorators.http import require_http_methods

from cart.forms import CartAddProductForm
from cart.helpers import Cart
from drugstore.models import Product


@require_http_methods(['POST'])
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cleaned_data = form.cleaned_data
        cart.add_or_update(
            product=product,
            quantity=cleaned_data['quantity'],
            update_quantity=cleaned_data['update']
        )
    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    return render(request,
                  'cart_detail.html',{}
                  )
