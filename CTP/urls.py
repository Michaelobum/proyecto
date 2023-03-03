from django.urls import re_path
from CTP.view_registros import viewTareas
from CTP.view_trabajadores import viewtrabajadores
from CTP.view_proyectos import viewProyectos
from seguridad.menu import menuinicial
from CTP.crearusuario import crear_superusuario


urlpatterns = [
    re_path(r'^$', menuinicial, name='inicio'),
    re_path(r'Tareas/', viewTareas, name='Tareas'),
    re_path(r'trabajadores/', viewtrabajadores, name='trabajadores'),
    re_path(r'Proyectos/', viewProyectos, name='Proyectos'),
    re_path(r'registration/', crear_superusuario, name='crear_superusuario'),
]