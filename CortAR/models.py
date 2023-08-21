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
    
class Publicacion(models.Model):
    idPublicacion = models.AutoField(primary_key=True)
    usuario = models.ForeignKey('Usuario',on_delete=models.DO_NOTHING)
    titulo = models.TextField(default="")
    texto = models.TextField()
    foto = models.TextField()
    zona = models.TextField()
    fecha = models.DateTimeField(default=timezone.now)
    like = models.IntegerField(default=0)
    #comentarios
    def modificar_like(self, like):
        self.like = self.like + like
    
class Comentario(models.Model):
    idComentario = models.AutoField(primary_key=True)
    publicacion = models.ForeignKey('Publicacion', on_delete=models.CASCADE)
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    texto = models.TextField()
    foto = models.TextField()
    fecha = models.DateTimeField(default=timezone.now)
    like = models.IntegerField(default=0)
    def modificar_like(self, like):
        self.like = self.like + like


class ZonaUsuario(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey('Usuario', on_delete=models.DO_NOTHING)
    zona = models.TextField()
    