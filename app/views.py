from django.shortcuts import render
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,auth
from django.contrib.auth import update_session_auth_hash
from .models import *
from django.http import JsonResponse
import os
from django.utils import timezone

# Create your views here.

def homepage(request):
    hero = HeroContent.objects.last()
    return render(request, 'homepage.html', {'hero': hero})

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
            messages.error(request, "Invalid username or password.", extra_tags='login')
            return render(request, 'homepage.html', {'show_login_modal': True})
    return render(request, 'homepage.html')

def admin_logout(request):
    auth.logout(request)
    return redirect('homepage')

def change_password(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        messages.error(request, "You are not authorized.", extra_tags='change')
        return redirect('/?modal=change')

    if request.method == 'POST':
        current_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        user = request.user

        if not user.check_password(current_password):
            messages.error(request, 'Current password is incorrect.', extra_tags='change')
            return redirect('/?modal=change')

        if new_password != confirm_password:
            messages.error(request, 'New passwords do not match.', extra_tags='change')
            return redirect('/?modal=change')

        if len(new_password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.', extra_tags='change')
            return redirect('/?modal=change')

        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)

        messages.success(request, 'Password changed successfully! Please login again.', extra_tags='login')
        return redirect('/?modal=login')

    return render(request, 'homepage.html')

def managecontent(request):
    hero, created = HeroContent.objects.get_or_create(id=1)
    return render(request, 'managecontent.html', {'hero': hero})

def update_content(request):
    if request.method == 'POST':
        hero = HeroContent.objects.first()
        if hero:
            hero.name = request.POST.get('name')
            hero.subtitle = request.POST.get('subtitle')
            hero.description = request.POST.get('description')
            hero.updated_by = request.user
            hero.updated_at = timezone.now()

            if 'resume' in request.FILES:
                hero.resume = request.FILES['resume']

            hero.save()
            messages.success(request, 'Content updated successfully!')
        else:
            messages.error(request, 'Content not found!')

        return redirect('managecontent')
    else:
        return redirect('managecontent')