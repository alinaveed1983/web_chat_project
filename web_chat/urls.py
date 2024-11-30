from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts_app.urls')),  # Include accounts_app URLs
    path('', include('chat_app.urls')),
]
