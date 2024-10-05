from django.urls import path
from .views import user_controller  # Importamos las vistas o controladores necesarios
from .views import forum_controller
from .views import game_page_controller

urlpatterns = [
    path('login/', user_controller.login, name='login'),
    path('logout/', user_controller.logout, name='logout'),
    path('editar_perfil/', user_controller.editar_perfil, name='editar_perfil'),
]
