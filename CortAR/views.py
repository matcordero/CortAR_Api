from django.shortcuts import render
from django.contrib.auth import authenticate
from django.http import JsonResponse
import uuid 
from .models import *
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view
from .serializer import *
from rest_framework import viewsets
# Create your views here. 
from django.http import JsonResponse
import cloudinary
import cloudinary.uploader
import cloudinary.api
from django.core.files.uploadedfile import InMemoryUploadedFile


class PublicacionViewSet(viewsets.ModelViewSet):
    queryset = Publicacion.objects.all()
    serializer_class = PublicacionSerializador
    
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializador
    
class ComentarioViewSet(viewsets.ModelViewSet):
    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializador

class ZonaUsuarioViewSet(viewsets.ModelViewSet):
    queryset = ZonaUsuario.objects.all()
    serializer_class = ZonaUsuarioSerializador

def mi_endpoint(request):
    data = {'mensaje': '¡Hola desde mi endpoint!'}
    return JsonResponse(data)

def obtener_usuarios():
    usuarios = Usuario.objects.all()
    print(usuarios)

@api_view(['GET'])
def login(request, mail, contrasena):
    #obtener_usuarios()
    try:
        user = Usuario.objects.get(mail=mail)
    except Usuario.DoesNotExist:
        user = None
    if user is not None and user.contraseña==contrasena:
        # and user.contraseña == make_password(contrasena)
        key_validate = str(uuid.uuid4()).replace("-", "")
        user.key_validate = key_validate
        user.save()

        response_data = {
            'mail': user.mail,
            'nombre': user.nombre,
            'keyValidate': key_validate,
            'tipografia': user.tipografia,
            'tamanoFuente': user.tamano_fuente,
            'fotoPerfil': user.foto_perfil,
            'status_code': 202
        }
        return JsonResponse(response_data, status=202)
    else:
        response_data = {
            'error': 'Usuario o Contraseña Incorrecto'
        }
        return JsonResponse(response_data, status=400)

@api_view(['POST'])
def crear_usuario(request):
    #User = get_user_model()
    mail = request.data.get('mail')
    contrasena = request.data.get('contrasena')
    nombre = request.data.get('nombre')

    if not all([mail, contrasena, nombre]):
        return JsonResponse({"error": "Campos Vacios"}, status=400)

    if Usuario.objects.filter(mail=mail).exists():
        return JsonResponse({"error": "El Usuario ya existe"}, status=400)

    #contrasena_encriptada = make_password(contrasena)
    
    usuario = Usuario(mail=mail, nombre=nombre, contraseña=contrasena)
    usuario.save()

    return JsonResponse({"message": "Usuario Creado con Éxito"}, status=201)
    
@api_view(['GET'])
def getInformationUsuario(request, mail, key):
    if not all([mail, key]):
        return JsonResponse({"error": "Campos Vacios"}, status=400)

    try:
        usuario_actual = Usuario.objects.get(mail=mail)
    except Usuario.DoesNotExist:
       return JsonResponse({"error": "Fallo de Validacion"}, status=400)

    if usuario_actual.key_validate != key:
        return JsonResponse({"error": "Fallo de Validacion"}, status=400)

    response_data = {
            'mail': usuario_actual.mail,
            'nombre': usuario_actual.nombre,
            'keyValidate': usuario_actual.key_validate,
            'tipografia': usuario_actual.tipografia,
            'tamanoFuente': usuario_actual.tamano_fuente,
            'fotoPerfil': usuario_actual.foto_perfil,
            'status_code': 202
        }
    return JsonResponse(response_data, status=201)


@api_view(['POST'])
def editarTipografia(request):
    mail = request.data.get('mail')
    key = request.data.get('key')
    tipografia = request.data.get('tipografia')
    
    if not all([mail, key,tipografia]):
        return JsonResponse({"error": "Campos Vacios"}, status=400)

    try:
        usuario_actual = Usuario.objects.get(mail=mail)
    except Usuario.DoesNotExist:
       return JsonResponse({"error": "Fallo de Validacion"}, status=400)

    if usuario_actual.key_validate != key:
        return JsonResponse({"error": "Fallo de Validacion"}, status=400)

    usuario_actual.tipografia = tipografia
    usuario_actual.save()
    
    return JsonResponse({"message": "Tipografia Cambiada"}, status=200)

