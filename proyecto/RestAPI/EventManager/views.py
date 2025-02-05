from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from .models import Event, User, Reserva, Comentario
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_datetime
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
import json


# Obtener eventos con filtros, ordenados y paginados
@csrf_exempt
def listar_eventos(request):
    # Obtener parámetros de búsqueda, ordenación y paginación
    titulo = request.GET.get("titulo", "")  # Filtrar por título
    fecha_hora = request.GET.get("fecha", None)  # Filtrar por fecha específica
    orden = request.GET.get("orden", "fecha_hora")  # Ordenar por fecha_hora por defecto
    limite = int(request.GET.get("limite", 5))  # Número de resultados por página (5 por defecto)
    pagina = int(request.GET.get("pagina", 1))  # Página actual (1 por defecto)

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
        return JsonResponse({"error": str(e)}, status=400)  # Manejar errores de paginación

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

    return JsonResponse(data, safe=False)

# Crear un nuevo evento (solo organizadores)
@csrf_exempt
def crear_evento(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido. Usa POST.'}, status=405)

    # Obtener el organizador desde la URL
    organizador_username = request.GET.get('organizador')
    if not organizador_username:
        return JsonResponse({'error': 'Falta el parámetro "organizador" en la URL.'}, status=400)

    try:
        # Buscar al usuario en la base de datos
        organizador = User.objects.get(username=organizador_username)
    except User.DoesNotExist:
        return JsonResponse({'error': f'No existe un usuario con el nombre de usuario "{organizador_username}".'}, status=404)

    # Verificar si el usuario es organizador
    if organizador.rol != 'organizador':
        return JsonResponse({'error': f'El usuario "{organizador_username}" no es un organizador.'}, status=403)

    try:
        # Leer los datos enviados en el cuerpo de la solicitud
        data = json.loads(request.body)

        # Crear el evento
        evento = Event.objects.create(
            titulo=data.get('titulo'),
            descripcion=data.get('descripcion'),
            fecha_hora=parse_datetime(data.get('fecha_hora')),
            capacidad_maxima=data.get('capacidad_maxima'),
            imagen_url=data.get('imagen_url', ''),
            organizador=organizador
        )

        return JsonResponse({'message': 'Evento creado con éxito', 'evento_id': evento.id}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'El cuerpo de la solicitud debe ser un JSON válido.'}, status=400)
    except KeyError as e:
        return JsonResponse({'error': f'Falta el campo obligatorio: {e}.'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Error al crear el evento: {str(e)}.'}, status=500)


# Actualizar evento
@csrf_exempt
@require_http_methods(["PUT", "PATCH"])
def actualizar_evento(request, evento_id):

    # Obtener el organizador desde la URL
    organizador_username = request.GET.get('organizador')
    if not organizador_username:
        return JsonResponse({'error': 'Falta el parámetro "organizador" en la URL.'}, status=400)

    try:
        # Buscar al usuario en la base de datos
        organizador = User.objects.get(username=organizador_username)
    except User.DoesNotExist:
        return JsonResponse({'error': f'No existe un usuario con el nombre de usuario "{organizador_username}".'},
                            status=404)

    # Verificar si el usuario es organizador
    if organizador.rol != 'organizador':
        return JsonResponse({'error': f'El usuario "{organizador_username}" no es un organizador.'}, status=403)

# Buscar el evento
    try:
        evento = Event.objects.get(id=evento_id, organizador=organizador)
    except Event.DoesNotExist:
        return JsonResponse({'error': 'Evento no encontrado o no tienes permisos.'}, status=404)

    try:
        data = json.loads(request.body)


        if request.method == 'PUT':
            evento.titulo = data.get('titulo', evento.titulo)
            evento.descripcion = data.get('descripcion', evento.descripcion)
            evento.fecha_hora = parse_datetime(data.get('fecha_hora')) or evento.fecha_hora
            evento.capacidad_maxima = data.get('capacidad_maxima', evento.capacidad_maxima)
            evento.imagen_url = data.get('imagen_url', evento.imagen_url)
        elif request.method == 'PATCH':
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

        return JsonResponse({'message': 'Evento actualizado correctamente'}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'El cuerpo de la solicitud debe ser un JSON válido.'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Error al actualizar el evento: {str(e)}.'}, status=500)


# Eliminar Eventos (solo organizadores)
@csrf_exempt
@require_http_methods(["DELETE"])
def eliminar_evento(request, evento_id):
    # Obtener el organizador desde la URL
    organizador_username = request.GET.get('organizador')
    if not organizador_username:
        return JsonResponse({'error': 'Falta el parámetro "organizador" en la URL.'}, status=400)

    try:
        # Buscar al usuario en la base de datos
        organizador = User.objects.get(username=organizador_username)
    except User.DoesNotExist:
        return JsonResponse({'error': f'No existe un usuario con el nombre de usuario "{organizador_username}".'},
                            status=404)

    # Verificar si el usuario es organizador
    if organizador.rol != 'organizador':
        return JsonResponse({'error': f'El usuario "{organizador_username}" no es un organizador.'}, status=403)

    # Buscar el evento, asegurando que pertenezca al organizador
    evento = get_object_or_404(Event, id=evento_id, organizador=organizador)

    # Eliminar el evento
    evento.delete()

    return JsonResponse({'message': 'Evento eliminado correctamente'}, status=200)


# Listar reservas de un usuario
@csrf_exempt
@require_http_methods(["GET"])
def listar_reservas(request, username):
    usuario = get_object_or_404(User, username=username)
    reservas = Reserva.objects.filter(usuario=usuario).select_related("evento").values(
        "id", "evento__titulo", "cantidad_entradas", "estado"
    )
    return JsonResponse({"reservas": list(reservas)}, status=200)


# Postear una nueva reserva
@csrf_exempt
@require_http_methods(["POST"])
def crear_reserva(request):
    try:
        data = json.loads(request.body)
        # Extraer datos
        usuario_username = data.get('usuario')
        evento_id = data.get('evento_id')
        cantidad_entradas = data.get('cantidad_entradas')

        # Verificar que los datos son válidos
        if not usuario_username or not evento_id or not cantidad_entradas:
            return JsonResponse({"error": "Faltan datos obligatorios."}, status=400)

        # Buscar usuario y evento
        usuario = User.objects.get(username=usuario_username)
        evento = Event.objects.prefetch_related("reservas").get(id=evento_id)

        # Crear la reserva
        reserva = Reserva.objects.create(
            usuario=usuario,
            evento=evento,
            cantidad_entradas=cantidad_entradas
        )

        return JsonResponse({"mensaje": "Reserva creada con éxito", "reserva_id": reserva.id}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({"error": "El cuerpo de la solicitud debe ser un JSON válido."}, status=400)
    except User.DoesNotExist:
        return JsonResponse({"error": "El usuario no existe."}, status=404)
    except Event.DoesNotExist:
        return JsonResponse({"error": "El evento no existe."}, status=404)
    except Exception as e:
        return JsonResponse({"error": f"Error al crear la reserva: {str(e)}"}, status=500)


# Actualizar reservas
@csrf_exempt
@require_http_methods(["PUT", "PATCH"])
def actualizar_reserva(request, reserva_id):

    organizador_username = request.GET.get('organizador')
    if not organizador_username:
        return JsonResponse({'error': 'Falta el parámetro "organizador" en la URL.'}, status=400)

    # Verificar si el organizador existe
    try:
        organizador = User.objects.get(username=organizador_username)
    except User.DoesNotExist:
        return JsonResponse({'error': f'No existe un usuario con el nombre de usuario "{organizador_username}".'}, status=404)


    # Verificar si el usuario es realmente un organizador
    if organizador.rol != 'organizador':
        return JsonResponse({'error': f'El usuario "{organizador_username}" no es un organizador.'}, status=403)

    # Obtener la reserva
    reserva = get_object_or_404(Reserva.objects.select_related("evento"), id=reserva_id)

    # Verificar si el organizador tiene permiso sobre la reserva
    if reserva.evento.organizador != organizador:
        return JsonResponse({'error': 'No tienes permiso para actualizar esta reserva.'}, status=403)

    try:
        data = json.loads(request.body)
        actualizacion = {}

        # Actualizar el estado de la reserva (si se envía en la solicitud)
        if "estado" in data:
            reserva.estado = data["estado"]
            actualizacion["estado"] = data["estado"]

        # Actualizar la cantidad de entradas (si se envía en la solicitud)
        if "cantidad_entradas" in data:
            nueva_cantidad = int(data["cantidad_entradas"])

            # Calcular el total reservado sin contar la reserva actual
            total_reservado = sum(r.cantidad_entradas for r in reserva.evento.reservas.all()) - reserva.cantidad_entradas

            # Verificar que haya espacio suficiente
            if total_reservado + nueva_cantidad > reserva.evento.capacidad_maxima:
                return JsonResponse({'error': 'No hay suficientes entradas disponibles.'}, status=400)

            reserva.cantidad_entradas = nueva_cantidad
            actualizacion["cantidad_entradas"] = nueva_cantidad

        # Guardar cambios si hubo actualizaciones
        if actualizacion:
            reserva.save()
            return JsonResponse({'message': 'Reserva actualizada correctamente', 'actualizacion': actualizacion}, status=200)

        return JsonResponse({'error': 'No se proporcionaron cambios válidos.'}, status=400)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'El cuerpo de la solicitud debe ser un JSON válido.'}, status=400)
    except ValueError:
        return JsonResponse({'error': 'La cantidad de entradas debe ser un número entero válido.'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Error al actualizar la reserva: {str(e)}.'}, status=500)


# Eliminar Reserva
@csrf_exempt
@require_http_methods(["DELETE"])
def cancelar_reserva(request, reserva_id):
    usuario_username = request.GET.get("usuario")

    if not usuario_username:
        return JsonResponse({"error": "Falta el parámetro 'usuario' en la URL."}, status=400)

    usuario = get_object_or_404(User, username=usuario_username)
    reserva = get_object_or_404(Reserva, id=reserva_id)

    # Solo el usuario que hizo la reserva puede cancelarla
    if reserva.usuario != usuario:
        return JsonResponse({"error": "No tienes permiso para cancelar esta reserva."}, status=403)

    reserva.delete()

    return JsonResponse({"message": "Reserva cancelada correctamente"}, status=200)


# Listar comentarios de eventos
@require_http_methods(["GET"])
def listar_comentarios(request, evento_id):

    evento = get_object_or_404(Event, id=evento_id)
    comentarios = evento.comentarios.select_related("usuario").values("usuario__username", "texto", "fecha_creacion")

    return JsonResponse({'comentarios': list(comentarios)}, status=200)


# Postear comentario solo a usuarios autenticados
@csrf_exempt
@require_http_methods(["POST"])
def crear_comentario(request, evento_id):
    try:
        data = json.loads(request.body)

        usuario_username = data.get("usuario")
        texto = data.get("texto")

        if not usuario_username or not texto:
            return JsonResponse({'error': 'Faltan datos obligatorios (usuario, texto).'}, status=400)

        usuario = get_object_or_404(User, username=usuario_username)
        evento = get_object_or_404(Event, id=evento_id)

        comentario = Comentario.objects.create(
            evento=evento,
            usuario=usuario,
            texto=texto
        )

        return JsonResponse({'message': 'Comentario creado con éxito', 'comentario_id': comentario.id}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'El cuerpo de la solicitud debe ser un JSON válido.'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Error al crear el comentario: {str(e)}'}, status=500)


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