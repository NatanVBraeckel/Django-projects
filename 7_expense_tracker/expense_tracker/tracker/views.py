from django.shortcuts import render, redirect
from .forms import ExpenseForm
from .models import Expense
from django.db.models import Sum
from datetime import datetime, timedelta

# Create your views here.
def index(request):

    if request.method == "POST":
        expense = ExpenseForm(request.POST)
        if expense.is_valid():
            expense.save()

    expenses = Expense.objects.all()
    total_amount = expenses.aggregate(Sum('amount'))
    # print(total_amount)

    # 365 days expenses
    last_year = datetime.today() - timedelta(days=365)
    dates = Expense.objects.filter(data__gt=last_year)
    total_year = dates.aggregate(Sum('amount'))

    # last month expenses
    last_month = datetime.today() - timedelta(days=30)
    dates = Expense.objects.filter(data__gt=last_month)
    total_month = dates.aggregate(Sum('amount'))

    # last week expenses
    last_week = datetime.today() - timedelta(days=7)
    dates = Expense.objects.filter(data__gt=last_week)
    total_week = dates.aggregate(Sum('amount'))

    daily_sums = Expense.objects.filter().values('data').order_by('data').annotate(sum=Sum('amount'))
    # print(daily_sums)

    category_sums = Expense.objects.filter().values('category').order_by('category').annotate(sum=Sum('amount'))
    print(category_sums)

    form = ExpenseForm()
    return render(request, 'tracker/index.html', { 
        'expense_form': form,
        'expenses': expenses,
        'total_amount': total_amount,
        'total_year': total_year,
        'total_month': total_month,
        'total_week': total_week,
        'daily_sums': daily_sums,
        'category_sums': category_sums,
    })

def edit(request, id):

    if request.method == "POST":
        expense = Expense.objects.get(id=id)
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('index')

    expense = Expense.objects.get(id=id)
    form = ExpenseForm(instance=expense)
    return render(request, 'tracker/edit.html',  { 'expense_form': form })

def delete(request, id):
    if request.method == "POST" and "delete" in request.POST:
        expense = Expense.objects.get(id=id)
        expense.delete()
    return redirect('index')