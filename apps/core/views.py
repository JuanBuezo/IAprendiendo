from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.conf import settings


@api_view(["GET"])
@permission_classes([AllowAny])
def health_check(request):
    """
    Endpoint de comprobación de salud de la API.
    No requiere autenticación — sirve para verificar que el servidor está activo.

    GET /api/v1/health/
    """
    return Response({
        "status": "ok",
        "version": "1.0.0",
        "debug": settings.DEBUG,
    })
