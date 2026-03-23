# Módulo `apps/users` — Lista de tareas

## Estado actual (2026-03-17) — ✅ MÓDULO COMPLETADO

### ✅ Completado
- [x] Instalar `djangorestframework-simplejwt`
- [x] Crear `apps/users/` con:
  - `models.py` — modelo `User` personalizado (extiende `AbstractUser`, login por email, campo `role`)
  - `serializers.py` — `UserSerializer`, `RegisterSerializer`, `CustomTokenObtainPairSerializer`
  - `views.py` — `RegisterView`, `CustomTokenObtainPairView`, `MeView`
  - `urls.py` — rutas: `auth/register/`, `auth/login/`, `auth/token/refresh/`, `users/me/`
  - `apps.py` — configuración de la app
- [x] Añadir `apps.users` a `LOCAL_APPS` en `base.py`
- [x] Configurar `AUTH_USER_MODEL = "users.User"` en `base.py`
- [x] Añadir `rest_framework_simplejwt` y `token_blacklist` a `THIRD_PARTY_APPS`
- [x] Configurar JWT como autenticación por defecto en `REST_FRAMEWORK`
- [x] Añadir bloque `SIMPLE_JWT` a `config/settings/base.py` (tiempos de expiración de tokens)
- [x] Descomentar `path("", include("apps.users.urls"))` en `config/urls.py`
- [x] Ejecutar migraciones (`makemigrations users` + `migrate`)
- [x] Verificar todos los endpoints end-to-end (2026-03-17):
  - `POST /api/v1/auth/register/` → 201 ✅
  - `POST /api/v1/auth/login/` → 200 ✅
  - `POST /api/v1/auth/token/refresh/` → 200 ✅
  - `GET /api/v1/users/me/` (con JWT) → 200 ✅
  - `PATCH /api/v1/users/me/` (con JWT) → 200 ✅
  - `GET /api/v1/users/me/` (sin token) → 401 ✅

---

## Endpoints del módulo users

| Método | URL                          | Auth requerida | Descripción                    |
|--------|------------------------------|----------------|--------------------------------|
| POST   | `/api/v1/auth/register/`     | No             | Crear nueva cuenta             |
| POST   | `/api/v1/auth/login/`        | No             | Obtener access + refresh token |
| POST   | `/api/v1/auth/token/refresh/`| No (refresh)   | Renovar el access token        |
| GET    | `/api/v1/users/me/`          | Sí (JWT)       | Ver perfil del usuario logado  |
| PATCH  | `/api/v1/users/me/`          | Sí (JWT)       | Actualizar perfil              |

---

## Próximos módulos (referencia)
- `apps/courses/` — Cursos y lecciones
- `apps/progress/` — Progreso del usuario
