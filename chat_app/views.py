from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden, HttpResponse
from .models import ChatRoom, Message
import logging

# Configure logging
logger = logging.getLogger(__name__)

# View for listing all available chat rooms
@login_required
def index(request):
    """
    Display a list of all available chat rooms.
    """
    logger.debug("Index view called")
    chat_rooms = ChatRoom.objects.all()
    logger.debug(f"Chat rooms retrieved: {list(chat_rooms)}")
    return render(request, 'chat/index.html', {'chat_rooms': chat_rooms})

# View for creating a new chat room
@login_required
def create_chat_room(request):
    """
    Handle the creation of a new chat room.
    """
    logger.debug("Create chat room view called")
    if request.method == 'POST':
        room_name = request.POST.get('name')
        logger.debug(f"Room name received: {room_name}")
        if room_name:
            ChatRoom.objects.create(name=room_name, created_by=request.user)
            logger.debug(f"Chat room created: {room_name}")
            return redirect('index')
        else:
            logger.warning("Room name is required.")
            return HttpResponseForbidden("Room name is required.")
    return render(request, 'chat/create_room.html')

# View for displaying a specific chat room
@login_required
def chat_room(request, room_name):
    """
    Display a specific chat room by its name.
    """
    logger.debug(f"Chat room view called for room: {room_name}")
    chat_room = get_object_or_404(ChatRoom, name=room_name)
    logger.debug(f"Chat room retrieved: {chat_room}")
    return render(request, 'chat/chat_room.html', {'room_name': chat_room.name})

# View for fetching the chat history of a specific room
@login_required
def chat_history(request, room_name):
    """
    Fetch the chat history for a specific room and return it as JSON.
    """
    logger.debug(f"Chat history view called for room: {room_name}")
    try:
        chat_room = get_object_or_404(ChatRoom, name=room_name)
        logger.debug(f"Chat room found: {chat_room}")
        messages = Message.objects.filter(room=chat_room).order_by('timestamp')
        logger.debug(f"Messages retrieved: {messages.count()}")
        serialized_messages = [
            {
                'username': message.user.username,
                'message': message.text,
                'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            }
            for message in messages
        ]
        logger.debug(f"Serialized messages: {serialized_messages}")
        return JsonResponse({'messages': serialized_messages})
    except Exception as e:
        logger.error(f"Error in chat_history view: {e}", exc_info=True)
        return HttpResponse(f"Error: {str(e)}", status=500)
