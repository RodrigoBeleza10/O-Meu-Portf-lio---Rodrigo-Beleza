from django.contrib import admin

from .models import (
     Licenciatura, Professor, UnidadeCurricular, Tecnologia, Competencia, Formacao, Projeto, TFC, MakingOf, Tipo
)

@admin.register(Licenciatura)
class LicenciaturaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ects_totais')
    search_fields = ('nome', 'descricao')

@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'numero', 'email')
    search_fields = ('nome', 'numero', 'email')

@admin.register(UnidadeCurricular)
class UnidadeCurricularAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ano', 'semestre', 'ects', 'licenciatura')
    list_filter = ('ano', 'semestre', 'licenciatura')
    search_fields = ('nome',)

@admin.register(Tecnologia)
class TecnologiaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo','nivel_interesse')
    list_filter = ('tipo','nivel_interesse',)
    search_fields = ('nome', 'detalhes')

@admin.register(Competencia)
class CompetenciaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'nivel')
    list_filter = ('categoria', 'nivel')
    search_fields = ('nome',)

@admin.register(Formacao)
class FormacaoAdmin(admin.ModelAdmin):
    list_display = ('designacao', 'instituicao', 'data_inicio', 'data_fim')
    list_filter = ('instituicao', 'data_inicio')
    search_fields = ('designacao', 'instituicao')

@admin.register(Projeto)
class ProjetoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'uc')
    list_filter = ('uc',)
    search_fields = ('titulo', 'descricao', 'conceitos_aplicados')

@admin.register(TFC)
class TFCAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autores', 'orientador', 'ano', 'destaque') 
    list_filter = ('ano', 'destaque')
    search_fields = ('titulo', 'autores', 'orientador')

@admin.register(MakingOf)
class MakingOfAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'entidade_relacionada', 'data_registo')
    list_filter = ('entidade_relacionada', 'data_registo')
    search_fields = ('titulo', 'descricao_decisoes', 'erros_correcoes')

@admin.register(Tipo)
class TipoAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)