"""
Punto de entrada ASGI — usado por servidores asíncronos como Daphne o Uvicorn.
Necesario para WebSockets y HTTP/2 en el futuro.
"""
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")

application = get_asgi_application()
