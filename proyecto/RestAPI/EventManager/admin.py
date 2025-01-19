from django.contrib import admin
from .models import User, Event, Reserva, Comentario


# Personalización de la tabla de eventos en el administrador
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha_hora', 'capacidad_maxima', 'organizador', 'created_at')  # Columnas visibles
    list_filter = ('fecha_hora', 'organizador')  # Filtros laterales
    search_fields = ('titulo', 'descripcion', 'organizador__nombre')  # Campos para la barra de búsqueda
    ordering = ('-fecha_hora',)  # Ordenar por fecha (más recientes primero)


# Registro de otros modelos con configuraciones básicas
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'correo_electronico', 'rol', 'created_at')
    list_filter = ('rol', 'created_at')
    search_fields = ('nombre', 'correo_electronico')


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'evento', 'cantidad_entradas', 'estado', 'created_at')
    list_filter = ('estado', 'evento')
    search_fields = ('usuario__nombre', 'evento__titulo')


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'evento', 'fecha_creacion', 'texto')
    list_filter = ('fecha_creacion',)
    search_fields = ('usuario__nombre', 'evento__titulo', 'texto')

