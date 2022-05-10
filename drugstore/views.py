from unicodedata import category
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.conf import settings
from django.http import HttpResponse
from cart.forms import CartAddProductForm
from cart.helpers import Cart
from .forms import ProductForm
from .helpers import product_list_filter_sort
from .models import Category, Product, Like
from .models import Comment
from .forms import CommentForm

def search_product(request):
    category = None
    categories = Category.objects.all()
    products = None
    search = request.GET.get('search')
    if search:
        products = Product.objects.filter(Q(name__icontains=search) |
                                          Q(description__icontains=search)
                                          )
    context = {
        'products': products,
        'categories': categories,
        'category': category
    }
    return render(
        request,
        'product/product_list.html',
        context
    )


def get_product_list(request, category_slug=None):
    """Функция вытаскивает продукты и если слаг приходит заполненым
    то фильтрует по слагу и в конце возвращаем контексты
    """

    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True).order_by('-created_at')
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    # фильтрацию по прайс и по категориям
    products = product_list_filter_sort(
        request,
        products,
        category_slug
    )

    paginator = Paginator(products, settings.PAGINATOR_NUM)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    context = {
        'products': products,
        'categories': categories,
        'category': category,
    }
    return render(
        request,
        'product/product_list.html',
        context
    )


def get_product_detail(request, product_slug):
    """Детализация продукта
    """
    categories = Category.objects.all()
    product = get_object_or_404(Product, slug=product_slug)
    cart_product_form = CartAddProductForm()
    comment = Comment.objects.filter(product=product)
    likes = product.likes.all().count()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comm = form.save(commit=False)
            comm.user = request.user
            comm.product = product
            comm.save()
    else:
        form = CommentForm()

    return render(
        request, 'product/product_detail.html', locals()
    )


def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            # product = Product.objects.create(**form.cleaned_data)
            return redirect(product.get_absolute_url())
    else:
        form = ProductForm()

    return render(request, 'product/create_product.html', {'product_form': form})


def update_product(request, product_slug):
    obj = get_object_or_404(Product, slug=product_slug)
    form = ProductForm(request.POST or None, request.FILES or None, instance=obj)
    if form.is_valid():
        product = form.save()
        # product = Product.objects.create(**form.cleaned_data)
        return redirect(product.get_absolute_url())

    return render(request, 'product/update_product.html', {'product_form': form})



def delete_product(request, product_slug):
    p = Product.objects.get(slug=product_slug)
    Cart(request).remove(p) 
    p.delete() 
    return redirect('/')


def like_product(request, id):
    product = get_object_or_404(Product, id=request.POST.get('product_id'))
    if Like.objects.filter(user=request.user, product=product).exists():
        Like.objects.get(user=request.user, product=product).delete()
    else:
        Like.objects.create(user=request.user, product=product)
    return redirect('drugstore:product_details', product.slug)

def write_db(request):
    import csv
    import os
    open('db.csv', 'w').close()
    products = Product.objects.all()
    with open('db.csv', 'w') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(('product_id', 'category', 'name', 'price'))
        for product in products:
            writer.writerow((product.id, product.category, product.name, product.price))
    with open('db.csv') as f:
        db = f.read()
    os.remove('db.csv')
    return HttpResponse(db, content_type='application/csv')