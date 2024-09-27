from django.db import models
from django.contrib.auth.models import AbstractBaseUser

# Archivo models, la app core funciona como una app centralizada donde se van a almacenar los modelos qye todas las demás
# apps van a compartir

class Usuario(models.Model):

    ## Atributos publicos ##
    user_img = models.CharField(max_length=255) # dirección a la imagen del usuario que se va a guardar en static
    user_name = models.CharField(max_length=255) 
    about = models.TextField() #texto rico en HTML
    social_networks = models.ManyToManyField('SocialNetwork', blank=True) #Relación con el modelo SocialNetwork

    ## Atributos privados ##
    _password = models.CharField(max_length=64) # Hash256 puede ser manejado por AbstractUser
    #_correos = models.
    _verified = models.BooleanField(default=False) # El usuario debe de verificar su cuenta antes de acceder al foro
    _publications = models.ManyToManyField('Publication', blank=True) # Publicaciones que el usuario ha hecho
    # related_name hace que podamos acceder a todos los usuarios que siguen una publicacion
    #
    # publicacion.followers.all()
    #
    _following = models.ManyToManyField('Publication', blank=True, related_name='followers') # Notificaciones que el usuario no ha leído
    _unread = models.IntegerField(default=0) # Notificaciones sin leer
    _token = models.CharField(max_length=64) # Hash256

class Normal(Usuario):

    def __str__(self):
        return f"{self.nombre_de_usuario} (Normal)"

class Asociado(Usuario):
    #permisos  matriz de permisos para Foro, Juego, RedSocial
    asociado_en = models.ManyToManyField('Juego', blank=True)  # Relación con Juego

    def __str__(self):
        return f"{self.nombre_de_usuario} (Asociado)"

class Empleado(Usuario):
    cargo = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.nombre_de_usuario} (Empleado)"
    
class Nickname(models.Model):
    nickname = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='nicknames') #lista de nicknames para los distintos foros en los que está el usuario
