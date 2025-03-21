from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Tjuegos

from django.views.decorators.csrf import csrf_exempt
from .models import Tjuegos, Tcomentarios
import json


def pagina_de_prueba(request):
	return HttpResponse("<h1>Hola caracola</h1>")
	
# Da a ver todos los juegos con todos los campos
def devolver_juegos(request):
	lista = Tjuegos.objects.all() #si pones "()[:7]" se limita a las 7 primeros juegos
	respuesta_final = []
	for fila_sql in lista:
		diccionario = {}
		diccionario['id'] = fila_sql.id
		diccionario['nombre'] = fila_sql.nombre
		diccionario['fecha_lanzamiento'] = fila_sql.fecha_lanzamiento
		diccionario['plataforma'] = fila_sql.plataforma
		respuesta_final.append(diccionario)
	return JsonResponse(respuesta_final, safe=False)

# Da por solicitud el numero de juego solicitado
def devolver_juego_por_id(request, id_solicitado):
	juego = Tjuegos.objects.get(id = id_solicitado)
	comentarios = juego.tcomentarios_set.all()
	lista_comentarios = []
	for fila_comentario_sql in comentarios:
		diccionario = {}
		diccionario['id'] = fila_comentario_sql.id
		diccionario['comentario'] = fila_comentario_sql.comentario
		if fila_comentario_sql.usuario is not None:	
			diccionario['usuario'] = fila_comentario_sql.usuario.id 
		lista_comentarios.append(diccionario)
	resultado = {
		'id': juego.id,
		'nombre': juego.nombre,
		'fecha': juego.fecha_lanzamiento,
		'comentarios': lista_comentarios
	}
	return JsonResponse(resultado, json_dumps_params={'ensure_ascii': False})

@csrf_exempt 
def guardar_comentario(request, juego_id):
	if request.method != 'POST': 
			return None

	json_peticion = json.loads(request.body)
	comentario = Tcomentarios()
	comentario.comentario = json_peticion['nuevo_comentario']
	comentario.juego = Tjuegos.objects.get(id = juego_id)
	comentario.save()
	return JsonResponse({"status": "ok"})