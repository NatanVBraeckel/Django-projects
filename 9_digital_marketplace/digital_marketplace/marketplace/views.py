from django.shortcuts import render, reverse
from .models import Product,OrderDetail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import stripe,json
import random

# Create your views here.
def index(request):
    products = Product.objects.all()
    return render(request, 'marketplace/index.html', { 'products': products })

def detail(request, id):
    product = Product.objects.get(id=id)
    return render(request, 'marketplace/detail.html', { 'product': product })

# @csrf_exempt
def create_checkout_session(request,id):
    # ik ga niet de stripe functionaliteit inbouwen

    request_data = json.loads(request.body)
    product = Product.objects.get(id=id)

    if(random.uniform(0, 1) == 1):
        return render(request, 'marketplace/index.html')
    
    order = OrderDetail()
    order.customer_email = request_data['email']
    order.product = product
    order.amount = int(product.price)
    order.save()
    
    return render(request, 'marketplace/index.html')

def payment_success_view(request, id):
    order = OrderDetail.objects.get(id=id)
    order.has_paid = True
    order.save()

    return render(request, 'marketplace/payment_success.html', { 'order': order })