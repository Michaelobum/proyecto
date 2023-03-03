from django.contrib import messages
from django.db import transaction
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template
from CTP.forms import TareasForm
from django.contrib.auth.decorators import login_required
from CTP.models import Tareas


@login_required
def viewTareas(request):
    data = {'empresa': 'Michael', 'nombre': 'Tareas', 'ruta': '/Tareas/'}

    if request.method == 'POST':

        if 'action' in request.POST:
            data['action'] = action = request.POST['action']

            if action == 'agregar':
                with transaction.atomic():
                    try:
                        if Tareas.objects.filter(nombre_tarea=request.POST['nombre_tarea']).exists():
                            messages.error(request, 'El nombre está repetido')
                            return redirect('{}?action=agregar'.format(request.path))
                        else:
                            form = TareasForm(request.POST)
                            if form.is_valid():
                                tareas = Tareas(nombre_tarea=form.cleaned_data['nombre_tarea'],
                                                encargados=form.cleaned_data['encargados'])
                                tareas.save(request)
                                messages.success(
                                    request, 'Tareas Guardado Correctamente chingadamadre')
                    except Exception as ex:
                        messages.error(request, ex)

            elif action == 'editar':
                with transaction.atomic():
                    try:
                        id = request.POST['id']
                        tareas = Tareas.objects.get(id=id)
                        form = TareasForm(request.POST, instance=tareas)
                        if form.is_valid():
                            form.save()
                            messages.success(request, 'Tareas guardado exitosamente chingadamadre!')
                    except Exception as ex:
                        messages.error(request, ex)

            elif action == 'eliminar':
                with transaction.atomic():
                    try:
                        id = request.POST['id']
                        tareas = Tareas.objects.get(id=id)
                        tareas.status = False
                        tareas.save()
                        messages.success(request, 'Tareas eliminado')
                    except Exception as ex:
                        messages.error(request, ex)

            elif action == 'pdflistado':
                try:
                    data['action'] = Tareas.objects.get(id=request.GET['id'])
                    template = get_template("pdf/Tareas/listadoP.html")
                    return JsonResponse({'data': template.render(data)})
                except Exception as ex:
                    messages.error(request, ex)
            return redirect(request.path)

    else:
        if 'action' in request.GET:
            data['action'] = action = request.GET['action']

            if action == 'agregar':
                form = TareasForm
                data['formulario'] = form
                return render(request, 'Tareas/formulario.html', data)

            elif action == 'editar':
                try:
                    data['id'] = id = request.GET['id']
                    tareas = Tareas.objects.get(id=id)
                    form = TareasForm(initial=model_to_dict(tareas))
                    data['formulario'] = form
                    return render(request, 'Tareas/formulario.html', data)
                except Exception as ex:
                    messages.error(request, ex)
                    return redirect('/Tareas/')

            elif action == 'eliminar':
                try:
                    data['id'] = id = request.GET['id']
                    data['Tareas'] = tareas = Tareas.objects.get(id=id)
                    return render(request, 'Tareas/eliminar.html', data)
                except Exception as ex:
                    messages.error(request, ex)
                    return redirect(request, '/Tareas/')

            elif action == 'pdflistado':
                data['listado'] = Tareas.objects.filter().order_by('nombre_tarea')
                return render(request, 'pdf/Tareas/listadoP.html', data)

            elif action == 'consultar':
                try:
                    resultado = True
                    data['id'] = id = request.GET['id']
                    data['Tareas'] = tareas = Tareas.objects.get(id=id)
                    template = get_template('Tareas/listadoajax.html')
                    return JsonResponse({"result": resultado, 'data': template.render(data)})

                except Exception as ex:
                    resultado = False
                    mensaje = ex
                    return JsonResponse({"result": resultado, 'mensaje': mensaje})

            return redirect('/Tareas/')

    try:
        data['listado'] = Tareas.objects.filter(status=True).order_by(
            'nombre_tarea', 'encargados')
    except Exception as ex:
        print(ex)
    return render(request, 'Tareas/listado.html', data)
