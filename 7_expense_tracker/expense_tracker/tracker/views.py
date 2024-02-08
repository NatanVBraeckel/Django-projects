from django.shortcuts import render, redirect
from .forms import ExpenseForm
from .models import Expense
from django.db.models import Sum
import datetime

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
    last_year = datetime.today() - datetime.timedelta(days=365)
    dates = Expense.objects.filter(data_gt=last_year)
    total_year = dates.aggregate(Sum('amount'))

    # last month expenses
    last_month = datetime.today() - datetime.timedelta(days=30)
    dates = Expense.objects.filter(data_gt=last_month)
    total_month = dates.aggregate(Sum('amount'))

    # last week expenses
    last_week = datetime.today() - datetime.timedelta(days=7)
    dates = Expense.objects.filter(data_gt=last_week)
    total_week = dates.aggregate(Sum('amount'))

    form = ExpenseForm()
    return render(request, 'tracker/index.html', { 'expense_form': form, 'expenses': expenses, 'total_amount': total_amount, 'total_year': total_year, 'total_month': total_month, 'total_week': total_week })

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