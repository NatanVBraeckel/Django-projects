import datetime
from django.shortcuts import redirect, render, reverse
from .models import Product,OrderDetail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import stripe,json
import random
from .forms import ProductForm, UserRegistrationForm
from django.db.models import Sum

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
    #updating product sales stats
    product = Product.objects.get(id=order.product.id)
    product.total_sales_amount += int(product.price)
    product.total_sales += 1
    product.save()
    order.save()

    return render(request, 'marketplace/payment_success.html', { 'order': order })

def payment_failed_view(request):
    return render(request, 'marketplace/payment_failed.html')

def create_product(request):
    if request.method == "POST":
        product_form = ProductForm(request.POST, request.FILES)
        if product_form.is_valid():
            new_product = product_form.save(commit=False)
            new_product.seller = request.user
            new_product.save()
            return redirect('index')
    else:
        product_form = ProductForm()
    return render(request, 'marketplace/create_product.html', { 'form': product_form })

def product_edit(request, id):
    product = Product.objects.get(id=id)
    if product.seller != request.user:
        return redirect('invalid')
    
    product_form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    if request.method == "POST":
        if product_form.is_valid():
            product_form.save()
            return redirect('index')
    return render(request, 'marketplace/product_edit.html', { 'form': product_form, 'product': product })

def product_delete(request, id):
    product = Product.objects.get(id=id)
    if product.seller != request.user:
        return redirect('invalid')
    
    if request.method == "POST":
        product.delete()
        return redirect('index')
    return render(request, 'marketplace/delete.html', { 'product': product })

def dashboard(request):
    products = Product.objects.filter(seller=request.user)
    return render(request, 'marketplace/dashboard.html',{'products':products})

def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        new_user = form.save(commit=False)
        new_user.set_password(form.cleaned_data['password'])
        new_user.save()
        return redirect('index')

    form = UserRegistrationForm()
    return render(request, 'marketplace/register.html', { 'user_form': form })

def invalid(request):
    return render(request, 'marketplace/invalid.html')

def my_purchases(request):
    orders = OrderDetail.objects.filter(customer_email=str(request.user.email))
    print(request.user.email)
    return render(request, 'marketplace/purchases.html', { 'orders': orders })

def sales(request):
    orders = OrderDetail.objects.filter(product__seller=request.user)
    total_sales = orders.aggregate(Sum('amount'))

    # 365 day sales
    last_year = datetime.date.today() - datetime.timedelta(days=365)
    data = OrderDetail.objects.filter(product__seller=request.user,created_on__gt=last_year)
    yearly_sales = data.aggregate(Sum('amount'))
    
    # 30 day sales
    last_month = datetime.date.today() - datetime.timedelta(days=30)
    data = OrderDetail.objects.filter(product__seller=request.user,created_on__gt=last_month)
    monthly_sales = data.aggregate(Sum('amount'))
    
    #7 day sales
    last_week = datetime.date.today() - datetime.timedelta(days=7)
    data = OrderDetail.objects.filter(product__seller=request.user,created_on__gt=last_week)
    weekly_sales = data.aggregate(Sum('amount'))

    #everday sum for the past 30 days
    daily_sales_sums = OrderDetail.objects.filter(product__seller=request.user).values('created_on__date').order_by('created_on__date').annotate(sum=Sum('amount'))

    #everday sum for each product
    product_sales_sums = OrderDetail.objects.filter(product__seller=request.user).values('product__name').order_by('product__name').annotate(sum=Sum('amount'))

    return render(request, 'marketplace/sales.html', { 'total_sales': total_sales, 'yearly_sales': yearly_sales, 'monthly_sales': monthly_sales, 'weekly_sales': weekly_sales, 'daily_sales_sums': daily_sales_sums, 'product_sales_sums': product_sales_sums })