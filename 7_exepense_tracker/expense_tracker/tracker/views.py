from django.shortcuts import render
from .forms import ExpenseForm

# Create your views here.
def index(request):
    form = ExpenseForm()
    return render(request, 'tracker/index.html', { 'expense_form': form })