from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegistoForm

from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.models import Group # Import adicionado no topo

def login_view(request):
    if request.method == "POST":
        user = authenticate(
            request, 
            username=request.POST.get('username'), 
            password=request.POST.get('password')
        )
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Utilizador ou password inválidos.")
    
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def registo_view(request):
    form = RegistoForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            
            grupo_autores, created = Group.objects.get_or_create(name='autores')
            user.groups.add(grupo_autores)
            
            messages.success(request, "Conta criada com sucesso! Faça login.")
            return redirect('login')
    
    return render(request, 'accounts/registo.html', {'form': form})

def pedir_magic_link(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            signer = TimestampSigner()
            
            token = signer.sign(user.id)
            
            link = request.build_absolute_uri(reverse('magic_link_login', args=[token]))
            
            # Print no terminal para ajudar a copiar o link facilmente nos testes
            print("\n" + "="*50)
            print(f"LINK MÁGICO GERADO PARA: {email}")
            print(f"{link}")
            print("="*50 + "\n")
            
            send_mail(
                subject='O seu Link Mágico de Acesso',
                message=f'Olá {user.first_name},\n\nClique no link abaixo para entrar na sua conta sem usar password:\n\n{link}\n\nEste link expira em 15 minutos.',
                from_email='noreply@portfoliogestao.com',
                recipient_list=[email],
                fail_silently=False,
            )
        except User.DoesNotExist:
            print(f"ERRO: Tentativa de login mágico com email não registado: {email}")
            pass
        
        messages.success(request, "Se o email estiver registado, receberá um link mágico na sua caixa de entrada em breves segundos!")
        return redirect('login')

def magic_link_login(request, token):
    signer = TimestampSigner()
    try:
        user_id = signer.unsign(token, max_age=900)
        user = User.objects.get(id=user_id)
        
        # --- A MAGIA ACONTECE AQUI: Forçar o Django a reconhecer o modelo de autenticação ---
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        
        # Iniciar a sessão
        login(request, user)
        messages.success(request, f"Autenticação mágica efetuada com sucesso! Bem-vindo(a), {user.first_name}.")
        
        # --- CORRIGIDO: Redirecionar para 'home' em vez de 'projetos' ---
        return redirect('home')
        
    except SignatureExpired:
        messages.error(request, "O link mágico expirou. Por favor, peça um novo.")
    except (BadSignature, User.DoesNotExist):
        messages.error(request, "Link mágico inválido ou corrompido.")
        
    return redirect('login')