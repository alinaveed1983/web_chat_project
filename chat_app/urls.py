from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create_chat_room, name='create_room'),
    path('<str:room_name>/', views.chat_room, name='chat_room'),
    path('history/<str:room_name>/', views.chat_history, name='chat_history'),
]
