from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_artigos, name='lista_artigos'),
    path('<int:id>/', views.artigo_detalhe, name='artigo_detalhe'),
    path('novo/', views.novo_artigo, name='novo_artigo'),
    path('<int:id>/editar/', views.editar_artigo, name='editar_artigo'),
    path('<int:id>/apagar/', views.apagar_artigo, name='apagar_artigo'),
]