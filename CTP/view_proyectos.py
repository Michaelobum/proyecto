from django.contrib import messages
from django.db import transaction
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template
from CTP.forms import ProjectForm, trabajadoresForm, encargadoform
from django.contrib.auth.decorators import login_required
from CTP.models import Proyectos, encargado


@login_required
def viewProyectos(request):
    data = {'empresa': 'Michael', 'nombre': 'Proyectos', 'ruta': '/Proyectos/'}
    proyecto = None

    if request.method == 'POST':
        if 'action' in request.POST:
            data['action'] = action = request.POST['action']
            if action == 'agregar':
                with transaction.atomic():
                    try:
                        if Proyectos.objects.filter(nombre_proyecto=request.POST['nombre_proyecto']).exists():
                            messages.error(request, 'El nombre está repetido')
                            return redirect('{}?action=agregar'.format(request.path))
                        else:
                            form = ProjectForm(request.POST)
                            if form.is_valid():
                                proyecto = Proyectos(nombre_proyecto=form.cleaned_data['nombre_proyecto'],
                                                     lider=form.cleaned_data['lider'])
                                proyecto.save()
                                encargados = form.cleaned_data['encargados']
                                proyecto.encargados.set(encargados)
                                messages.success(
                                    request, 'Proyecto Guardado Correctamente')
                    except Exception as ex:
                        messages.error(request, ex)

            elif action == 'editar':
                with transaction.atomic():
                    try:
                        id = request.POST['id']
                        proyecto = Proyectos.objects.get(id=id)
                        if proyecto.encargados.exists():
                            encargado = proyecto.encargados.first().nombres
                        else:
                            encargado = None
                        form = ProjectForm(request.POST, instance=proyecto)
                        if form.is_valid():
                            form.save()
                            messages.success(request, 'Proyectos guardado exitosamente!')
                    except Exception as ex:
                        messages.error(request, ex)

            elif action == 'eliminar':
                with transaction.atomic():
                    try:
                        id = request.POST['id']
                        proyectos = Proyectos.objects.get(id=id)
                        proyectos.status = False
                        proyectos.save()
                        messages.success(request, 'Proyectos eliminado')
                    except Exception as ex:
                        messages.error(request, ex)

            elif action == 'pdflistado':
                try:
                    data['action'] = Proyectos.objects.get(id=request.GET['id'])
                    template = get_template("pdf/Proyectos/listadoP.html")
                    return JsonResponse({'data': template.render(data)})
                except Exception as ex:
                    messages.error(request, ex)
            return redirect(request.path)

    else:
        if 'action' in request.GET:
            data['action'] = action = request.GET['action']

            if action == 'agregar':
                form = ProjectForm()
                data['formulario'] = form
                return render(request, 'Proyectos/formulario.html', data)


            elif action == 'editar':
                try:
                    data['id'] = id = request.GET['id']
                    proyecto = Proyectos.objects.get(id=id)
                    form = ProjectForm(initial=model_to_dict(proyecto))
                    data['formulario'] = form
                    return render(request, 'Proyectos/formulario.html', data)
                except Exception as ex:
                    messages.error(request, ex)
                    return redirect('/Proyectos/')

            elif action == 'eliminar':
                try:
                    resultado = True
                    data['id'] = id = request.GET['id']
                    data['Proyectos'] = proyectos = Proyectos.objects.get(id=id)
                    return render(request, 'Proyectos/eliminar.html', data)
                except Exception as ex:
                    messages.error(request, ex)
                    return redirect(request, '/Proyectos/')


            elif action == 'pdflistado':
                proyectos = Proyectos.objects.filter(status=True).order_by('nombre_proyecto', 'lider')
                data['listado'] = []
                for proyecto in proyectos:
                    encargados = [e.nombres for e in proyecto.encargados.all()]
                    data['listado'].append({
                        'pk': proyecto.pk,
                        'nombre_proyecto': proyecto.nombre_proyecto,
                        'lider': proyecto.lider.nombres,
                        'encargados': encargados
                    })
                return render(request, 'pdf/Proyectos/listadoP.html', data)

            elif action == 'consultar':
                try:
                    resultado = True
                    data['id'] = id = request.GET['id']
                    data['Proyectos'] = proyectos = Proyectos.objects.get(id=id)
                    template = get_template('Proyectos/listadoajax.html')
                    return JsonResponse({"result": resultado, 'data': template.render(data)})

                except Exception as ex:
                    resultado = False
                    mensaje = ex
                    return JsonResponse({"result": resultado, 'mensaje': mensaje})

            return redirect('/Proyectos/')

    try:
        proyectos = Proyectos.objects.filter(status=True).order_by('nombre_proyecto', 'lider')
        data['listado'] = []
        for proyecto in proyectos:
            encargados = [e.nombres for e in proyecto.encargados.all()]
            data['listado'].append({
                'cont': 0,
                'pk': proyecto.pk,
                'nombre_proyecto': proyecto.nombre_proyecto,
                'lider': proyecto.lider.nombres,
                'encargados': encargados
            })
    except Exception as ex:
        print(ex)
    return render(request, 'Proyectos/listado.html', data)
