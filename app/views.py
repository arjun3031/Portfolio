from django.shortcuts import render
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,auth


# Create your views here.

def homepage(request):
    return render(request,'homepage.html')

@login_required(login_url='admin_login')
def adminhome(request):
    return render(request,'adminhome.html')

def admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('adminhome')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'homepage.html')

def admin_logout(request):
    auth.logout(request)
    return redirect('homepage')