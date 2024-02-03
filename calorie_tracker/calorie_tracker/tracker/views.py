from django.shortcuts import render, redirect
from .models import Consume, Food

# Create your views here.
def index(request):

    if request.method == "POST":
        food_consumed = request.POST['food_consumed']
        consume = Food.objects.get(name=food_consumed)
        user = request.user
        consume_object = Consume(user=user, food_consumed=consume)
        consume_object.save()

    consumed_food = Consume.objects.filter(user=request.user)
    foods = Food.objects.all()

    return render(request, 'tracker/index.html', { 'foods': foods, 'consumed_food': consumed_food })

def delete_consume(request, id):
    consumed_food = Consume.objects.get(id=id)
    if request.method == 'POST':
        consumed_food.delete()
        return redirect('/')
    return render(request, 'tracker/delete.html')