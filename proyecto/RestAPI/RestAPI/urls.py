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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('eventos', views.listar_eventos, name='listar_eventos'),
    path('eventos/crear', views.crear_evento, name='crear_evento'),
    path('eventos/<int:evento_id>/actualizar', views.actualizar_evento, name='actualizar_evento'),
    path('eventos/<int:evento_id>/eliminar', views.eliminar_evento, name='eliminar_evento'),
    path('reservas/<str:username>', views.listar_reservas, name='listar_reservas'),
    path('reservas/crear/', views.crear_reserva, name='crear_reserva'),
    path('reservas/<int:reserva_id>/actualizar', views.actualizar_reserva, name='actualizar_reserva'),
    path('reservas/<int:reserva_id>/cancelar', views.cancelar_reserva, name='cancelar_reserva'),
    path('eventos/<int:evento_id>/comentarios', views.listar_comentarios, name='listar_comentarios'),
    path('eventos/<int:evento_id>/comentarios/crear', views.crear_comentario, name='crear_comentario'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
]
