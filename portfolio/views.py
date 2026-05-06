from django.shortcuts import render, redirect, get_object_or_404
from .models import Tecnologia, Licenciatura, Formacao, MakingOf, Projeto, Competencia, UnidadeCurricular, Tipo
from django.contrib.auth.decorators import login_required


# ==========================================
# PÁGINAS PRINCIPAIS
# ==========================================

@login_required
def home_view(request):
    return render(request, 'portfolio/home.html')

def contactos_view(request):
    return render(request, 'portfolio/contactos.html')

@login_required
def makingofs_view(request):
    makingofs = MakingOf.objects.all().order_by('-id') 
    return render(request, 'portfolio/makingofs.html', {'makingofs': makingofs})

# ==========================================
# TECNOLOGIAS (CRUD)
# ==========================================

@login_required
def tecnologias_view(request):
    if request.method == "POST":
        nome = request.POST.get('nome')
        link = request.POST.get('link_oficial')
        detalhes = request.POST.get('detalhes')
        nivel = request.POST.get('nivel_interesse')
        
        tecnologia = Tecnologia(nome=nome, link_oficial=link, detalhes=detalhes, nivel_interesse=nivel)
        if 'logo' in request.FILES:
            tecnologia.logo = request.FILES['logo']
            
        tecnologia.save()
        return redirect('tecnologias')
        
    tecnologias = Tecnologia.objects.all()
    return render(request, 'portfolio/tecnologias.html', {'tecnologias': tecnologias})

def editar_tecnologia(request, id):
    tecnologia = get_object_or_404(Tecnologia, id=id)
    if request.method == "POST":
        tecnologia.nome = request.POST.get('nome')
        tecnologia.link_oficial = request.POST.get('link_oficial')
        tecnologia.detalhes = request.POST.get('detalhes')
        tecnologia.nivel_interesse = request.POST.get('nivel_interesse')
        
        if 'logo' in request.FILES:
            tecnologia.logo = request.FILES['logo']
            
        tecnologia.save()
        return redirect('tecnologias')
        
    return render(request, 'portfolio/editar_tecnologia.html', {'tecnologia': tecnologia})

def eliminar_tecnologia(request, id):
    tecnologia = get_object_or_404(Tecnologia, id=id)
    tecnologia.delete()
    return redirect('tecnologias')

# ==========================================
# PROJETOS (CRUD)
# ==========================================
@login_required
def projetos_view(request):
    if request.method == "POST":
        projeto = Projeto.objects.create(
            titulo=request.POST.get('titulo'), 
            descricao=request.POST.get('descricao'),
            conceitos_aplicados=request.POST.get('conceitos_aplicados'),
            link_github=request.POST.get('link_github'),
            video_demo=request.POST.get('video_demo') 
        )
        
        uc_id = request.POST.get('uc')
        if uc_id: projeto.uc_id = uc_id
        if 'imagem' in request.FILES: projeto.imagem = request.FILES['imagem']
            
        projeto.save()
        projeto.tecnologias.set(request.POST.getlist('tecnologias'))
        projeto.competencias.set(request.POST.getlist('competencias'))
        return redirect('projetos')
    
    context = {
        'projetos': Projeto.objects.all(),
        'todas_tecnologias': Tecnologia.objects.all(),
        'todas_ucs': UnidadeCurricular.objects.all(), 
        'todas_competencias': Competencia.objects.all(),
    }
    return render(request, 'portfolio/projetos.html', context)

def editar_projeto(request, id):
    projeto = get_object_or_404(Projeto, id=id)
    if request.method == "POST":
        projeto.titulo = request.POST.get('titulo')
        projeto.descricao = request.POST.get('descricao')
        projeto.conceitos_aplicados = request.POST.get('conceitos_aplicados')
        projeto.link_github = request.POST.get('link_github')
        projeto.video_demo = request.POST.get('video_demo')
        
        uc_id = request.POST.get('uc')
        if uc_id: projeto.uc_id = uc_id
        else: projeto.uc = None

        if 'imagem' in request.FILES: projeto.imagem = request.FILES['imagem']
            
        projeto.save()
        projeto.tecnologias.set(request.POST.getlist('tecnologias'))
        projeto.competencias.set(request.POST.getlist('competencias'))
        return redirect('projetos')

    context = {
        'projeto': projeto,
        'todas_tecnologias': Tecnologia.objects.all(),
        'todas_ucs': UnidadeCurricular.objects.all(), 
        'todas_competencias': Competencia.objects.all(),
    }
    return render(request, 'portfolio/editar_projeto.html', context)

def eliminar_projeto(request, id):
    projeto = get_object_or_404(Projeto, id=id)
    projeto.delete()
    return redirect('projetos')

# ==========================================
# PERCURSO ACADÉMICO / FORMAÇÕES (CRUD)
# ==========================================

@login_required
def percurso_view(request):
    if request.method == "POST":
        formacao = Formacao.objects.create(
            designacao=request.POST.get('designacao'),
            instituicao=request.POST.get('instituicao'),
            data_inicio=request.POST.get('data_inicio'),
            data_fim=request.POST.get('data_fim') or None,
            descricao=request.POST.get('descricao')
        )
        formacao.competencias_adquiridas.set(request.POST.getlist('competencias_adquiridas'))
        return redirect('percurso')
    
    context = {
        'formacoes': Formacao.objects.all(),
        'todas_competencias': Competencia.objects.all(), 
    }
    return render(request, 'portfolio/percurso.html', context)

def editar_formacao(request, id):
    formacao = get_object_or_404(Formacao, id=id)
    if request.method == "POST":
        formacao.designacao = request.POST.get('designacao')
        formacao.instituicao = request.POST.get('instituicao')
        formacao.data_inicio = request.POST.get('data_inicio')
        formacao.data_fim = request.POST.get('data_fim') or None
        formacao.descricao = request.POST.get('descricao')
        
        formacao.save()
        formacao.competencias_adquiridas.set(request.POST.getlist('competencias_adquiridas'))
        return redirect('percurso')

    context = {
        'formacao': formacao,
        'todas_competencias': Competencia.objects.all(),
    }
    return render(request, 'portfolio/editar_formacao.html', context)

def eliminar_formacao(request, id):
    formacao = get_object_or_404(Formacao, id=id)
    formacao.delete()
    return redirect('percurso')

# ==========================================
# COMPETÊNCIAS (CRUD)
# ==========================================

@login_required
def competencias_view(request):
    if request.method == "POST":
        Competencia.objects.create(
            nome=request.POST.get('nome'), 
            categoria=request.POST.get('categoria'), 
            nivel=request.POST.get('nivel')
        )
        return redirect('competencias')
    return render(request, 'portfolio/competencias.html', {'competencias': Competencia.objects.all()})

def editar_competencia(request, id):
    competencia = get_object_or_404(Competencia, id=id)
    if request.method == "POST":
        competencia.nome = request.POST.get('nome')
        competencia.categoria = request.POST.get('categoria')
        competencia.nivel = request.POST.get('nivel')
        competencia.save()
        return redirect('competencias')
    return render(request, 'portfolio/editar_competencia.html', {'competencia': competencia})

def eliminar_competencia(request, id):
    competencia = get_object_or_404(Competencia, id=id)
    competencia.delete()
    return redirect('competencias')


@login_required
def sobre_view(request):
    tecnologias = Tecnologia.objects.all().order_by('tipo__nome', 'nome')
    makingofs = MakingOf.objects.all().order_by('-id')
    
    context = {
        'tecnologias': tecnologias,
        'makingofs': makingofs,
    }
    return render(request, 'portfolio/sobre.html', context)


