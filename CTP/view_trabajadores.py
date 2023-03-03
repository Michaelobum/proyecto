from django.contrib import messages
from django.db import transaction
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template
from CTP.forms import trabajadoresForm
from CTP.models import encargado
from django.contrib.auth.decorators import login_required


@login_required
def viewtrabajadores(request):
    data = {'empresa': 'Michael', 'nombre': 'Encargado', 'ruta': '/trabajadores/'}

    if request.method == 'POST':

        if 'action' in request.POST:
            action = request.POST['action']

            if action == 'agregar':
                with transaction.atomic():
                    try:
                        if encargado.objects.filter(nombres=request.POST['nombres']).exists():
                            messages.error(request, 'Registro ya existe')
                            return redirect('{}?action=agregar'.format(request.path))

                        else:
                            form = trabajadoresForm(request.POST)
                            try:
                                if form.is_valid():
                                    Encargado = encargado(nombres=form.cleaned_data['nombres'])
                                    Encargado.save()
                                    messages.success(
                                        request, 'Registro Guardado Correctamente')
                            except Exception as ex:
                                messages.error(request, ex)
                    except Exception as ex:
                        messages.error(request, ex)

            elif action == 'editar':
                with transaction.atomic():
                    try:
                        id = request.POST['id']
                        Encargado = encargado.objects.get(id=id)
                        form = trabajadoresForm(request.POST, instance=encargado)
                        if form.is_valid():
                            form.save()
                            messages.success(request, 'El registro se editó correctamente')
                        else:
                            messages.error(request, 'error')
                    except Exception as ex:
                        messages.error(request, ex)

            elif action == 'pdflistado':
                with transaction.atomic():
                    try:
                        data['pdf'] = encargado.objects.get(id=request.GET['id'])
                        template = get_template('pdf/trabajadores/listadoM.html')
                        return JsonResponse({'data': template.render(data)})
                    except Exception as ex:
                        mensaje = ex
                        return JsonResponse({"mensaje": mensaje})

            elif action == 'eliminar':
                with transaction.atomic():
                    try:
                        id = request.POST['id']
                        Encargado = encargado.objects.get(id=id)
                        Encargado.status = False
                        Encargado.save()
                        messages.success(request, 'registro eliminado')
                    except Exception as ex:
                        messages.error(request, ex)

            return redirect(request.path)

    else:
        if 'action' in request.GET:
            data['action'] = action = request.GET['action']

            if action == 'agregar':
                form = trabajadoresForm()
                data['formulario'] = form
                return render(request, 'trabajadores/formulario.html', data)

            elif action == 'editar':
                try:
                    data['id'] = id = request.GET['id']
                    Encargado = encargado.objects.get(id=id)
                    form = trabajadoresForm(initial=model_to_dict(encargado))
                    data['formulario'] = form
                    return render(request, 'trabajadores/formulario.html', data)
                except Exception as ex:
                    messages.error(request, ex)
                    return redirect('/trabajadores/')
            elif action == 'eliminar':
                data['id'] = id = request.GET['id']
                data['trabajadores'] = Encargado = encargado.objects.get(id=id)
                return render(request, 'trabajadores/eliminar.html', data)

            elif action == 'pdflistado':
                data['listado'] = encargado.objects.filter(status=True).order_by('nombres')
                return render(request, 'pdf/trabajadores/listadoM.html', data)

            elif action == 'consultar':
                try:
                    resultado = True
                    data['encargados'] = Encargado = encargado.objects.get(id=request.GET['id'])
                    template = get_template('trabajadores/listadoajax.html')
                    return JsonResponse({'result': resultado, 'data': template.render(data)})
                except Exception as ex:
                    resultado = False
                    mensaje = ex
                    return JsonResponse({'result': resultado, 'mensaje': mensaje})

            return redirect('/trabajadores/')
    try:
        data['listado'] = encargado.objects.filter(status=True)
    except Exception as ex:
        print(ex)
    return render(request, 'trabajadores/listado.html', data)
