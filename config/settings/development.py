"""
Configuración de DESARROLLO.
Actívala con: DJANGO_SETTINGS_MODULE=config.settings.development
"""
from .base import *  # noqa: F401, F403

# En desarrollo DEBUG=True muestra errores detallados en el navegador.
# NUNCA activar en producción.
DEBUG = True

# En desarrollo permitimos cualquier host local
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]

# --- Base de datos -------------------------------------------------------
# SQLite es perfecto para desarrollo: no necesita instalar nada.
# En producción se cambiará a PostgreSQL.

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",  # noqa: F405
    }
}

# --- CORS ----------------------------------------------------------------
# En desarrollo permitimos todas las peticiones desde cualquier origen
# para facilitar las pruebas con el frontend.

CORS_ALLOW_ALL_ORIGINS = True

# --- DRF — añadir BrowsableAPI en desarrollo para poder probar la API ----
# en el navegador en http://localhost:8000/api/

REST_FRAMEWORK = {
    **REST_FRAMEWORK,  # noqa: F405
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",  # Solo en desarrollo
    ],
}

# --- Email (consola) -----------------------------------------------------
# En desarrollo los emails se imprimen en la terminal en lugar de enviarse.

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
