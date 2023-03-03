from django.shortcuts import render, redirect
from CTP.models import *
from django.contrib.auth.decorators import login_required


@login_required
def menuinicial(request):
    data = {
        'ruta': '/',
        'empresa': 'CWP',
        'nombre': 'Inicio',
        'totalmar': encargado.objects.all().count(),
        'totalpro': Tareas.objects.all().count()
    }

    return render(request, 'menu.html', data)
