from django.db import models
from django.contrib.auth.models import User

class ChatRoom(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chat_rooms", null=True, blank=True)

    def __str__(self):
        return self.name

class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name="messages", default=5)  # Default ChatRoom ID
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages", default=4)  # Default User ID
    text = models.TextField()  # Message content
    timestamp = models.DateTimeField(auto_now_add=True)  # Timestamp when the message was created

    def __str__(self):
        return f"{self.user.username} - {self.text[:20]}"  # Display the first 20 characters of the message
