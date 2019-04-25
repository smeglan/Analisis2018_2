'''
Created on 15/04/2019

@author: Sebastian
'''
from django.urls import path
from . import views 
from .views import AlgorListView

#Urls de cada uno de los templates.
urlpatterns = [
    path('', AlgorListView.as_view(), name = 'Web-IDE'),
    path('arbol/', views.arbol, name = 'Web-IDE-arbol'),
    path('about/', views.about, name = 'Web-IDE-about'),
    path('scores/', views.scores, name = 'Web-IDE-scores'),
    path(r'detail/<id>', views.detail, name = 'detail'),
    path('addAlgor/', views.addAlgor, name='add-algor')
]