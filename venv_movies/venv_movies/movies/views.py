from django.shortcuts import render
from .models import Movies
from django.core.paginator import Paginator

# Create your views here.
def movie_list(request):
    list = Movies.objects.all()

    paginator = Paginator(list, 4)
    page = request.GET.get('page')
    movie_objects = paginator.get_page(page)

    return render(request, 'movies/movie_list.html', {'movie_objects': movie_objects})