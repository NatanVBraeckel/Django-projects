from django.shortcuts import render
from .forms import PostCreateForm
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def post_create(request):
    if request.method == "POST":
        form_data = PostCreateForm(data=request.POST, files=request.FILES)
        if form_data.is_valid():
            new_item = form_data.save(commit=False)
            new_item.user = request.user
            new_item.save()
    else:
        form_data = PostCreateForm(data=request.POST)
    return render(request, 'posts/create.html', {'form': form_data})