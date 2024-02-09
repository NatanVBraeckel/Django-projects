from django.shortcuts import render
from .models import ChatRoom

# Create your views here.
def index(request):
    rooms = ChatRoom.objects.all()
    return render(request, 'chat/index.html', { 'chatrooms': rooms })