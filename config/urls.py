"""
URL principal del proyecto.
Aquí se montan todas las rutas de las distintas apps y de la documentación.
"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    # Panel de administración de Django
    path("admin/", admin.site.urls),

    # --- API v1 -----------------------------------------------------------
    path("api/v1/", include([
        # App core: health check y utilidades
        path("", include("apps.core.urls")),

        # Aquí irás añadiendo las rutas de cada nueva app:
        # path("users/", include("apps.users.urls")),
        # path("courses/", include("apps.courses.urls")),
    ])),

    # --- Documentación OpenAPI -------------------------------------------
    # /api/schema/         → fichero YAML/JSON con el esquema completo
    # /api/docs/           → Swagger UI interactivo
    # /api/docs/redoc/     → ReDoc (alternativa más legible)
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/docs/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]
