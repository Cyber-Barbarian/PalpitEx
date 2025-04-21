# palpitexApp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('soma/', views.minha_view, name='minha_view'),
   path('', views.index, name='index'), 
   path('extract_data/', views.extract_data, name='extract_data'),
]