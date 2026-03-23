"""
Configuración BASE de Django — compartida por todos los entornos.
No usar directamente: importar desde development.py o production.py.
"""
from datetime import timedelta
from pathlib import Path
from decouple import config

# Directorio raíz del proyecto (donde está manage.py)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Clave secreta — se lee del fichero .env (nunca hardcodear aquí)
SECRET_KEY = config("SECRET_KEY")

# --- Aplicaciones instaladas ----------------------------------------------

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "rest_framework",                           # Django REST Framework — el motor de la API
    "corsheaders",                              # Gestión de CORS (permite llamadas desde el frontend)
    "drf_spectacular",                          # Genera documentación OpenAPI automáticamente
    "rest_framework_simplejwt",                 # Autenticación con JWT
    "rest_framework_simplejwt.token_blacklist", # Permite invalidar tokens al hacer logout
]

LOCAL_APPS = [
    "apps.core",             # App de utilidades: health check, helpers, etc.
    "apps.users",            # Usuarios, autenticación y perfiles
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# --- Middleware ------------------------------------------------------------
# Los middleware se ejecutan en orden para cada petición/respuesta.

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",          # CORS — debe ir antes de CommonMiddleware
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# --- URLs y WSGI/ASGI -----------------------------------------------------

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# --- Templates ------------------------------------------------------------

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# --- Validación de contraseñas --------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --- Internacionalización -------------------------------------------------

LANGUAGE_CODE = "es-es"
TIME_ZONE = "Europe/Madrid"
USE_I18N = True
USE_TZ = True

# --- Archivos estáticos y media ------------------------------------------

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# --- Primary key type por defecto ----------------------------------------
# BigAutoField usa enteros de 64-bit en lugar de 32-bit (mejor para tablas grandes)

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- Modelo de usuario personalizado -------------------------------------
# CRÍTICO: debe declararse antes de la primera migración que use usuarios.
# Le dice a Django que use nuestro User (apps/users/models.py) en lugar
# del User por defecto de django.contrib.auth.
# Todos los demás modelos que hagan FK a User deben usar:
#   settings.AUTH_USER_MODEL  (en vez de importar User directamente)
# para evitar dependencias circulares entre apps.

AUTH_USER_MODEL = "users.User"

# --- Django REST Framework -----------------------------------------------
# Configuración global de la API

REST_FRAMEWORK = {
    # Formato de respuesta por defecto
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    # Autenticación: el cliente manda el JWT en el header:
    #   Authorization: Bearer <access_token>
    # Django verifica la firma del token y carga el usuario automáticamente
    # en request.user — igual que Spring Security hace con el SecurityContext.
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    # Permisos: por defecto solo usuarios autenticados pueden acceder.
    # Los endpoints públicos (register, login, health) lo sobreescriben
    # con @permission_classes([AllowAny]) o permission_classes = [AllowAny].
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    # Paginación global — todas las listas devuelven máximo 20 items por página
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    # Esquema para la documentación automática
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# --- Documentación OpenAPI (drf-spectacular) -----------------------------

SPECTACULAR_SETTINGS = {
    "TITLE": "IAprendiendo API",
    "DESCRIPTION": "API REST para la plataforma de aprendizaje con IA",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}

# --- JWT (Simple JWT) -------------------------------------------------------
# Configura los tiempos de vida de los tokens y otras opciones.
# ACCESS_TOKEN_LIFETIME  → cuánto dura el token de acceso (corto, 15-60 min)
# REFRESH_TOKEN_LIFETIME → cuánto dura el token de refresco (más largo, días)
# ROTATE_REFRESH_TOKENS  → al refrescar, se emite un nuevo refresh token
# BLACKLIST_AFTER_ROTATE → el refresh token usado queda invalidado (seguridad)

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME":  timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS":    True,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_HEADER_TYPES":      ("Bearer",),
    "USER_ID_FIELD":          "id",
    "USER_ID_CLAIM":          "user_id",
}
