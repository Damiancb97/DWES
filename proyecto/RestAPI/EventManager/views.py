from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from .models import Event, User
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_datetime
from django.core.paginator import Paginator
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
    eventos = Event.objects.filter(titulo__icontains=titulo)
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


# Actualizar PUT y PATCH
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
