from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden
from .models import Artigo, Comentario
from .forms import ArtigoForm, ComentarioForm

def is_autor(user):
    return user.groups.filter(name='autores').exists() or user.is_superuser

def lista_artigos(request):
    artigos = Artigo.objects.all().order_by('-data_criacao')
    return render(request, 'artigos/lista.html', {'artigos': artigos})

def artigo_detalhe(request, id):
    artigo = get_object_or_404(Artigo, id=id)
    comentarios = artigo.comentarios.all().order_by('-data_criacao')
    form_comentario = ComentarioForm()

    if request.method == 'POST':
        if 'like' in request.POST:
            artigo.likes += 1
            artigo.save()
            return redirect('artigo_detalhe', id=artigo.id)
            
        elif 'comentar' in request.POST and request.user.is_authenticated:
            form_comentario = ComentarioForm(request.POST)
            if form_comentario.is_valid():
                comentario = form_comentario.save(commit=False)
                comentario.artigo = artigo
                comentario.autor = request.user
                comentario.save()
                return redirect('artigo_detalhe', id=artigo.id)

    return render(request, 'artigos/detalhe.html', {
        'artigo': artigo,
        'comentarios': comentarios,
        'form_comentario': form_comentario
    })

@login_required
@user_passes_test(is_autor)
def novo_artigo(request):
    form = ArtigoForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        artigo = form.save(commit=False)
        artigo.autor = request.user
        artigo.save()
        return redirect('lista_artigos')
    return render(request, 'artigos/form.html', {'form': form, 'titulo_pagina': 'Novo Artigo'})

@login_required
def editar_artigo(request, id):
    artigo = get_object_or_404(Artigo, id=id)
    # Proteção EXTRA: Apenas o autor original (ou um superuser) pode editar
    if artigo.autor != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("Não tens permissão para editar um artigo que não é teu.")

    form = ArtigoForm(request.POST or None, request.FILES or None, instance=artigo)
    if form.is_valid():
        form.save()
        return redirect('artigo_detalhe', id=artigo.id)
    return render(request, 'artigos/form.html', {'form': form, 'titulo_pagina': 'Editar Artigo'})

@login_required
def apagar_artigo(request, id):
    artigo = get_object_or_404(Artigo, id=id)
    if artigo.autor != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("Não tens permissão para apagar um artigo que não é teu.")
    
    artigo.delete()
    return redirect('lista_artigos')