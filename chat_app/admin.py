from django.contrib import admin
from .models import ChatRoom, Message

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    # Update to use valid model fields
    list_display = ('room', 'user', 'text', 'timestamp')  
    search_fields = ('text', 'user__username')  # Enable search by message text or username
    list_filter = ('room', 'timestamp')  # Add filtering by room and timestamp