@api_view(['POST'])
def editarTamanoLetra(request):
    mail = request.data.get('mail')
    key = request.data.get('key')
    tamanoLetra = request.data.get('tamanoLetra')
    
    if not all([mail, key,tamanoLetra]):
        return JsonResponse({"error": "Campos Vacios"}, status=400)

    try:
        usuario_actual = Usuario.objects.get(mail=mail)
    except Usuario.DoesNotExist:
       return JsonResponse({"error": "Fallo de Validacion"}, status=400)

    if usuario_actual.key_validate != key:
        return JsonResponse({"error": "Fallo de Validacion"}, status=400)

    usuario_actual.tamano_fuente = tamanoLetra
    usuario_actual.save()
    
    return JsonResponse({"message": "Tamaño Letra Cambiado"}, status=200)

@api_view(['POST'])
def editarNombre(request):
    mail = request.data.get('mail')
    key = request.data.get('key')
    nombre = request.data.get('nombre')
    
    if not all([mail, key,nombre]):
        return JsonResponse({"error": "Campos Vacios"}, status=400)

    try:
        usuario_actual = Usuario.objects.get(mail=mail)
    except Usuario.DoesNotExist:
       return JsonResponse({"error": "Fallo de Validacion"}, status=400)

    if usuario_actual.key_validate != key:
        return JsonResponse({"error": "Fallo de Validacion"}, status=400)

    usuario_actual.nombre = nombre
    usuario_actual.save()
    
    return JsonResponse({"message": "Nombre Cambiado"}, status=200)

@api_view(['POST'])
def editarContrasena(request):
    mail = request.data.get('mail')
    key = request.data.get('key')
    contrasenaVieja = request.data.get('contrasenaVieja')
    contrasenaNueva = request.data.get('contrasenaNueva')
    
    if not all([mail, key, contrasenaVieja, contrasenaNueva]):
        return JsonResponse({"error": "Campos Vacios"}, status=400)

    try:
        usuario_actual = Usuario.objects.get(mail=mail)
    except Usuario.DoesNotExist:
       return JsonResponse({"error": "Fallo de Validacion"}, status=400)

    if usuario_actual.key_validate != key and usuario_actual.contraseña != contrasenaVieja:
        return JsonResponse({"error": "Fallo de Validacion"}, status=400)

    usuario_actual.contraseña = contrasenaNueva
    usuario_actual.save()
    
    return JsonResponse({"message": "Contraseña Cambiado"}, status=200)    

@api_view(['POST'])
def editarFotoPerfil(request):
    mail = request.data.get('mail')
    key = request.data.get('key')
    imagen = request.FILES.get('imagen')
    
    if not all([mail, key, imagen]):
        return JsonResponse({"error": "Campos Vacios"}, status=400)

    try:
        usuario_actual = Usuario.objects.get(mail=mail)
    except Usuario.DoesNotExist:
       return JsonResponse({"error": "Fallo de Validacion"}, status=400)

    if usuario_actual.key_validate != key:
        return JsonResponse({"error": "Fallo de Validacion"}, status=400)

    cloudinary_response = cloudinary.uploader.upload(imagen)
    imagen_url = cloudinary_response.get("url")
    
    usuario_actual.foto_perfil = imagen_url
    usuario_actual.save()
    
    return JsonResponse({"message": "Contraseña Cambiado"}, status=200)

#--ZONAS--------------

@api_view(['GET'])
def get_zonas(request):
    zonas = ZonaUsuario.objects.all()
    zonas_data = [{'nombre': zona.nombre, 'descripcion': zona.descripcion} for zona in zonas]
    return JsonResponse(zonas_data, status=200)    

@api_view(['POST'])
def crear_zona(request):
    zona = request.data.get('zona')
    nombre = request.data.get('nombre')

    if not all([zona, nombre]):
        return JsonResponse({"error": "Campos Vacios"}, status=400)

    if ZonaUsuario.objects.filter(zona=zona).exists():
        return JsonResponse({"error": "La zona ya existe"}, status=400)

    #contrasena_encriptada = make_password(contrasena)
    
    zona = ZonaUsuario(zona=zona, nombre=nombre)
    zona.save()

    return JsonResponse({"message": "La Zona fue Creado con Éxito"}, status=201)

