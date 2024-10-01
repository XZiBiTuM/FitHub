import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets, generics, status
from .models import *
from django.views.decorators.http import require_POST
from .forms import *
from django.core.mail import EmailMessage
from .serializers import *
from django.template.loader import render_to_string


def protein_catalog(request):
    protein_category = ProductCategory.objects.get(category='Протеин')
    products = Product.objects.filter(category=protein_category)

    brands = products.values_list('brand', flat=True).distinct()

    selected_brand = request.GET.get('brand')
    sort_by = request.GET.get('sort_by')

    if selected_brand:
        products = products.filter(brand=selected_brand)

    if sort_by:
        products = products.order_by(sort_by)

    return render(request, 'protein_catalog.html', {
        'products': products,
        'brands': brands,
        'selected_brand': selected_brand,
        'sort_by': sort_by,
        'title': 'Протеин',
    })


def creatine_catalog(request):
    creatine_category = ProductCategory.objects.get(category='Креатин')
    products = Product.objects.filter(category=creatine_category)

    brands = products.values_list('brand', flat=True).distinct()

    selected_brand = request.GET.get('brand')
    sort_by = request.GET.get('sort_by')

    if selected_brand:
        products = products.filter(brand=selected_brand)

    if sort_by:
        products = products.order_by(sort_by)

    return render(request, 'creatine_catalog.html', {
        'products': products,
        'brands': brands,
        'selected_brand': selected_brand,
        'sort_by': sort_by,
        'title': 'Креатин',
    })


def gainer_catalog(request):
    gainer_category = ProductCategory.objects.get(category='Гейнер')
    products = Product.objects.filter(category=gainer_category)

    brands = products.values_list('brand', flat=True).distinct()

    selected_brand = request.GET.get('brand')
    sort_by = request.GET.get('sort_by')

    if selected_brand:
        products = products.filter(brand=selected_brand)

    if sort_by:
        products = products.order_by(sort_by)

    return render(request, 'gainer_catalog.html', {
        'products': products,
        'brands': brands,
        'selected_brand': selected_brand,
        'sort_by': sort_by,
        'title': 'Гейнер',
    })


def sport_bars_catalog(request):
    sport_bars_category = ProductCategory.objects.get(category='Спортивные батончики')
    products = Product.objects.filter(category=sport_bars_category)

    brands = products.values_list('brand', flat=True).distinct()

    selected_brand = request.GET.get('brand')
    sort_by = request.GET.get('sort_by')

    if selected_brand:
        products = products.filter(brand=selected_brand)

    if sort_by:
        products = products.order_by(sort_by)

    return render(request, 'sport_bars_catalog.html', {
        'products': products,
        'brands': brands,
        'selected_brand': selected_brand,
        'sort_by': sort_by,
        'title': 'Спортивные батончики',
    })


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html',
                  {'product': product, 'title': product.title})


def main(request):
    return render(request, 'main.html', {'title': 'Главная'})


@csrf_exempt
def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        cart = request.session.get('cart', {})

        if str(product_id) in cart:
            cart[str(product_id)] += 1
        else:
            cart[str(product_id)] = 1

        request.session['cart'] = cart

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'}, status=400)


@csrf_exempt
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        del cart[str(product_id)]

    request.session['cart'] = cart

    products = Product.objects.filter(id__in=cart.keys())
    cart_items = []
    total_price = 0

    for product in products:
        quantity = cart[str(product.id)]
        total_price += product.price * quantity
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total_price': product.price * quantity
        })

    response_data = {
        'cart_items': [{
            'id': item['product'].id,
            'title': item['product'].title,
            'quantity': item['quantity'],
            'total_price': item['total_price']
        } for item in cart_items],
        'total_price': total_price
    }

    return JsonResponse(response_data)


