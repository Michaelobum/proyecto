from django.contrib.auth.models import User
from django.shortcuts import render, redirect

def crear_superusuario(request):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 != password2:
            error = 'Las contraseñas no coinciden, porfavor intentelo de nuevo'
            return render(request, 'registration/pruebas.html', {'error': error})
        User.objects.create_superuser(username=username, password=password1)
        return render(request, 'registration/login.html')

    return render(request, 'registration/pruebas.html')
