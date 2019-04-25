from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse 

class algoritmos(models.Model):
    title = models.CharField(max_length = 100)
    logica =  models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete = models.CASCADE)

    def get_absolute_url(self):
        return reverse("detail", kwargs={"id":self.id})
    
    def __str__(self):
        return self.title

class puntuacion(models.Model):
    score = models.IntegerField()
    date_posted = models.DateTimeField(default=timezone.now)
    algoritmo = models.ForeignKey(algoritmos, on_delete = models.CASCADE)
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    def __str__(self):
        return algoritmos.objects.filter(id = self.algoritmo.id).first().title