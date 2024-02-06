from django.shortcuts import render
from .forms import ExpenseForm

# Create your views here.
def index(request):

    if request.method == "POST":
        expense = ExpenseForm(request.POST)
        if expense.is_valid():
            expense.save()

    form = ExpenseForm()
    return render(request, 'tracker/index.html', { 'expense_form': form })