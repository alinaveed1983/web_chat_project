"""
WSGI config for web_chat project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""
import os
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_chat.settings')

# Initialize the WSGI application
application = get_wsgi_application()

# Add WhiteNoise to serve static files
application = WhiteNoise(application, root=os.path.join(os.path.dirname(__file__), '../staticfiles'))
