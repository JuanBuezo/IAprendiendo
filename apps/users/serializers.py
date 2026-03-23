from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Representación pública de un usuario.

    Se usa en dos sitios:
    1. GET  /api/v1/users/me/   → el usuario ve sus propios datos
    2. PATCH /api/v1/users/me/  → el usuario edita su perfil

    'read_only_fields' son campos que se devuelven en la respuesta
    pero que el cliente NO puede modificar directamente (como el rol,
    que solo un admin debería poder cambiar).

    Comparación Spring:
        Este serializer hace el trabajo de UserResponseDTO + UserUpdateDTO
        juntos, controlado por read_only_fields.
    """

    class Meta:
        model  = User
        fields = ["id", "username", "email", "role", "date_joined"]
        read_only_fields = ["id", "email", "role", "date_joined"]


class RegisterSerializer(serializers.ModelSerializer):
    """
    Validación y creación de nuevos usuarios.

    Se usa en:  POST /api/v1/auth/register/

    Tiene dos campos extra (password, password_confirm) que NO están
    en el modelo — solo existen para la validación del formulario de
    registro. 'write_only=True' significa que nunca se devuelven en
    la respuesta (no queremos mandar la contraseña de vuelta al cliente).

    Comparación Spring:
        Equivale a @Valid UserRegisterDTO con un @AssertTrue que valida
        que las contraseñas coinciden.
    """

    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],  # Aplica las reglas de base.py AUTH_PASSWORD_VALIDATORS
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
    )

    class Meta:
        model  = User
        fields = ["username", "email", "password", "password_confirm"]

    def validate(self, attrs):
        """
        Validación a nivel de objeto (cuando necesitas comparar varios campos).
        Si validate_<campo> es validación de un campo individual,
        este método valida relaciones entre campos.
        """
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError(
                {"password_confirm": "Las contraseñas no coinciden."}
            )
        return attrs

    def create(self, validated_data):
        """
        Aquí ocurre la creación real del usuario.
        Usamos create_user (no create) porque create_user se encarga
        de hashear la contraseña automáticamente.
        Si usáramos create(), la contraseña se guardaría en texto plano — un error de seguridad.
        """
        validated_data.pop("password_confirm")
        user = User.objects.create_user(**validated_data)
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Extiende el JWT estándar para incluir datos del usuario en el payload del token.

    Por qué es útil:
    El frontend (React) puede decodificar el JWT y saber el rol del usuario
    sin tener que hacer una petición extra a /users/me/. Esto es especialmente
    útil para mostrar/ocultar elementos de la UI según el rol.

    El token JWT tiene tres partes: header.payload.signature
    El payload es la parte que modificamos aquí. Quedará así:
    {
        "user_id": 1,
        "username": "juan",
        "email": "juan@ejemplo.com",
        "role": "member",
        "exp": 1234567890,   ← cuándo expira (lo añade simplejwt automáticamente)
        "iat": 1234567890    ← cuándo se creó
    }

    Comparación Spring:
        Equivale a un JwtEncoder personalizado que añade claims extra al token.
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Claims personalizados — datos extra en el payload del JWT
        token["username"] = user.username
        token["email"]    = user.email
        token["role"]     = user.role
        return token
