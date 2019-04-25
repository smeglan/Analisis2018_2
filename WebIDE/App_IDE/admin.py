from django.contrib import admin
from .models import algoritmos, puntuacion

#Añade modelos de la base de datos a la pagina de la administracion.
admin.site.register(algoritmos)
admin.site.register(puntuacion)
