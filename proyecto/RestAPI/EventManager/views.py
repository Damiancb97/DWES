from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from .models import Event, User, Reserva, Comentario
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_datetime
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
import json

#IMPLEMENTACION
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from .models import Event
from rest_framework.permissions import AllowAny  # Permite acceso a todos los usuarios



# Obtener eventos con filtros, ordenados y paginados
class ListarEventosAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        # Obtener parámetros de búsqueda, ordenación y paginación
        titulo = request.query_params.get("titulo", "")  # Filtrar por título
        fecha_hora = request.query_params.get("fecha", None)  # Filtrar por fecha específica
        orden = request.query_params.get("orden", "fecha_hora")  # Ordenar por defecto
        limite = int(request.query_params.get("limite", 5))  # Resultados por página
        pagina = int(request.query_params.get("pagina", 1))  # Página actual

        # Filtrar y ordenar eventos
        eventos = Event.objects.filter(titulo__icontains=titulo).select_related("organizador")
        if fecha_hora:
            eventos = eventos.filter(fecha_hora__date=fecha_hora)  # Filtrar por fecha exacta
        eventos = eventos.order_by(orden)  # Ordenar por campo especificado

        # Paginación
        paginator = Paginator(eventos, limite)
        try:
            eventos_pagina = paginator.page(pagina)
        except Exception as e:
            return Response({"error": str(e)}, status=400)  # Manejar errores de paginación

        # Crear respuesta con datos paginados
        data = {
            "count": paginator.count,  # Número total de eventos
            "total_pages": paginator.num_pages,  # Número total de páginas
            "current_page": pagina,  # Página actual
            "next": pagina + 1 if eventos_pagina.has_next() else None,  # Página siguiente
            "previous": pagina - 1 if eventos_pagina.has_previous() else None,  # Página anterior
            "results": [
                {
                    "id": e.id,
                    "titulo": e.titulo,
                    "descripcion": e.descripcion,
                    "fecha_hora": e.fecha_hora,
                    "capacidad_maxima": e.capacidad_maxima,
                    "imagen_url": e.imagen_url,
                    "organizador": {
                        "id": e.organizador.id,
                        "nombre": e.organizador.username,
                        "correo_electronico": e.organizador.email
                    }
                }
                for e in eventos_pagina
            ]  # Resultados actuales
        }

        return Response(data)



# Crear un nuevo evento (solo organizadores)
class CrearEventoAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados pueden acceder

    def post(self, request):
        try:
            # Verificar si el usuario es organizador
            if request.user.rol != 'organizador':
                return Response({'error': 'No tienes permisos para crear eventos.'}, status=403)

            # Obtener datos del request
            data = request.data
            evento = Event.objects.create(
                titulo=data.get('titulo'),
                descripcion=data.get('descripcion'),
                fecha_hora=parse_datetime(data.get('fecha_hora')),
                capacidad_maxima=data.get('capacidad_maxima'),
                imagen_url=data.get('imagen_url', ''),
                organizador=request.user
            )

            return Response({'message': 'Evento creado con éxito', 'evento_id': evento.id}, status=201)

        except KeyError as e:
            return Response({'error': f'Falta el campo obligatorio: {e}.'}, status=400)
        except Exception as e:
            return Response({'error': f'Error al crear el evento: {str(e)}.'}, status=500)



# Actualizar evento (solo organizadores)
class ActualizarEventoAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados pueden acceder

    def put(self, request, evento_id):
        return self.actualizar_evento(request, evento_id, metodo='PUT')

    def patch(self, request, evento_id):
        return self.actualizar_evento(request, evento_id, metodo='PATCH')

    def actualizar_evento(self, request, evento_id, metodo):
        # Verificar si el usuario autenticado es organizador
        if request.user.rol != 'organizador':
            return Response({'error': 'No tienes permisos para actualizar eventos.'}, status=403)

        # Buscar el evento del usuario autenticado
        try:
            evento = Event.objects.get(id=evento_id, organizador=request.user)
        except Event.DoesNotExist:
            return Response({'error': 'Evento no encontrado o no tienes permisos.'}, status=404)

        try:
            data = request.data  # DRF maneja automáticamente JSON

            if metodo == 'PUT':
                evento.titulo = data.get('titulo', evento.titulo)
                evento.descripcion = data.get('descripcion', evento.descripcion)
                evento.fecha_hora = parse_datetime(data.get('fecha_hora')) or evento.fecha_hora
                evento.capacidad_maxima = data.get('capacidad_maxima', evento.capacidad_maxima)
                evento.imagen_url = data.get('imagen_url', evento.imagen_url)
            elif metodo == 'PATCH':
                if 'titulo' in data:
                    evento.titulo = data['titulo']
                if 'descripcion' in data:
                    evento.descripcion = data['descripcion']
                if 'fecha_hora' in data:
                    evento.fecha_hora = parse_datetime(data['fecha_hora']) or evento.fecha_hora
                if 'capacidad_maxima' in data:
                    evento.capacidad_maxima = data['capacidad_maxima']
                if 'imagen_url' in data:
                    evento.imagen_url = data['imagen_url']

            evento.save()
            return Response({'message': 'Evento actualizado correctamente'}, status=200)

        except json.JSONDecodeError:
            return Response({'error': 'El cuerpo de la solicitud debe ser un JSON válido.'}, status=400)
        except Exception as e:
            return Response({'error': f'Error al actualizar el evento: {str(e)}.'}, status=500)



