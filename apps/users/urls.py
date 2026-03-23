from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

# Estas rutas se montan bajo /api/v1/ en config/urls.py
# así que las URLs finales son:
#   POST  /api/v1/auth/register/
#   POST  /api/v1/auth/login/
#   POST  /api/v1/auth/token/refresh/
#   GET   /api/v1/users/me/
#   PATCH /api/v1/users/me/

urlpatterns = [
    # --- Autenticación -------------------------------------------------------
    path("auth/register/",      views.RegisterView.as_view(),            name="auth-register"),
    path("auth/login/",         views.CustomTokenObtainPairView.as_view(), name="auth-login"),

    # TokenRefreshView viene directamente de simplejwt — no necesitamos
    # crear una vista propia para esto.
    path("auth/token/refresh/", TokenRefreshView.as_view(),              name="token-refresh"),

    # --- Perfil del usuario autenticado --------------------------------------
    path("users/me/",           views.MeView.as_view(),                  name="users-me"),
]
