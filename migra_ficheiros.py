import os
import django
from django.core.files import File

from artigos.models import Artigo 
from portfolio.models import UnidadeCurricular, Tecnologia, Projeto, MakingOf

from django.conf import settings

# 2. ADAPTAR AQUI: usar o teu modelo
for obj in Artigo.objects.all():
    
    # 3. ADAPTAR AQUI: usar o nome do teu campo (ex: fotografia em vez de imagem)
    if obj.fotografia and obj.fotografia.name: 
        local_path = os.path.join(settings.MEDIA_ROOT, obj.fotografia.name)
        
        if os.path.exists(local_path):
            with open(local_path, 'rb') as f:
                
                # 4. ADAPTAR AQUI TAMBÉM: o nome do teu campo
                obj.fotografia.save(
                    os.path.basename(local_path),
                    File(f),
                    save=True
                )
            print(f"Migrado: {obj}")


# Configuração necessária se correres o script diretamente no terminal
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings') # Substitui 'project' pelo nome da tua pasta de settings se for diferente
django.setup()

print("A iniciar migração de imagens...")

# 1. Migrar Unidades Curriculares
print("\n--- A procurar Unidades Curriculares ---")
for obj in UnidadeCurricular.objects.all():
    if obj.imagem and obj.imagem.name:
        local_path = os.path.join(settings.MEDIA_ROOT, obj.imagem.name)
        if os.path.exists(local_path):
            with open(local_path, 'rb') as f:
                obj.imagem.save(os.path.basename(local_path), File(f), save=True)
            print(f" Migrada UC: {obj}")

# 2. Migrar Tecnologias
print("\n--- A procurar Tecnologias ---")
for obj in Tecnologia.objects.all():
    if obj.logo and obj.logo.name:
        local_path = os.path.join(settings.MEDIA_ROOT, obj.logo.name)
        if os.path.exists(local_path):
            with open(local_path, 'rb') as f:
                obj.logo.save(os.path.basename(local_path), File(f), save=True)
            print(f" Migrada Tecnologia: {obj}")

# 3. Migrar Projetos
print("\n--- A procurar Projetos ---")
for obj in Projeto.objects.all():
    if obj.imagem and obj.imagem.name:
        local_path = os.path.join(settings.MEDIA_ROOT, obj.imagem.name)
        if os.path.exists(local_path):
            with open(local_path, 'rb') as f:
                obj.imagem.save(os.path.basename(local_path), File(f), save=True)
            print(f" Migrado Projeto: {obj}")

# 4. Migrar Making Of
print("\n--- A procurar Making Of ---")
for obj in MakingOf.objects.all():
    if obj.fotografia_caderno and obj.fotografia_caderno.name:
        local_path = os.path.join(settings.MEDIA_ROOT, obj.fotografia_caderno.name)
        if os.path.exists(local_path):
            with open(local_path, 'rb') as f:
                obj.fotografia_caderno.save(os.path.basename(local_path), File(f), save=True)
            print(f" Migrado MakingOf: {obj}")

print("\n🎉 Migração terminada!")