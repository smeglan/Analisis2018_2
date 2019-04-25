from django.shortcuts import render, redirect
from django.views.generic import ListView
from .models import algoritmos, puntuacion
from users.models import User 
from .logic import procesador_algoritmos
from django.contrib.auth.decorators import login_required

def home(request):
    context = {
            'algoritmos' : algoritmos.objects.all()
        }
    return render(request, 'ide/home.html', context)

@login_required
def addAlgor(request):
    algor = request.POST['algoritmo']
    user = User.objects.first()
    nombre = procesador_algoritmos.get_algor_name(algor.splitlines())
    new_algor = algoritmos(title = nombre, logica = algor, author = user)
    new_algor.save()
    return redirect("Web-IDE")

@login_required
def detail(request, id):
    pk = id
    algor = algoritmos.objects.get(id = pk)
    context = {
        'algoritmo' : algor.logica.splitlines(),
        'algoritmo2': algoritmos.objects.all().first().logica.splitlines(),
    }
    return render(request, 'App_IDE/detail.html', context)

@login_required
def set_points(request):
    algor = request.POST['algoritmo']
    user = User.objects.first()
    nombre = procesador_algoritmos.get_algor_name(algor.splitlines())
    new_algor = algoritmos(title = nombre, logica = algor, author = user)
    new_algor.save()
    return redirect("Web-IDE")

class AlgorListView(ListView):
    model = algoritmos
    template_name = 'ide/home.html'
    context_object_name = 'algoritmos'
    ordering = ['-date_posted']

def about(request):
    developers = [
        {   
            'desarrollador': 'Sebastian Norena Meglan',
            'email': 'sebastian.1701313412@ucaldas.edu.co'
        },
        {
            'desarrollador':'Nicolas Rivera Jaramillo',
            'email':'nicolas.1701313965@ucaldas.edu.co'
        }
    ]
    context = {
        'title': 'About',
        'developers':developers
    }
    return render(request, 'ide/about.html', context)

def arbol(request):
    return render(request, 'ide/tree_page.html', {'title': 'Arbol'})


def scores(request):
    context = {
            'title': 'Tabla de puntuaciones',
            'scores' : puntuacion.objects.all()
        }
    
    return render(request, 'ide/scores.html', context)
