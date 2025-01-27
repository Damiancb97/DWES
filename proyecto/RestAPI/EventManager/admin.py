from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Event, Reserva, Comentario


# Personalización de la tabla de usuarios en el administrador
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Campos visibles en la lista
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'rol')
    # Filtros laterales
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'rol')
    # Campos para la barra de búsqueda
    search_fields = ('username', 'email', 'first_name', 'last_name')


# Personalización de la tabla de eventos en el administrador
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha_hora', 'capacidad_maxima', 'organizador')  # Columnas visibles
    list_filter = ('fecha_hora', 'organizador')  # Filtros laterales
    search_fields = ('titulo', 'descripcion', 'organizador__username')  # Campos para la barra de búsqueda
    ordering = ('-fecha_hora',)  # Ordenar por fecha (más recientes primero)


# Personalización de reservas en el administrador
@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'evento', 'cantidad_entradas', 'estado')
    list_filter = ('estado', 'evento')
    search_fields = ('usuario__username', 'evento__titulo')


# Personalización de comentarios en el administrador
@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'evento', 'fecha_creacion', 'texto')
    list_filter = ('fecha_creacion',)
    search_fields = ('usuario__username', 'evento__titulo', 'texto')
