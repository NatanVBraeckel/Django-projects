from django.shortcuts import render
from .models import Movies

# Create your views here.
def movie_list(request):
    list = Movies.objects.all()
    return render(request, 'movies/movie_list.html', {'movie_objects': list})