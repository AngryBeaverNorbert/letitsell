from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .cart import Cart
from .forms import CartAddProductForm, OrderCreateForm
from .models import Product, Category, OrderItem
from .tasks import order_created


def shop(request, category_slug=None):
    category = None
    categories = Category.objects.all()

    products = Product.available.all()

    # paginator = Paginator(products, 2)
    #
    # try:
    #     page = int(request.GET.get("page", '1'))
    # except ValueError:
    #     page = 1
    #
    # try:
    #     products = paginator.page(page)
    # except (InvalidPage, EmptyPage):
    #     products = paginator.page(paginator.num_pages)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'product/shop.html', {'category': category,
                                                 'categories': categories,
                                                 'products': products})


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, status='available')

    try:
        product.views += 1
        product.save()
    except:
        pass
    cart_product_form = CartAddProductForm()
    return render(request,
                  'product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form})


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('shop:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('shop:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],
                                                                   'update': True})
    return render(request, 'product/cart.html', {'cart': cart})


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # clear the cart
            cart.clear()
            # launch task
            order_created(order.id)
            return render(request, 'orders/created.html', {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'orders/create.html', {'cart': cart,
                                                  'form': form})





# from django.shortcuts import render, redirect, get_object_or_404
# from .models import Product, Category, OrderItem
# from .forms import CartAddProductForm
#
# from django.views.decorators.http import require_POST
# from .cart import Cart
# from .forms import CartAddProductForm, OrderCreateForm
#
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#
# from .tasks import order_created
#
#
# def shop(request, category_slug=None):
#     category = None
#     categories = Category.objects.all()
#     # products = Product.objects.filter(status='available')
#     products = Product.available.all()
#
#     if category_slug:
#         category = get_object_or_404(Category, slug=category_slug)
#         products = products.filter(category=category)
#     return render(request, 'product/shop.html', {'category': category,
#                                                       'categories': categories,
#                                                       'products': products})
#
#
# def product_detail(request, id, slug):
#     product = get_object_or_404(Product, id=id, slug=slug, status='available')
#     cart_product_form = CartAddProductForm()
#     return render(request,
#                   'product/detail.html',
#                   {'product': product,
#                    'cart_product_form': cart_product_form})
#
#
# @require_POST
# def cart_add(request, product_id):
#     cart = Cart(request)
#     product = get_object_or_404(Product, id=product_id)
#     form = CartAddProductForm(request.POST)
#     if form.is_valid():
#         cd = form.cleaned_data
#         cart.add(product=product,
#                  quantity=cd['quantity'],
#                  update_quantity=cd['update'])
#     return redirect('shop:cart_detail')
#
#
# def cart_remove(request, product_id):
#     cart = Cart(request)
#     product = get_object_or_404(Product, id=product_id)
#     cart.remove(product)
#     return redirect('shop:cart_detail')
#
#
# def cart_detail(request):
#     cart = Cart(request)
#     for item in cart:
#         item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],
#                                                                    'update': True})
#     return render(request, 'product/cart.html', {'cart': cart})
#
#
# def order_create(request):
#     cart = Cart(request)
#     if request.method == 'POST':
#         form = OrderCreateForm(request.POST)
#         if form.is_valid():
#             order = form.save()
#             for item in cart:
#                 OrderItem.objects.create(order=order,
#                                          product=item['product'],
#                                          price=item['price'],
#                                          quantity=item['quantity'])
#             # clear the cart
#             cart.clear()
#             # launch task
#             order_created(order.id)
#             return render(request, 'orders/created.html', {'order': order})
#     else:
#         form = OrderCreateForm()
#     return render(request, 'orders/create.html', {'cart': cart, 'form': form})
