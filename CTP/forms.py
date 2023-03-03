from django import forms
from CTP.models import Tareas, encargado, Proyectos
from django.contrib.auth.forms import UserCreationForm



class trabajadoresForm(forms.ModelForm):
    class Meta:
        model = encargado
        fields = ['nombres']
        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'form-control',
                                             "placeholder": 'Ingresa el nombre'}), }
        labels = {'nombres': 'nombres'}


class TareasForm(forms.ModelForm):
    class Meta:
        model = Tareas
        fields = ['nombre_tarea', 'encargados']
        widgets = {
            'nombre_tarea': forms.TextInput(attrs={'class': 'form-control'}),
            'encargados': forms.Select(attrs={'class': 'form-control'})
        }
        labels = {'nombre_tarea': 'nombre_tarea', 'encargados': 'encargados'}

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Proyectos
        fields = ['nombre_proyecto', 'lider','encargados']
        widgets = {
            'nombre_proyecto': forms.TextInput(attrs={'class': 'form-control'}),
            'lider': forms.Select(attrs={'class': 'form-control'}),
            'encargados': forms.SelectMultiple(attrs={'class': 'form_control select2'}),
        }
        labels = {'nombre_proyecto': 'nombre_proyecto', 'lider': 'lider', 'encargados':'encargados' }

class encargadoform(forms.ModelForm):
    class Meta:
        model = Proyectos
        fields = ['encargados']
        widgets = {
            'encargados': forms.Select(attrs={'class': 'form-control'})
        }
        labels = {'encargados': 'encargados'}