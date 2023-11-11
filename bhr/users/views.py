from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User, Group
from .models import IPAddress
from django.http import HttpResponse
from django.templatetags.static import static
# Create your views here.
def home(request):
    user = request.user

    if user.is_authenticated:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            user_ip = x_forwarded_for.split(',')[-1].strip()
        else:
            user_ip = request.META.get('REMOTE_ADDR')
        
        ip, _ = IPAddress.objects.get_or_create(address=user_ip)
        ip.users.add(user)
    
    return render(request, 'home.html')

def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                user_ip = x_forwarded_for.split(',')[-1].strip()
            else:
                user_ip = request.META.get('REMOTE_ADDR')
            if user_ip:
                ip, _ = IPAddress.objects.get_or_create(address=user_ip)
                ip.users.add(user)
            return redirect('/home')
    else:
        form = RegisterForm()
        
    return render(request, 'registration/sign_up.html', {"form": form})


def favicon(_):
    url=static("favicon.ico")
    return redirect(url)
