from django.core.management.base import BaseCommand
from daphne.server import Server
from web_chat.asgi import application  # Import the ASGI application directly


class Command(BaseCommand):
    help = "Run the ASGI server with Daphne"

    def add_arguments(self, parser):
        parser.add_argument(
            "--port", "-p",
            type=int,
            default=8000,
            help="Port number to listen on (default: 8000)."
        )
        parser.add_argument(
            "--host", "-b",
            type=str,
            default="0.0.0.0",
            help="Host address to bind to (default: 0.0.0.0)."
        )

    def handle(self, *args, **options):
        host = options.get("host", "0.0.0.0")
        port = options.get("port", 8000)

        # Pass the ASGI application directly
        Server(
            application=application,
            endpoints=[f"tcp:{port}:interface={host}"],
            signal_handlers=False  # Avoid conflicts with Django signal handlers
        ).run()
