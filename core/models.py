from django.db import models
from django.contrib.auth.models import AbstractBaseUser

# Archivo models, la app core funciona como una app centralizada donde se van a almacenar los modelos qye todas las demás
# apps van a compartir

class Usuario(models.Model):

    ## Atributos publicos ##

    user_img = models.CharField(max_length=255) # dirección a la imagen del usuario que se va a guardar en static
    user_name = models.CharField(max_length=255) 
    about = models.TextField() #texto rico en HTML
    #Relación muchos a muchos, un usuario puede tener más de una red social y una red social puede estar relacionada a más de un usuario
    #social_networks = models.ManyToManyField('RedSocial', blank=True, related_name='usuarios') 
    #social_networks = models.ForeignKey('RedSocialUsuario', on_delete=models.CASCADE, related_name='usuario')

    ## Atributos privados ##

    _password = models.CharField(max_length=64) # Hash256 puede ser manejado por AbstractUser
    ##_correos = models.
    _verified = models.BooleanField(default=False) # El usuario debe de verificar su cuenta antes de acceder al foro
    #_publications = models.ManyToManyField('Publication', blank=True) # Publicaciones que el usuario ha hecho
    _publicaciones = models.ForeignKey('Publicacion', on_delete=models.CASCADE, related_name='publicacion_usuario')
    # related_name hace que podamos acceder a todos los usuarios que siguen una publicacion
    #
    # publicacion.followers.all()
    #
    _following = models.ManyToManyField('Publicacion', blank=True, related_name='seguidores') # Notificaciones que el usuario no ha leído
    _unread = models.IntegerField(default=0) # Notificaciones sin leer
    _token = models.CharField(max_length=64) # Hash256
    ##numero o app
    def __str__(self):
        return self.user_name

# El usuario normal tiene un atributo nickname que guarda una lista de nicknames y se almacena
# en otro modelo llamado Nicknames
class Normal(Usuario):

    def __str__(self):
        return f"{self.nombre_de_usuario} (Normal)"

# El usuario Asociado necesita una matriz de permisos y una lista de juegos en los que 
# tienen permisos los asociados editar los foros, juegos y redes sociales
# la lista de juegos a los que tiene permisos el asociado es un modelo llamado AsociadoEn
class Asociado(Usuario):
    #permisos  matriz de permisos para Foro, Juego, RedSocial
    #en_cuales
    def __str__(self):
        return f"{self.nombre_de_usuario} (Asociado)"

class Empleado(Usuario):
    cargo = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.nombre_de_usuario} (Empleado)"

class Developer(models.Model):
    descripcion = models.TextField() #texto rico en html
    nombre = models.CharField(max_length=100)
    imagen = models.CharField(max_length=100) #url
    link = models.CharField(max_length=255) # link a pagina del developer
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='developer')  # Relación con el modelo Usuario

# Modelo que guarda los nicknames de un usuario
# Un usuario puede tener más de un apodo por lo que es un OneToMany y se logra con un foreignkey
# el atributo usuario guarda la referencia a Usuario al que pertenece el apodo 
class Nickname(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='nickname') #lista de nicknames para los distintos foros en los que está el usuario
    nombre = models.CharField(max_length=100)

    # Ejemplo de instancias
    # usuario_david = Usuario.objects.create(user_name="David")
    # nickname_1 = Nickname.objects.create(usuario=usuario_david, nombre="DarkKnight")
    # nickname_2 = Nickname.objects.create(usuario=usuario_david, nombre="ShadowMaster")
    # nickname_3 = Nickname.objects.create(usuario=usuario_david, nombre="FireMage")

    #acceso desde modelo Usuario
    # david = Usuario.objects.get(user_name="David")
    # apodos = david.nicknames.all()  # Esto te devuelve ['DarkKnight', 'ShadowMaster', 'FireMage']

# Un usuario asociado puede editar cosas referentes a uno o más juegos
class AsociadoEn(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='asociado_en')
    #juego_asociado = models
    #falta implementar modelo de juegos

class RedSocial(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='redes_sociales_usuario')
    nombre = models.CharField(max_length=64)
    logo = models.TextField() # url a la imagen
    integracion = models.TextField() # texto rico en html
    link = models.TextField() # url a la red social


class Publicacion(models.Model):
    publicador = models.ForeignKey(Usuario, on_delete=models.SET_NULL, related_name='publicaciones', null=True)
    #auto_now_add establece la fecha en el mometo en el que se crea un objeto de tipo publicacion
    fecha_de_publicacion = models.DateField(auto_now_add=True)
    contenido = models.TextField() #texto rico en html
    #respuestas
    upvotes = models.IntegerField()
    #followers
    def __str__(self):
        return self.contenido[:50]  # Mostrar los primeros 50 caracteres como representación
            

class Respuesta(models.Model):
    usuario_publicador = models.ForeignKey(Usuario, on_delete=models.SET_NULL, related_name='respuestas', null=True)
    publicacion = models.ForeignKey('Publicacion', on_delete=models.CASCADE, related_name='respuestas')
    fecha_publicacion = models.DateField(auto_now=True)
    contenido = models.TextField() # texto rico en html # originalmente se llamaba publicacion pero puede generar conflicto con el modelo Publicacion
    upvotes = models.IntegerField()
    def __str__(self):
        return self.contenido[:50]  # Mostrar los primeros 50 caracteres como representación

    