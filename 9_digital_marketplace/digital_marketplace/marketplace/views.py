from django.shortcuts import redirect, render, reverse
from .models import Product,OrderDetail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import stripe,json
import random
from .forms import ProductForm, UserRegistrationForm

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
    if request.method == "POST":
        product_form = ProductForm(request.POST, request.FILES)
        if product_form.is_valid():
            new_product = product_form.save()
            return redirect('index')
    else:
        product_form = ProductForm()
    return render(request, 'marketplace/create_product.html', { 'form': product_form })

def product_edit(request, id):
    product = Product.objects.get(id=id)
    product_form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    if request.method == "POST":
        if product_form.is_valid():
            product_form.save()
            return redirect('index')
    return render(request, 'marketplace/product_edit.html', { 'form': product_form, 'product': product })

def product_delete(request, id):
    product = Product.objects.get(id=id)
    if request.method == "POST":
        product.delete()
        return redirect('index')
    return render(request, 'marketplace/delete.html', { 'product': product })

def dashboard(request):
    products = Product.objects.all()
    return render(request, 'marketplace/dashboard.html',{'products':products})

def register(request):
    form = UserRegistrationForm()
    return render(request, 'marketplace/register.html', { 'user_form': form })