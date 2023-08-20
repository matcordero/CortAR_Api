from rest_framework import serializers
from .models import *

class PublicacionSerializador(serializers.ModelSerializer):
    class Meta:
        model = Publicacion
        fields = '__all__'

class UsuarioSerializador(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'
        
class ComentarioSerializador(serializers.ModelSerializer):
    class Meta:
        model = Comentario
        fields = '__all__'
        
class ZonaUsuarioSerializador(serializers.ModelSerializer):
    class Meta:
        model = ZonaUsuario
        fields = '__all__'