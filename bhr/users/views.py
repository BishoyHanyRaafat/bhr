from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User, Group
from .models import IPAddress
from django.http import HttpResponse
# Create your views here.

def home(request):
    user = request.user
    try:
        user.id
    except:
        return render(request, 'home.html')
    if user:
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
            return redirect('/home')
    else:
        form = RegisterForm()
        
    return render(request, 'registration/sign_up.html', {"form": form})


def favicon(_):
    with open("favicon.ico", "rb") as f:
        return HttpResponse(f.read(), content_type="image/jpeg")