@api_view(['POST'])
def crear_publicacion(request):
    mail = request.data.get('mail')
    key = request.data.get('key')
    texto = request.data.get('texto')
    zona = request.data.get('zona')
    
    if not all([mail, key, texto, zona]):
        return JsonResponse({"error": "Campos Vacios"}, status=400)

    try:
        usuario_actual = Usuario.objects.get(mail=mail)
    except Usuario.DoesNotExist:
       return JsonResponse({"error": "Fallo de Validacion"}, status=400)

    if usuario_actual.key_validate != key:
        return JsonResponse({"error": "Fallo de Validacion"}, status=400)
    
    #if not ZonaUsuario.objects.filter(zona=zona).exists:
    #    return JsonResponse({"error": "Zona no Encontrada"}, status=400)
    
    
    publicacion = Publicacion(usuario=usuario_actual,texto=texto,zona=zona)
    publicacion.save()
    
    return JsonResponse({"message": "La Publicacion fue Creado con Éxito"}, status=201)

@api_view(['POST'])
def crear_publicacionFoto(request):
    mail = request.data.get('mail')
    key = request.data.get('key')
    texto = request.data.get('texto')
    zona = request.data.get('zona')
    imagen = request.FILES.get('imagen')  # Obtén la imagen del campo "imagen"
    
    if not all([mail, key, texto, zona, imagen]):
        return JsonResponse({"error": "Campos Vacios"}, status=400)

    try:
        usuario_actual = Usuario.objects.get(mail=mail)
    except Usuario.DoesNotExist:
       return JsonResponse({"error": "Fallo de Validacion"}, status=400)

    if usuario_actual.key_validate != key:
        return JsonResponse({"error": "Fallo de Validacion"}, status=400)
    
    #if not ZonaUsuario.objects.filter(zona=zona).exists:
    #    return JsonResponse({"error": "Zona no Encontrada"}, status=400)
    
    # Sube la imagen a Cloudinary y obtén la URL y el ID de la imagen subida
    cloudinary_response = cloudinary.uploader.upload(imagen)
    imagen_url = cloudinary_response.get("url")
    imagen_id = cloudinary_response.get("public_id")
    
    publicacion = Publicacion(
        usuario=usuario_actual, 
        texto=texto, 
        zona=zona,
        foto=imagen_url,  # Almacena la URL de la imagen
        idFoto=imagen_id     # Almacena el ID de la imagen en Cloudinary
    )
    publicacion.save()
    
    return JsonResponse({"message": "La Publicacion fue Creado con Éxito"}, status=201)

@api_view(['GET'])
def getPublicaciones(request):
    publicaciones = Publicacion.objects.all()
    publicaciones_con_comentarios = []

    for publicacion in publicaciones:
        comentarios = Comentario.objects.filter(publicacion=publicacion)
        comentario_list = []

        for comentario in comentarios:
            comentario_data = {
                "idComentario": comentario.idComentario,
                "usuario": comentario.usuario.nombre,
                "texto": comentario.texto,
                "foto": comentario.foto,
                "fecha": comentario.fecha.strftime("%Y-%m-%d %H:%M:%S"),
                "like": comentario.like,
            }
            comentario_list.append(comentario_data)

        publicacion_data = {
            "idPublicacion": publicacion.idPublicacion,
            "usuario": publicacion.usuario.nombre,
            "texto": publicacion.texto,
            "foto": publicacion.foto,
            "zona": publicacion.zona,
            "fecha": publicacion.fecha.strftime("%Y-%m-%d %H:%M:%S"),
            "like": publicacion.like,
            "comentarios": comentario_list
        }
        publicaciones_con_comentarios.append(publicacion_data)

    return JsonResponse(publicaciones_con_comentarios, safe=False)
    
