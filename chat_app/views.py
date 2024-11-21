from django.shortcuts import render
from .models import ChatRoom

def index(request):
    chat_rooms = ChatRoom.objects.all()
    return render(request, 'chat/index.html', {'chat_rooms': chat_rooms})