@csrf_exempt
def update_cart_quantity(request, product_id, action):
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        if action == 'increase':
            cart[str(product_id)] += 1
        elif action == 'decrease' and cart[str(product_id)] > 1:
            cart[str(product_id)] -= 1
        elif action == 'decrease' and cart[str(product_id)] == 1:
            del cart[str(product_id)]

    request.session['cart'] = cart

    products = Product.objects.filter(id__in=cart.keys())
    cart_items = []
    total_price = 0

    for product in products:
        quantity = cart[str(product.id)]
        total_price += product.price * quantity
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total_price': product.price * quantity
        })

    response_data = {
        'cart_items': [{
            'id': item['product'].id,
            'title': item['product'].title,
            'quantity': item['quantity'],
            'total_price': item['total_price']
        } for item in cart_items],
        'total_price': total_price
    }

    return JsonResponse(response_data)


def cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        total_price += product.price * quantity
        cart_items.append({
            'product': product,
            'price': product.price,
            'quantity': quantity,
            'total_price': product.price * quantity
        })

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'cart_fragment.html', {'cart_items': cart_items, 'total_price': total_price})

    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price, 'title': 'Корзина'})


@require_POST
def check_stock(request):
    cart = request.session.get('cart', {})
    insufficient_stock = []

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        total_quantity = ProductQuantity.objects.get(product=product).quantity
        print(total_quantity)

        if total_quantity < quantity:
            insufficient_stock.append({
                'product_id': product.id,
                'title': product.title,
                'requested_quantity': quantity,
                'available_quantity': total_quantity
            })

    if insufficient_stock:
        return JsonResponse({'status': 'error', 'insufficient_stock': insufficient_stock})
    else:
        return JsonResponse({'status': 'ok'})


def order(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            user_form = form.save()

            order = Order.objects.create(
                user=user_form,
                total_price=0,
                payment_status='Заказ в обработке'
            )

            total_price = 0

            for product_id, quantity in cart.items():
                product = get_object_or_404(Product, id=product_id)
                total_quantity = get_object_or_404(ProductQuantity, product=product)
                print(total_quantity)
                item_price = product.price * quantity
                total_price += item_price

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=item_price
                )

                total_quantity.quantity -= quantity
                total_quantity.save()

            order.total_price = total_price
            order.save()

            request.session['cart'] = {}
            return JsonResponse({'status': 'ok'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})

    form = OrderForm()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'order_fragment.html', {'form': form})

    return render(request, 'order.html', {'form': form})


def order_success(request):
    return render(request, 'order_success.html')


import datetime
from django.db.models import F
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets, generics, status
from .models import *
from django.views.decorators.http import require_POST
from .forms import *
from django.core.mail import EmailMessage
from .serializers import *
from django.template.loader import render_to_string


def protein_catalog(request):
    protein_category = ProductCategory.objects.get(category='Протеин')
    products = Product.objects.filter(category=protein_category)

    brands = products.values_list('brand', flat=True).distinct()

    selected_brand = request.GET.get('brand')
    sort_by = request.GET.get('sort_by')

    if selected_brand:
        products = products.filter(brand=selected_brand)

    if sort_by:
        products = products.order_by(sort_by)

    return render(request, 'protein_catalog.html', {
        'products': products,
        'brands': brands,
        'selected_brand': selected_brand,
        'sort_by': sort_by,
        'title': 'Протеин',
    })


def creatine_catalog(request):
    creatine_category = ProductCategory.objects.get(category='Креатин')
    products = Product.objects.filter(category=creatine_category)

    brands = products.values_list('brand', flat=True).distinct()

    selected_brand = request.GET.get('brand')
    sort_by = request.GET.get('sort_by')

    if selected_brand:
        products = products.filter(brand=selected_brand)

    if sort_by:
        products = products.order_by(sort_by)

    return render(request, 'creatine_catalog.html', {
        'products': products,
        'brands': brands,
        'selected_brand': selected_brand,
        'sort_by': sort_by,
        'title': 'Креатин',
    })