@api_view(['GET'])
def getPublicacionesPorUsuario(request,mail):
    try:
        usuario_actual = Usuario.objects.get(mail=mail)
    except Usuario.DoesNotExist:
       return JsonResponse({"error": "Usuario no Existe"}, status=400)
    
    publicaciones_con_comentarios = []
    publicaciones = Publicacion.objects.filter(usuario=usuario_actual)
    for publicacion in publicaciones:
        comentarios = Comentario.objects.filter(publicacion=publicacion)
        comentario_list = []

        for comentario in comentarios:
            comentario_data = {
                "idComentario": comentario.idComentario,
                "usuario": comentario.usuario.nombre,
                "texto": comentario.texto,
                "foto": comentario.foto,
                "fecha": comentario.fecha.strftime("%Y-%m-%d %H:%M:%S"),
                "like": comentario.like,
            }
            comentario_list.append(comentario_data)

        publicacion_data = {
            "idPublicacion": publicacion.idPublicacion,
            "usuario": publicacion.usuario.nombre,
            "texto": publicacion.texto,
            "foto": publicacion.foto,
            "zona": publicacion.zona,
            "fecha": publicacion.fecha.strftime("%Y-%m-%d %H:%M:%S"),
            "like": publicacion.like,
            "comentarios": comentario_list
        }
        publicaciones_con_comentarios.append(publicacion_data)

    return JsonResponse(publicaciones_con_comentarios, safe=False)
   
@api_view(['POST'])    
def deletePublicacion(request):
    id = request.data.get('id')
    mail = request.data.get('mail')
    key = request.data.get('key')
    
    if not all([mail, key, id]):
        return JsonResponse({"error": "Campos Vacios"}, status=400)
    
    try:
        publicacion = Publicacion.objects.get(idPublicacion=id)
    except Publicacion.DoesNotExist:
        return JsonResponse({"error": "Publicacion No Existia"}, status=400)
    
    try:
        usuario_actual = Usuario.objects.get(mail=mail)
    except Usuario.DoesNotExist:
       usuario_actual = None
       
    if usuario_actual == None or usuario_actual.key_validate != key or publicacion.usuario != usuario_actual:
        return JsonResponse({"error": "Fallo de Validacion"}, status=400)

    
    publicacion.delete()
    return JsonResponse({"message": "Publicacion Eliminada"}, status=200)

@api_view(['POST'])
def actualizarLikesPublicacion(request):
    id = request.data.get('id')
    likes = request.data.get('likes') 
    mail = request.data.get('mail')
    key = request.data.get('key')
    
    if not all([mail, key, id]):
        return JsonResponse({"error": "Campos Vacios"}, status=400)
    
    try:
        publicacion = Publicacion.objects.get(idPublicacion=id)
    except Publicacion.DoesNotExist:
        return JsonResponse({"error": "Publicacion No Existia"}, status=400)
    
    try:
        usuario_actual = Usuario.objects.get(mail=mail)
    except Usuario.DoesNotExist:
       usuario_actual = None
       
    if usuario_actual == None or usuario_actual.key_validate != key or publicacion.usuario != usuario_actual:
        return JsonResponse({"error": "Fallo de Validacion"}, status=400)
    
    publicacion.like = publicacion.like+likes
    publicacion.save()
    
    return JsonResponse({"message": "Likes Actualizados"}, status=200)

@api_view(['POST'])
def crear_comentario(request):
    mail = request.data.get('mail')
    key = request.data.get('key')
    texto = request.data.get('texto')
    idPublicacion = request.data.get('idPublicacion')
    
    if not all([mail, key, texto, idPublicacion]):
        return JsonResponse({"error": "Campos Vacios"}, status=400)

    try:
        usuario_actual = Usuario.objects.get(mail=mail)
    except Usuario.DoesNotExist:
       return JsonResponse({"error": "Fallo de Validacion"}, status=400)

    if usuario_actual.key_validate != key:
        return JsonResponse({"error": "Fallo de Validacion"}, status=400)
    
    #if not ZonaUsuario.objects.filter(zona=zona).exists:
    #    return JsonResponse({"error": "Zona no Encontrada"}, status=400)
    
    try:
        publicacion = Publicacion.objects.get(idPublicacion=idPublicacion)
    except Publicacion.DoesNotExist:
       return JsonResponse({"error": "No se encontro la Publicacion"}, status=400)
    
    comentario = Comentario(publicacion=publicacion,texto=texto,Usuario=usuario_actual)
    comentario.save()
    
    return JsonResponse({"message": "El Comentario fue Creado con Éxito"}, status=201)

