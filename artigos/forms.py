from django import forms
from .models import Artigo, Comentario

class ArtigoForm(forms.ModelForm):
    class Meta:
        model = Artigo
        fields = ['titulo', 'texto', 'fotografia', 'link_externo']

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto']
        widgets = {
            'texto': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Escreva aqui o seu comentário...', 'class': 'form-control rounded-4 border-0 bg-light p-3'})
        }