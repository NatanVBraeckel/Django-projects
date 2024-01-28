from django.shortcuts import render
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