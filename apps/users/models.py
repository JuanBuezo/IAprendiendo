from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Modelo de usuario personalizado de IAprendiendo.

    Extiende AbstractUser de Django para poder añadir campos propios
    sin perder nada de la funcionalidad de autenticación que Django
    ya implementa (contraseña hasheada, permisos, sesiones, admin...).

    RELACIÓN CON EL RESTO DEL PROYECTO:
    - projects:      Project tiene un campo 'members' ManyToMany → User
                     Task tiene 'assigned_to' FK → User
    - collaboration: Message tiene 'author' FK → User
                     Document tiene 'last_edited_by' FK → User
    - study:         Note tiene 'owner' FK → User
                     ChatMessage tiene 'user' FK → User
    Todos los módulos dependen de este modelo. Es la base de la plataforma.
    """

    class Role(models.TextChoices):
        """
        TextChoices es la forma Django de definir un enum con valor y etiqueta.
        Equivale a un enum Java:  enum Role { MEMBER("member"), ADMIN("admin") }

        Por ahora solo dos roles:
        - MEMBER: usuario normal — puede crear proyectos, usar la herramienta de estudio
        - ADMIN:  administrador — gestiona la plataforma (usuarios, contenido)
        Si más adelante necesitas un rol TEACHER, lo añades aquí y en una migración.
        """
        MEMBER = "member", "Miembro"
        ADMIN  = "admin",  "Administrador"

    # Django ya tiene 'username', 'first_name', 'last_name', 'password'.
    # Sobreescribimos email para forzar que sea único (por defecto no lo es).
    email = models.EmailField(
        unique=True,
        verbose_name="correo electrónico",
    )

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.MEMBER,
        verbose_name="rol",
    )

    # Usamos email como campo de login en lugar de username.
    # En Spring sería: @Override String getUsername() { return this.email; }
    USERNAME_FIELD  = "email"
    # AbstractUser requiere declarar qué campos pide al crear un superusuario
    # por línea de comandos además del USERNAME_FIELD y password.
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name        = "usuario"
        verbose_name_plural = "usuarios"
        ordering            = ["-date_joined"]

    def __str__(self):
        return self.email

    @property
    def is_admin(self):
        """Atajo para comprobar el rol. Úsalo en las vistas: user.is_admin"""
        return self.role == self.Role.ADMIN
