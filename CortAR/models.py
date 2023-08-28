from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.
class Usuario(models.Model):
    mail = models.EmailField(primary_key=True)
    contraseña = models.TextField()
    nombre = models.CharField(max_length=100)
    foto_perfil = models.TextField()
    key_validate = models.CharField(max_length=100, null=True, blank=True)
    tipografia = models.CharField(max_length=100)
    tamano_fuente = models.FloatField(default=12.0)
    fechaNacimiento = models.DateTimeField(default=timezone.now)
    
    def dar_LikePublicacion(self, publicacion):
        like, created = LikePublicacion.objects.get_or_create(
            usuario = self,
            publicacion = publicacion,
        )
        if created:
            like.save()
        else:
            like.delete()
        
    def get_LikePublicacion(self,publicacion):
        likePublicacion = LikePublicacion.objects.filter(usuario=self,publicacion=publicacion)
        if likePublicacion:
            return True
        return False
    
    def get_LikeComentario(self,comentario):
        likeComentario = LikeComentario.objects.filter(usuario=self,comentario=comentario)
        if likeComentario:
            return True
        return False
    
    def dar_LikeComentario(self, comentario):
        like, created = LikeComentario.objects.get_or_create(
            usuario = self,
            comentario = comentario,
        )
        if created:
            like.save()
        else:
            like.delete()
    
    
class Publicacion(models.Model):
    idPublicacion = models.AutoField(primary_key=True)
    usuario = models.ForeignKey('Usuario',on_delete=models.DO_NOTHING)
    titulo = models.TextField(default="")
    texto = models.TextField()
    foto = models.TextField()
    zona = models.TextField()
    sugerencia = models.TextField(default="")
    fecha = models.DateTimeField(default=timezone.now)
    #like = models.IntegerField(default=0)
    #comentarios
    def total_likes(self):
        return LikePublicacion.objects.filter(publicacion=self).count()
    
class LikePublicacion(models.Model):
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    publicacion = models.ForeignKey('Publicacion', on_delete=models.CASCADE)
    
class LikeComentario(models.Model):
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    comentario = models.ForeignKey('Comentario', on_delete=models.CASCADE)
    
class Comentario(models.Model):
    idComentario = models.AutoField(primary_key=True)
    publicacion = models.ForeignKey('Publicacion', on_delete=models.CASCADE)
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    texto = models.TextField()
    foto = models.TextField()
    fecha = models.DateTimeField(default=timezone.now)
    #like = models.IntegerField(default=0)
    def total_likes(self):
        return LikeComentario.objects.filter(comentario=self).count()


class ZonaUsuario(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey('Usuario', on_delete=models.DO_NOTHING)
    zona = models.TextField()
    