def gainer_catalog(request):
    gainer_category = ProductCategory.objects.get(category='Гейнер')
    products = Product.objects.filter(category=gainer_category)

    brands = products.values_list('brand', flat=True).distinct()

    selected_brand = request.GET.get('brand')
    sort_by = request.GET.get('sort_by')

    if selected_brand:
        products = products.filter(brand=selected_brand)

    if sort_by:
        products = products.order_by(sort_by)

    return render(request, 'gainer_catalog.html', {
        'products': products,
        'brands': brands,
        'selected_brand': selected_brand,
        'sort_by': sort_by,
        'title': 'Гейнер',
    })


def sport_bars_catalog(request):
    sport_bars_category = ProductCategory.objects.get(category='Спортивные батончики')
    products = Product.objects.filter(category=sport_bars_category)

    brands = products.values_list('brand', flat=True).distinct()

    selected_brand = request.GET.get('brand')
    sort_by = request.GET.get('sort_by')

    if selected_brand:
        products = products.filter(brand=selected_brand)

    if sort_by:
        products = products.order_by(sort_by)

    return render(request, 'sport_bars_catalog.html', {
        'products': products,
        'brands': brands,
        'selected_brand': selected_brand,
        'sort_by': sort_by,
        'title': 'Спортивные батончики',
    })


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html',
                  {'product': product, 'title': product.title})


def main(request):
    return render(request, 'main.html', {'title': 'Главная'})


@csrf_exempt
def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        cart = request.session.get('cart', {})

        if str(product_id) in cart:
            cart[str(product_id)] += 1
        else:
            cart[str(product_id)] = 1

        request.session['cart'] = cart

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'}, status=400)


@csrf_exempt
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        del cart[str(product_id)]

    request.session['cart'] = cart

    products = Product.objects.filter(id__in=cart.keys())
    cart_items = []
    total_price = 0

    for product in products:
        quantity = cart[str(product.id)]
        total_price += product.price * quantity
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total_price': product.price * quantity
        })

    response_data = {
        'cart_items': [{
            'id': item['product'].id,
            'title': item['product'].title,
            'quantity': item['quantity'],
            'total_price': item['total_price']
        } for item in cart_items],
        'total_price': total_price
    }

    return JsonResponse(response_data)


@csrf_exempt
def update_cart_quantity(request, product_id, action):
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        if action == 'increase':
            cart[str(product_id)] += 1
        elif action == 'decrease' and cart[str(product_id)] > 1:
            cart[str(product_id)] -= 1
        elif action == 'decrease' and cart[str(product_id)] == 1:
            del cart[str(product_id)]

    request.session['cart'] = cart

    products = Product.objects.filter(id__in=cart.keys())
    cart_items = []
    total_price = 0

    for product in products:
        quantity = cart[str(product.id)]
        total_price += product.price * quantity
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total_price': product.price * quantity
        })

    response_data = {
        'cart_items': [{
            'id': item['product'].id,
            'title': item['product'].title,
            'quantity': item['quantity'],
            'total_price': item['total_price']
        } for item in cart_items],
        'total_price': total_price
    }

    return JsonResponse(response_data)


def cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        total_price += product.price * quantity
        cart_items.append({
            'product': product,
            'price': product.price,
            'quantity': quantity,
            'total_price': product.price * quantity
        })

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'cart_fragment.html', {'cart_items': cart_items, 'total_price': total_price})

    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price, 'title': 'Корзина'})


@require_POST
def check_stock(request):
    cart = request.session.get('cart', {})
    insufficient_stock = []

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        total_quantity = ProductQuantity.objects.get(product=product).quantity
        print(total_quantity)

        if total_quantity < quantity:
            insufficient_stock.append({
                'product_id': product.id,
                'title': product.title,
                'requested_quantity': quantity,
                'available_quantity': total_quantity
            })

    if insufficient_stock:
        return JsonResponse({'status': 'error', 'insufficient_stock': insufficient_stock})
    else:
        return JsonResponse({'status': 'ok'})


