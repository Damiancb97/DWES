from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROL_CHOICES = [
        ('organizador', 'Organizador'),
        ('participante', 'Participante'),
    ]

    biografia = models.TextField(blank=True, null=True)  # Campo opcional
    rol = models.CharField(max_length=20, choices=ROL_CHOICES)

    def __str__(self):
        return self.username


class Event(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha_hora = models.DateTimeField()
    capacidad_maxima = models.IntegerField()
    imagen_url = models.URLField(blank=True, null=True)  # Campo opcional
    organizador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='eventos_organizados')

    def __str__(self):
        return self.titulo


class Reserva(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservas')
    evento = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='reservas')
    cantidad_entradas = models.IntegerField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')

    def __str__(self):
        return f"Reserva de {self.usuario.username} para {self.evento.titulo}"


class Comentario(models.Model):
    texto = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comentarios')
    evento = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='comentarios')

    def __str__(self):
        return f"Comentario de {self.usuario.username} en {self.evento.titulo}"