@api_view(['POST'])
def crear_comentarioFoto(request):
    mail = request.data.get('mail')
    key = request.data.get('key')
    texto = request.data.get('texto')
    idPublicacion = request.data.get('idPublicacion')
    imagen = request.FILES.get('imagen')
    
    if not all([mail, key, texto, idPublicacion, imagen]):
        return JsonResponse({"error": "Campos Vacios"}, status=400)

    try:
        usuario_actual = Usuario.objects.get(mail=mail)
    except Usuario.DoesNotExist:
       return JsonResponse({"error": "Fallo de Validacion"}, status=400)

    if usuario_actual.key_validate != key:
        return JsonResponse({"error": "Fallo de Validacion"}, status=400)
    
    #if not ZonaUsuario.objects.filter(zona=zona).exists:
    #    return JsonResponse({"error": "Zona no Encontrada"}, status=400)
    
    try:
        publicacion = Publicacion.objects.get(idPublicacion=idPublicacion)
    except Publicacion.DoesNotExist:
       return JsonResponse({"error": "No se encontro la Publicacion"}, status=400)
    
    cloudinary_response = cloudinary.uploader.upload(imagen)
    imagen_url = cloudinary_response.get("url")
    imagen_id = cloudinary_response.get("public_id")
    
    comentario = Comentario(publicacion=publicacion,texto=texto,Usuario=usuario_actual,foto = imagen_url, idFoto = imagen_id)
    comentario.save()
    
    return JsonResponse({"message": "El Comentario fue Creado con Éxito"}, status=201)

@api_view(['POST'])
def actualizarLikesPublicacion(request):
    id = request.data.get('id')
    likes = request.data.get('likes') 
    mail = request.data.get('mail')
    key = request.data.get('key')
    
    if not all([mail, key, id]):
        return JsonResponse({"error": "Campos Vacios"}, status=400)
    
    try:
        publicacion = Publicacion.objects.get(idPublicacion=id)
    except Publicacion.DoesNotExist:
        return JsonResponse({"error": "Publicacion No Existia"}, status=400)
    
    try:
        usuario_actual = Usuario.objects.get(mail=mail)
    except Usuario.DoesNotExist:
       usuario_actual = None
       
    if usuario_actual == None or usuario_actual.key_validate != key or publicacion.usuario != usuario_actual:
        return JsonResponse({"error": "Fallo de Validacion"}, status=400)
    
    publicacion.like = publicacion.like+likes
    publicacion.save()
    
    return JsonResponse({"message": "Likes Actualizados"}, status=200)@api_view(['POST'])

@api_view(['POST'])
def actualizarLikesComentarios(request):
    id = request.data.get('id')
    likes = request.data.get('likes') 
    mail = request.data.get('mail')
    key = request.data.get('key')
    
    if not all([mail, key, id]):
        return JsonResponse({"error": "Campos Vacios"}, status=400)
    
    try:
        comentario = Comentario.objects.get(idComentario=id)
    except Comentario.DoesNotExist:
        return JsonResponse({"error": "Comentario No Existia"}, status=400)
    
    try:
        usuario_actual = Usuario.objects.get(mail=mail)
    except Usuario.DoesNotExist:
       usuario_actual = None
       
    if usuario_actual == None or usuario_actual.key_validate != key or comentario.usuario != usuario_actual:
        return JsonResponse({"error": "Fallo de Validacion"}, status=400)
    
    comentario.like = comentario.like+likes
    comentario.save()
    
    return JsonResponse({"message": "Likes Actualizados"}, status=200)

@api_view(['POST'])    
def deleteComentario(request):
    id = request.data.get('id')
    mail = request.data.get('mail')
    key = request.data.get('key')
    
    if not all([mail, key, id]):
        return JsonResponse({"error": "Campos Vacios"}, status=400)
    
    try:
        comentario = Comentario.objects.get(idComentario=id)
    except Comentario.DoesNotExist:
        return JsonResponse({"error": "Comentario No Existia"}, status=400)
    
    try:
        usuario_actual = Usuario.objects.get(mail=mail)
    except Usuario.DoesNotExist:
       usuario_actual = None
       
    if usuario_actual == None or usuario_actual.key_validate != key or comentario.usuario != usuario_actual:
        return JsonResponse({"error": "Fallo de Validacion"}, status=400)

    
    comentario.delete()
    return JsonResponse({"message": "Comentario Eliminado"}, status=200)