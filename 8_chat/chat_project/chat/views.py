from django.shortcuts import render
from .models import ChatRoom, ChatMessage

# Create your views here.
def index(request):
    rooms = ChatRoom.objects.all()
    return render(request, 'chat/index.html', { 'chatrooms': rooms })

def chatroom(request, slug):
    room = ChatRoom.objects.get(slug=slug)
    messages = ChatMessage.objects.filter(room=room)[0:30]
    return render(request, 'chat/room.html', { 'chatroom': room, 'messages': messages })