# Eliminar Eventos (solo organizadores)
class EliminarEventoAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, evento_id):
        # Verificar si el usuario autenticado es organizador
        if request.user.rol != 'organizador':
            return Response({'error': 'No tienes permisos para eliminar eventos.'}, status=403)

        # Buscar el evento asegurando que pertenece al usuario autenticado
        evento = get_object_or_404(Event, id=evento_id, organizador=request.user)

        # Eliminar el evento
        evento.delete()

        return Response({'message': 'Evento eliminado correctamente'}, status=200)



# Listar reservas de un usuario
class ListarReservasAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        reservas = Reserva.objects.filter(usuario=request.user).select_related("evento").values(
            "id", "evento__titulo", "cantidad_entradas", "estado"
        )
        return Response({"reservas": list(reservas)}, status=200)



# Postear una nueva reserva
class CrearRervaAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Extraer datos del cuerpo de la solicitud (DRF maneja esto automáticamente)
            usuario = request.user  # Usar el usuario autenticado
            evento_id = request.data.get('evento_id')
            cantidad_entradas = request.data.get('cantidad_entradas')

            # Verificar que los datos son válidos
            if not evento_id or not cantidad_entradas:
                return Response({"error": "Faltan datos obligatorios."}, status=400)

            # Buscar el evento
            evento = get_object_or_404(Event, id=evento_id)

            # Verificar que el evento no tenga una reserva previa del mismo usuario
            if Reserva.objects.filter(usuario=usuario, evento=evento).exists():
                return Response({"error": "Ya has realizado una reserva para este evento."}, status=400)

            # Crear la reserva
            reserva = Reserva.objects.create(
                usuario=usuario,
                evento=evento,
                cantidad_entradas=cantidad_entradas
            )

            return Response({"mensaje": "Reserva creada con éxito", "reserva_id": reserva.id}, status=201)

        except Event.DoesNotExist:
            return Response({"error": "El evento no existe."}, status=404)
        except Exception as e:
            return Response({"error": f"Error al crear la reserva: {str(e)}"}, status=500)



# Actualizar reservas (solo organizadores)
class ActualizarReservaAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, reserva_id):
        # Obtener al usuario autenticado
        organizador = request.user

        # Verificar si el usuario es organizador
        if organizador.rol != 'organizador':
            return Response({'error': f'El usuario "{organizador.username}" no es un organizador.'}, status=403)

        # Obtener la reserva
        reserva = get_object_or_404(Reserva.objects.select_related("evento"), id=reserva_id)

        # Verificar si el organizador tiene permiso sobre la reserva
        if reserva.evento.organizador != organizador:
            return Response({'error': 'No tienes permiso para actualizar esta reserva.'}, status=403)

        # Extraer datos de la solicitud
        data = request.data
        actualizacion = {}

        # Actualizar el estado de la reserva (si se envía en la solicitud)
        if "estado" in data:
            reserva.estado = data["estado"]
            actualizacion["estado"] = data["estado"]

        # Actualizar la cantidad de entradas (si se envía en la solicitud)
        if "cantidad_entradas" in data:
            nueva_cantidad = int(data["cantidad_entradas"])

            # Calcular el total reservado sin contar la reserva actual
            total_reservado = sum(
                r.cantidad_entradas for r in reserva.evento.reservas.all()) - reserva.cantidad_entradas

            # Verificar que haya espacio suficiente
            if total_reservado + nueva_cantidad > reserva.evento.capacidad_maxima:
                return Response({'error': 'No hay suficientes entradas disponibles.'}, status=400)

            reserva.cantidad_entradas = nueva_cantidad
            actualizacion["cantidad_entradas"] = nueva_cantidad

        # Guardar cambios si hubo actualizaciones
        if actualizacion:
            reserva.save()
            return Response({'message': 'Reserva actualizada correctamente', 'actualizacion': actualizacion},
                            status=200)

        return Response({'error': 'No se proporcionaron cambios válidos.'}, status=400)

    def patch(self, request, reserva_id):
        # Similar a put, pero actualizando parcialmente solo los campos que se envíen
        return self.put(request, reserva_id)  # Usamos el mismo código que en PUT para simplificar



