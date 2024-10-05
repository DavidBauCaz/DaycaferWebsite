from django.shortcuts import render
from ..models import Usuario # importamos al usuario definido en core/models.py

## User controller ##

#Usuario
#_tipo

# Funcion que inicia sesión de un usuario
# Usuario usuario que quiere iniciar sesión
# pwd contraseña de la cuenta del usuario
def login(Usuario, pwd):
    return "token"

# Funcion que cierra sesión de un usuario
# Usuario usuario que va a cerrar sesión
def logout(Usuario):
    return False

def editar_perfil(Usuario, token):
    return False

def borrar(Usuario, token):
    return False

def crear(): #sugiero cambiarlo a signin
    return False

def verificar_correo(Usuario):
    return False

def factor_dos(Usuario):
    return False

def donacion(Usuario): # falta pesar en integraciones segun el diagrama
    return False
