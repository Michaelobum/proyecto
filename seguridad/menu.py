from django.shortcuts import render, redirect
from CTP.models import *
from django.contrib.auth.decorators import login_required


@login_required
def menuinicial(request):
    data = {
        'ruta': '/',
        'empresa': 'CTP',
        'nombre': 'Inicio',
        'totalencarga': encargado.objects.all().count(),
        'totalta': Tareas.objects.all().count(),
        'totalpro': Proyectos.objects.all().count(),
        'user': request.user
    }

    return render(request, 'menu.html', data)
