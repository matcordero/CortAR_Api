from django.urls import path,include
from rest_framework import routers

from .views import *
router = routers.DefaultRouter()
router.register(r'Publicacion',PublicacionViewSet)
router.register(r'Usuario',UsuarioViewSet)
router.register(r'Comentario',ComentarioViewSet)
router.register(r'ZonaUsuario',ZonaUsuarioViewSet)

urlpatterns = [
    path('',include(router.urls)),
    path('login/<str:mail>/<str:contrasena>', login, name='login'),
    path('GetInformationUsuario/<str:mail>/<str:key>', getInformationUsuario, name='GetInformationUsuario'),
    path('crear_usuario', crear_usuario, name='crear_usuario'),
    path('editarTipografia', editarTipografia, name='editarTipografia'),
    path('editarTamanoLetra', editarTamanoLetra, name='editarTamanoLetra'),
    path('editarNombre', editarNombre, name='editarNombre'),
    path('editarContrasena', editarContrasena, name='editarContrasena'),
    path('editarFotoPerfil', editarFotoPerfil, name='editarFotoPerfil'),
    
    path('crear_Zona', crear_zona, name='crear_zona'),
    path('getZonas', get_zonas, name='getZonas'),
    
    
    path('crear_publicacion', crear_publicacion, name='crear_publicacion'),
    path('crear_publicacionFoto', crear_publicacionFoto, name='crear_publicacionFoto'),
    path('getPublicaciones', getPublicaciones, name='getPublicaciones'),
    path('getPublicacionesPorUsuario/<str:mail>', getPublicacionesPorUsuario, name='getPublicacionesPorUsuario'),
    path('deletePublicacion', deletePublicacion, name='deletePublicacion'),
    path('actualizarLikesPublicacion', actualizarLikesPublicacion, name='actualizarLikesPublicacion'),
    
    path('crear_comentario', crear_comentario, name='crear_comentario'),
    path('crear_comentarioFoto', crear_comentarioFoto, name='crear_comentarioFoto'),
    path('actualizarLikesComentario', actualizarLikesComentarios, name='actualizarLikesComentarios'),
    path('deleteComentario', deleteComentario, name='deleteComentario'),
]