def order(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            user_form = form.save()

            order = Order.objects.create(
                user=user_form,
                total_price=0,
                payment_status='Заказ в обработке'
            )

            total_price = 0

            for product_id, quantity in cart.items():
                product = get_object_or_404(Product, id=product_id)
                total_quantity = get_object_or_404(ProductQuantity, product=product)
                print(total_quantity)
                item_price = product.price * quantity
                total_price += item_price

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=item_price
                )

                total_quantity.quantity -= quantity
                total_quantity.save()

            order.total_price = total_price
            order.save()

            request.session['cart'] = {}
            return JsonResponse({'status': 'ok'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})

    form = OrderForm()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'order_fragment.html', {'form': form})

    return render(request, 'order.html', {'form': form})


def order_success(request):
    return render(request, 'order_success.html')


class ProductDetailViewSet(viewsets.ModelViewSet):
    queryset = ProductDetail.objects.all()
    serializer_class = ProductDetailSerializer


class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer


class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductProteinViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(category=1)
    serializer_class = ProductSerializerProtein


class ProductCreatineViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(category=2)
    serializer_class = ProductSerializerCreatine


class ProductGainerViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(category=3)
    serializer_class = ProductSerializerGainer


class ProductSportBarsViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(category=4)
    serializer_class = ProductSerializerSportBar


class ProductProteinBrandViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(category=1).values('brand').distinct()
    serializer_class = ProductProteinBrandsSerializer


class ProductCreatineBrandViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(category=2).values('brand').distinct()
    serializer_class = ProductCreatineBrandsSerializer


class ProductGainerBrandViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(category=3).values('brand').distinct()
    serializer_class = ProductGainerBrandsSerializer


class ProductSportBarsBrandViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(category=4).values('brand').distinct()
    serializer_class = ProductSportBarsBrandsSerializer


class BasketViewSet(viewsets.ModelViewSet):
    queryset = Basket.objects.all()
    serializer_class = BasketSerializer


class ProductQuantityViewSet(viewsets.ModelViewSet):
    queryset = ProductQuantity.objects.all()
    serializer_class = ProductQuantitySerializer


class FormViewSet(viewsets.ModelViewSet):
    queryset = Form.objects.all()
    serializer_class = FormSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class ProductIDViewSet(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductIDSerializer
    lookup_field = 'id'


@api_view(['POST'])
def product_create(request):
    if request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def product_create_protein(request):
    if request.method == 'POST':
        serializer = ProductSerializerProtein(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def product_create_creatine(request):
    if request.method == 'POST':
        serializer = ProductSerializerCreatine(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def product_create_gainer(request):
    if request.method == 'POST':
        serializer = ProductSerializerGainer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def product_create_sport_bar(request):
    if request.method == 'POST':
        serializer = ProductSerializerSportBar(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def product_create_protein_brands(request):
    if request.method == 'POST':
        serializer = ProductProteinBrandsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def product_create_creatine_brands(request):
    if request.method == 'POST':
        serializer = ProductCreatineBrandsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def product_create_gainer_brands(request):
    if request.method == 'POST':
        serializer = ProductGainerBrandsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def product_create_sport_bars_brands(request):
    if request.method == 'POST':
        serializer = ProductSportBarsBrandsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def product_detail_create(request):
    if request.method == 'POST':
        serializer = ProductDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def product_image_create(request):
    if request.method == 'POST':
        serializer = ProductImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def product_category_create(request):
    if request.method == 'POST':
        serializer = ProductCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def basket_create(request):
    if request.method == 'POST':
        serializer = BasketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def product_quantity_create(request):
    if request.method == 'POST':
        serializer = ProductQuantitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def form_create(request):
    if request.method == 'POST':
        serializer = FormSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def order_create(request):
    if request.method == 'POST':
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def order_item_create(request):
    if request.method == 'POST':
        serializer = OrderItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def payment_create(request):
    if request.method == 'POST':
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
