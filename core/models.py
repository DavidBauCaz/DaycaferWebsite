from django.db import models
from django.contrib.auth.models import AbstractBaseUser

# Archivo models, la app core funciona como una app centralizada donde se van a almacenar los modelos qye todas las demás
# apps van a compartir

class Usuario(models.Model):

    ## Atributos publicos ##

    imagen_usuario = models.CharField(max_length=255) # dirección a la imagen del usuario que se va a guardar en static
    nombre_usuario = models.CharField(max_length=255) 
    acerca_de = models.TextField() #texto rico en HTML
    redes_sociales = models.ForeignKey('RedSocial', on_delete=models.CASCADE, null=True, related_name='redes_usuario')
    #Relación muchos a muchos, un usuario puede tener más de una red social y una red social puede estar relacionada a más de un usuario
    #social_networks = models.ManyToManyField('RedSocial', blank=True, related_name='usuarios') 
    #social_networks = models.ForeignKey('RedSocialUsuario', on_delete=models.CASCADE, related_name='usuario')

    ## Atributos privados ##

    _contraseña = models.CharField(max_length=64) # Hash256 puede ser manejado por AbstractUser
    ##_correos = models.
    _verificado = models.BooleanField(default=False) # El usuario debe de verificar su cuenta antes de acceder al foro
    #_publications = models.ManyToManyField('Publication', blank=True) # Publicaciones que el usuario ha hecho
    _publicaciones = models.ForeignKey('Publicacion', on_delete=models.CASCADE, null=True, related_name='publicacion_usuario')
    # related_name hace que podamos acceder a todos los usuarios que siguen una publicacion
    #
    # publicacion.followers.all()
    #
    _siguiendo = models.ManyToManyField('Publicacion', related_name='seguidores') # Notificaciones que el usuario no ha leído
    _sin_leer = models.IntegerField(default=1) # Notificaciones sin leer
    _token = models.CharField(max_length=64) # Hash256
    ##numero o app
    def __str__(self): 
        return self.nombre_usuario

# El usuario normal tiene un atributo nickname que guarda una lista de nicknames y se almacena
# en otro modelo llamado Nicknames
class Normal(Usuario):
    nick = models.JSONField(blank=True, null=True)
    def __str__(self):
        return f"{self.nombre_de_usuario} (Normal)"

# El usuario Asociado necesita una matriz de permisos y una lista de juegos en los que 
# tienen permisos los asociados editar los foros, juegos y redes sociales
# la lista de juegos a los que tiene permisos el asociado es un modelo llamado AsociadoEn
class Asociado(Usuario):
    #permisos  matriz de permisos para Foro, Juego, RedSocial
    #en_cuales
    permisos = models.JSONField(blank=True, null=True) #matriz booleana que nos dice que tipo de permisos tiene el asociado en determinado foro de juego 
    #juegos_asociados = models.JSONField(blank=True, null=True) # Solo guardamos una lista de strings de los juegos
    juegos_asociados = models.ForeignKey('Juego', on_delete=models.CASCADE, null=True, related_name='juegos_asociados')
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
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE, related_name='developer')  # Relación con el modelo Usuario
    #correo

# Modelo que guarda los nicknames de un usuario
# Un usuario puede tener más de un apodo por lo que es un OneToMany y se logra con un foreignkey
# el atributo usuario guarda la referencia a Usuario al que pertenece el apodo 
# class Nickname(models.Model):
#     usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='nickname') #lista de nicknames para los distintos foros en los que está el usuario
#     nombre = models.CharField(max_length=100)

#     # Ejemplo de instancias
#     # usuario_david = Usuario.objects.create(user_name="David")
#     # nickname_1 = Nickname.objects.create(usuario=usuario_david, nombre="DarkKnight")
#     # nickname_2 = Nickname.objects.create(usuario=usuario_david, nombre="ShadowMaster")
#     # nickname_3 = Nickname.objects.create(usuario=usuario_david, nombre="FireMage")

#     #acceso desde modelo Usuario
#     # david = Usuario.objects.get(user_name="David")
#     # apodos = david.nicknames.all()  # Esto te devuelve ['DarkKnight', 'ShadowMaster', 'FireMage']

# Un usuario asociado puede editar cosas referentes a uno o más juegos
# class AsociadoEn(models.Model):
#     usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE, related_name='asociado_en')

#     def __str__(self):
#         return f"{self.user_name} (Asociado)"

class RedSocial(models.Model):
    #usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='redes_sociales_usuario')
    nombre = models.CharField(max_length=64)
    logo = models.TextField() # url a la imagen
    integracion = models.TextField() # texto rico en html
    link = models.TextField() # url a la red social
    def __str__(self):
        return self.nombre


class Publicacion(models.Model):
    publicador = models.ForeignKey(Usuario, on_delete=models.SET_NULL, related_name='publicaciones', null=True)
    #auto_now_add establece la fecha en el mometo en el que se crea un objeto de tipo publicacion
    fecha_de_publicacion = models.DateField(auto_now_add=True)
    contenido = models.TextField() #texto rico en html
    respuestas = models.ForeignKey('Respuesta', on_delete=models.CASCADE,null=True, related_name='respuestas_publicacion')
    upvotes = models.IntegerField()
    #seguidores = models.ForeignKey('Usuario', on_delete=models.CASCADE, related_name='usuarios_siguiendo') #es many to many y está definida en Usuario
    def __str__(self):
        return self.contenido[:50]  # Mostrar los primeros 50 caracteres como representación
            

class Respuesta(models.Model):
    usuario_publicador = models.ForeignKey(Usuario, on_delete=models.SET_NULL,null=True, related_name='respuestas')
    #publicacion = models.ForeignKey('Publicacion', on_delete=models.CASCADE, related_name='respuestas')
    fecha_publicacion = models.DateField(auto_now=True)
    contenido = models.TextField() # texto rico en html # originalmente se llamaba publicacion pero puede generar conflicto con el modelo Publicacion
    upvotes = models.IntegerField()
    
    def __str__(self):
        return self.contenido[:50]  # Mostrar los primeros 50 caracteres como representación

class Juego(models.Model):
    subforos = models.ForeignKey('SubForo', on_delete=models.CASCADE,null=True, related_name='subforos_juego')
    nombre = models.CharField(max_length=255)
    logo = models.CharField(max_length=255)
    subpaginas = models.JSONField(blank=True, null=True)
    redes_sociales = models.ForeignKey('RedSocial', on_delete=models.CASCADE, null=True, related_name='redes_juego')
    destacados = models.ForeignKey('Noticia', on_delete=models.CASCADE, null=True, related_name='noticias_juego')
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre


class SubForo(models.Model):
    publicaciones =  models.ForeignKey('Publicacion', on_delete=models.CASCADE,null=True, related_name='publicaciones_subforo')
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre


class Noticia(models.Model):
    publicacion_asociada = models.ForeignKey('Publicacion',on_delete=models.CASCADE, related_name='noticias_asociadas')
    imagen_principal = models.CharField(max_length=255)
    descripcion_rapida = models.TextField()
    titulo = models.TextField()
    def __str__(self):
        return self.titulo