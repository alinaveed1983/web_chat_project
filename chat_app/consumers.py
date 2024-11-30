import json
import logging
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import ChatRoom, Message
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        self.username = self.scope["user"].username

        # Log the connection attempt
        logger.debug(f"User {self.username} connecting to room {self.room_name}")

        # Join the room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        # Add the user to the room's user list
        if not hasattr(self.channel_layer, "users_in_room"):
            self.channel_layer.users_in_room = {}
        if self.room_group_name not in self.channel_layer.users_in_room:
            self.channel_layer.users_in_room[self.room_group_name] = set()

        self.channel_layer.users_in_room[self.room_group_name].add(self.username)

        # Accept the WebSocket connection
        self.accept()

        # Broadcast updated user list
        self.send_user_list_update()

    def disconnect(self, close_code):
        # Log the disconnection
        logger.debug(f"User {self.username} disconnecting from room {self.room_name}")

        # Leave the room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

        # Remove the user from the room's user list
        if hasattr(self.channel_layer, "users_in_room") and self.room_group_name in self.channel_layer.users_in_room:
            self.channel_layer.users_in_room[self.room_group_name].discard(self.username)

        # Broadcast updated user list
        self.send_user_list_update()

    def send_user_list_update(self):
        try:
            # Get the current list of users in the room
            users_in_room = list(self.channel_layer.users_in_room[self.room_group_name])
            logger.debug(f"Updated user list for room {self.room_name}: {users_in_room}")

            # Broadcast the updated user list to the room
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'user_list_update',
                    'users': users_in_room,
                }
            )
        except Exception as e:
            logger.error(f"Error updating user list: {str(e)}", exc_info=True)

    def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message = data.get('message')

            if not message:
                self.send(text_data=json.dumps({
                    'type': 'error',
                    'message': 'Message content is required.'
                }))
                return

            # Save the message to the database
            chat_room = ChatRoom.objects.get(name=self.room_name)
            user = User.objects.get(username=self.username)
            Message.objects.create(room=chat_room, user=user, text=message)

            # Broadcast the message to the room
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': self.username,
                }
            )
        except ChatRoom.DoesNotExist:
            logger.error(f"Chat room '{self.room_name}' does not exist.", exc_info=True)
            self.send(text_data=json.dumps({
                'type': 'error',
                'message': f"Chat room '{self.room_name}' does not exist."
            }))
        except User.DoesNotExist:
            logger.error(f"User '{self.username}' does not exist.", exc_info=True)
            self.send(text_data=json.dumps({
                'type': 'error',
                'message': f"User '{self.username}' does not exist."
            }))
        except Exception as e:
            logger.error(f"Error in receive method: {str(e)}", exc_info=True)
            self.send(text_data=json.dumps({
                'type': 'error',
                'message': f"An error occurred: {str(e)}"
            }))

    def chat_message(self, event):
        # Send the message to WebSocket
        self.send(text_data=json.dumps({
            'type': 'message',
            'message': event['message'],
            'username': event['username']
        }))

    def user_list_update(self, event):
        # Send the updated user list to WebSocket
        self.send(text_data=json.dumps({
            'type': 'user_list',
            'users': event['users']
        }))
