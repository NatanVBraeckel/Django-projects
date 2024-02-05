from django.shortcuts import get_object_or_404, render, redirect
from .forms import PostCreateForm
from django.contrib.auth.decorators import login_required
from .models import Post

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

def feed(request):
    all_posts = Post.objects.all()
    return render(request, 'posts/feed.html', { 'posts': all_posts })

def like_post(request):
    post_id = request.POST.get('post_id')
    post = get_object_or_404(Post, id=post_id)
    if post.liked_by.filter(id=request.user.id).exists():
        post.liked_by.remove(request.user)
    else:
        post.liked_by.add(request.user)
    return redirect('feed')
    