# Generated by Django 3.2.18 on 2023-03-06 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CTP', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='encargado',
            name='nombres',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]