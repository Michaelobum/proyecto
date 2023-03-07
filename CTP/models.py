from django.db import models


class ModeloBase(models.Model):
    fecha_registro = models.DateField(
        verbose_name="Fecha Registro", auto_now_add=True)
    hora_registro = models.TimeField(
        verbose_name="Hora Registro", auto_now_add=True)
    status = models.BooleanField(default=True)

    class Meta:
        abstract = True


class encargado(ModeloBase):
    nombres = models.CharField(null=True, blank=True, max_length=100)
    def __str__(self):
        return self.nombres


class Proyectos(ModeloBase):
    nombre_proyecto = models.CharField(max_length=100)
    lider = models.ForeignKey(encargado, on_delete=models.CASCADE, related_name='proyectos_lider')
    encargados = models.ManyToManyField(encargado, related_name='proyectos_encargados')
    def __str__(self):
        return str(self.nombre_proyecto)

class Tareas(ModeloBase):
    nombre_tarea = models.CharField(null=True, blank=True, max_length=100)
    encargados = models.ForeignKey(encargado, on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre_tarea



