from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User
from .serializers import CustomTokenObtainPairSerializer, RegisterSerializer, UserSerializer


class RegisterView(generics.CreateAPIView):
    """
    POST /api/v1/auth/register/

    Crea un nuevo usuario. No requiere autenticación (AllowAny).

    Flujo:
    1. Recibe { username, email, password, password_confirm }
    2. RegisterSerializer valida los datos (contraseñas iguales, email único, etc.)
    3. Si es válido → crea el usuario con contraseña hasheada
    4. Devuelve 201 con los datos públicos del usuario creado

    Comparación Spring:
        @PostMapping("/auth/register")
        public ResponseEntity<UserDTO> register(@Valid @RequestBody RegisterRequest req)

    RELACIÓN CON EL PROYECTO:
    Este endpoint es el punto de entrada de cualquier usuario a la plataforma.
    Sin él no hay proyectos, ni mensajes, ni estudio. Es el primer paso.
    """

    queryset           = User.objects.all()
    serializer_class   = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # Devolvemos los datos públicos del usuario recién creado
        # (no los del RegisterSerializer, que tiene los campos de contraseña)
        return Response(
            UserSerializer(user).data,
            status=status.HTTP_201_CREATED,
        )


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    POST /api/v1/auth/login/

    Recibe { email, password } y devuelve { access, refresh }.

    - 'access'  → token de corta duración (15 min). Se manda en cada petición.
    - 'refresh' → token de larga duración (7 días). Solo se usa para pedir un access nuevo.

    El cliente React guarda ambos y cuando el access expira llama a
    /auth/token/refresh/ con el refresh para obtener uno nuevo — sin
    que el usuario tenga que volver a hacer login.

    Comparación Spring:
        Equivale al endpoint de Spring Security que devuelve el JWT
        al hacer POST a /auth/login con las credenciales.
    """

    serializer_class = CustomTokenObtainPairSerializer


class MeView(generics.RetrieveUpdateAPIView):
    """
    GET   /api/v1/users/me/  → devuelve los datos del usuario autenticado
    PATCH /api/v1/users/me/  → actualiza username

    'RetrieveUpdateAPIView' implementa GET y PUT/PATCH automáticamente.
    Solo sobreescribimos get_object() para que siempre devuelva el
    usuario del token en lugar de buscar por ID en la URL.

    Por qué no hay /users/{id}/:
    En esta API los usuarios NO pueden ver perfiles ajenos (por privacidad
    y simplicidad). Solo cada usuario ve su propio perfil a través de /me/.
    Si en el futuro se necesita un perfil público, se añade un endpoint nuevo.

    RELACIÓN CON EL PROYECTO:
    El frontend usa este endpoint al cargar la aplicación para saber
    quién está logueado y con qué rol. Con esa info decide si mostrar
    el panel de admin, los proyectos disponibles, etc.
    """

    serializer_class   = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # request.user lo rellena automáticamente el middleware de autenticación
        # JWT al verificar el token del header Authorization: Bearer <token>
        return self.request.user
