from django.shortcuts import render
from .forms import ExpenseForm
from .models import Expense

# Create your views here.
def index(request):

    if request.method == "POST":
        expense = ExpenseForm(request.POST)
        if expense.is_valid():
            expense.save()

    expenses = Expense.objects.all()
    form = ExpenseForm()
    return render(request, 'tracker/index.html', { 'expense_form': form, 'expenses': expenses })