# Eliminar Reserva (solo los participantes para su reserva)
class CancelarReservaAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, reserva_id):
        usuario = request.user  # Usuario autenticado

        # Verificar que el usuario es un participante (no organizador)
        if usuario.rol != "participante":
            return Response({"error": "Solo los participantes pueden cancelar sus reservas."}, status=403)

        # Buscar la reserva
        reserva = get_object_or_404(Reserva, id=reserva_id)

        # Verificar que el usuario autenticado sea el dueño de la reserva
        if reserva.usuario != usuario:
            return Response({"error": "No tienes permiso para cancelar esta reserva."}, status=403)

        # Cancelar (eliminar) la reserva
        reserva.delete()

        return Response({"message": "Reserva cancelada correctamente"}, status=200)



# Listar comentarios de eventos
class ListarComentariosAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, evento_id):
        evento = get_object_or_404(Event, id=evento_id)

        # Obtiene los comentarios relacionados con el evento y los usuarios que los hicieron
        comentarios = evento.comentarios.select_related("usuario").values(
            "usuario__username", "texto", "fecha_creacion"
        )

        return Response({"comentarios": list(comentarios)}, status=200)



# Postear comentario solo a usuarios autenticados
class CrearcomentariosAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, evento_id):
        try:
            data = request.data  # DRF ya maneja JSON automáticamente

            texto = data.get("texto")
            if not texto:
                return Response({'error': 'El campo "texto" es obligatorio.'}, status=400)

            evento = get_object_or_404(Event, id=evento_id)

            # Usamos request.user en lugar de recibirlo en el JSON
            comentario = Comentario.objects.create(
                evento=evento,
                usuario=request.user,
                texto=texto
            )

            return Response(
                {'message': 'Comentario creado con éxito', 'comentario_id': comentario.id},
                status=201
            )

        except Exception as e:
            return Response({'error': f'Error al crear el comentario: {str(e)}'}, status=500)


# Register de un usuario
User = get_user_model()  # Usar el modelo de usuario personalizado
@csrf_exempt
@require_http_methods(["POST"])
def register(request):
    try:
        data = json.loads(request.body)

        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        rol = data.get("rol", "participante")  # Asignar rol predeterminado o el proporcionado

        # Validaciones
        if not username or not email or not password:
            return JsonResponse({"error": "Todos los campos son obligatorios."}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "El nombre de usuario ya está en uso."}, status=400)

        if rol not in dict(User.ROL_CHOICES).keys():
            return JsonResponse({"error": "Rol inválido."}, status=400)

        # Crear usuario
        user = User.objects.create_user(username=username, email=email, password=password, rol=rol)

        return JsonResponse({"message": "Usuario registrado con éxito", "user_id": user.id}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({"error": "El cuerpo de la solicitud debe ser un JSON válido."}, status=400)
    except Exception as e:
        return JsonResponse({"error": f"Error al registrar usuario: {str(e)}"}, status=500)


# Login de usuario
@csrf_exempt
@require_http_methods(["POST"])
def login(request):
    try:
        data = json.loads(request.body)

        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return JsonResponse({"error": "Todos los campos son obligatorios."}, status=400)

        # Autenticar al usuario
        user = authenticate(username=username, password=password)

        if user is None:
            return JsonResponse({"error": "Credenciales inválidas."}, status=401)

        return JsonResponse({"message": "Inicio de sesión exitoso", "user_id": user.id, "rol": user.rol}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"error": "El cuerpo de la solicitud debe ser un JSON válido."}, status=400)
    except Exception as e:
        return JsonResponse({"error": f"Error al iniciar sesión: {str(e)}"}, status=500)