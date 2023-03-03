# Generated by Django 3.2.18 on 2023-03-03 02:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='encargado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_registro', models.DateField(auto_now_add=True, verbose_name='Fecha Registro')),
                ('hora_registro', models.TimeField(auto_now_add=True, verbose_name='Hora Registro')),
                ('status', models.BooleanField(default=True)),
                ('nombres', models.CharField(blank=True, max_length=10, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Tareas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_registro', models.DateField(auto_now_add=True, verbose_name='Fecha Registro')),
                ('hora_registro', models.TimeField(auto_now_add=True, verbose_name='Hora Registro')),
                ('status', models.BooleanField(default=True)),
                ('nombre_tarea', models.CharField(blank=True, max_length=100, null=True)),
                ('encargados', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CTP.encargado')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Proyectos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_registro', models.DateField(auto_now_add=True, verbose_name='Fecha Registro')),
                ('hora_registro', models.TimeField(auto_now_add=True, verbose_name='Hora Registro')),
                ('status', models.BooleanField(default=True)),
                ('nombre_proyecto', models.CharField(max_length=100)),
                ('encargados', models.ManyToManyField(related_name='proyectos_encargados', to='CTP.encargado')),
                ('lider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proyectos_lider', to='CTP.encargado')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
