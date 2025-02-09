"""
URL configuration for RestAPI project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from EventManager import views
from rest_framework.authtoken.views import ObtainAuthToken
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

# Importaciones para eventos
from EventManager.views import ListarEventosAPIView, CrearEventoAPIView, ActualizarEventoAPIView, EliminarEventoAPIView

# Importaciones para reservas
from EventManager.views import ListarReservasAPIView, CrearRervaAPIView, ActualizarReservaAPIView, CancelarReservaAPIView

# Importaciones para comentarios
from EventManager.views import ListarComentariosAPIView, CrearcomentariosAPIView


from drf_yasg.views import get_schema_view
schema_view = get_schema_view(
    openapi.Info(
        title="EventManager API",
        default_version="v1",
        description="API para gestionar eventos y reservas",
    ),
    public=True, # Documentación disponible para cualquier usuario
    permission_classes=[AllowAny], #Permitir acceso sin autenticación
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login', ObtainAuthToken.as_view(), name='api_token_auth'),
    #path('eventos', views.listar_eventos, name='listar_eventos'),
    #path('eventos/crear', views.crear_evento, name='crear_evento'),
    #path('eventos/<int:evento_id>/actualizar', views.actualizar_evento, name='actualizar_evento'),
    #path('eventos/<int:evento_id>/eliminar', views.eliminar_evento, name='eliminar_evento'),
    #path('reservas/<str:username>', views.listar_reservas, name='listar_reservas'),
    #path('reservas/crear/', views.crear_reserva, name='crear_reserva'),
    #path('reservas/<int:reserva_id>/actualizar', views.actualizar_reserva, name='actualizar_reserva'),
    #path('reservas/<int:reserva_id>/cancelar', views.cancelar_reserva, name='cancelar_reserva'),
    #path('eventos/<int:evento_id>/comentarios', views.listar_comentarios, name='listar_comentarios'),
    #path('eventos/<int:evento_id>/comentarios/crear', views.crear_comentario, name='crear_comentario'),
    path('register', views.register, name='register'),


    path('eventos/', ListarEventosAPIView.as_view(), name='listar_eventos'),
    path('eventos/crear/', CrearEventoAPIView.as_view(), name='crear_eventos'),
    path('eventos/<int:evento_id>/actualizar/', ActualizarEventoAPIView.as_view(), name='actualizar_evento'),
    path('eventos/<int:evento_id>/eliminar/', EliminarEventoAPIView.as_view(), name='eliminar_evento'),
    path('reservas/', ListarReservasAPIView.as_view(), name='listar_reservas'),
    path('reservas/crear/', CrearRervaAPIView.as_view(), name='crear_reserva'),
    path('reservas/<int:reserva_id>/actualizar/', ActualizarReservaAPIView.as_view(), name='actualizar_reserva'),
    path('reservas/<int:reserva_id>/cancelar/', CancelarReservaAPIView.as_view(), name='cancelar_reserva'),
    path('eventos/<int:evento_id>/comentarios/', ListarComentariosAPIView.as_view(), name='listar_comentarios'),
    path('eventos/<int:evento_id>/comentarios/crear/', CrearcomentariosAPIView.as_view(), name='crear_comentario'),

    # Documentación Swagger
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
