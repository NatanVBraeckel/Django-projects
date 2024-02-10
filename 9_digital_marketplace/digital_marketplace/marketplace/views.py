from django.shortcuts import redirect, render, reverse
from .models import Product,OrderDetail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import stripe,json
import random
from .forms import ProductForm

# Create your views here.
def index(request):
    products = Product.objects.all()
    return render(request, 'marketplace/index.html', { 'products': products })

def detail(request, id):
    product = Product.objects.get(id=id)
    return render(request, 'marketplace/detail.html', { 'product': product })

@csrf_exempt
def create_checkout_session(request, id):
    # ik ga niet de stripe functionaliteit inbouwen, ik ga mocken of een payment failed of success is

    request_data = json.loads(request.body)
    product = Product.objects.get(id=id)

    if random.uniform(0, 1) < 0.2:
        return redirect('failed')
    
    order = OrderDetail()
    order.customer_email = request_data['email']
    order.product = product
    order.amount = int(product.price)
    order.save()
    
    return redirect('success', order.id)

def payment_success_view(request, id):
    order = OrderDetail.objects.get(id=id)
    order.has_paid = True
    order.save()

    return render(request, 'marketplace/payment_success.html', { 'order': order })

def payment_failed_view(request):
    return render(request, 'marketplace/payment_failed.html')

def create_product(request):
    product_form = ProductForm()
    return render(request, 'marketplace/create_product.html', { 'form': product_form })