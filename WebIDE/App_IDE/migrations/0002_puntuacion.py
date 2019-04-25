# Generated by Django 2.1.7 on 2019-04-21 23:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('App_IDE', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='puntuacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField()),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('algoritmo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App_IDE.algoritmos')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]