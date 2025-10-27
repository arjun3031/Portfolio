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
from django.shortcuts import get_object_or_404
from django.db.models import Avg, Count


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
            hero.about = request.POST.get('about')
            
            hero.updated_by = request.user
            hero.updated_at = timezone.now()

            if 'resume' in request.FILES:
                hero.resume = request.FILES['resume']

            if 'image' in request.FILES:
                hero.image = request.FILES['image']

            hero.save()
            messages.success(request, 'Content updated successfully!')
        else:
            messages.error(request, 'Content not found!')

        return redirect('managecontent')
    else:
        return redirect('managecontent')

# def manageskills(request):
#     return render(request, 'manageskills.html')

@login_required
def manageskills(request):
    skills = Skill.objects.filter(is_active=True)
    categories = skills.values('category').annotate(count=Count('category'))
    avg_proficiency = skills.aggregate(Avg('proficiency'))['proficiency__avg'] or 0
    
    context = {
        'skills': skills,
        'categories': categories,
        'average_proficiency': avg_proficiency,
    }
    return render(request, 'manageskills.html', context)


@login_required
def add_skill(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            category = request.POST.get('category')
            icon = request.POST.get('icon', 'fas fa-code')
            proficiency = int(request.POST.get('proficiency', 50))
            description = request.POST.get('description', '')
            
            if proficiency < 0 or proficiency > 100:
                messages.error(request, 'Proficiency must be between 0 and 100.')
                return redirect('manageskills')
            
            skill = Skill.objects.create(
                name=name,
                category=category,
                icon=icon,
                proficiency=proficiency,
                description=description,
                updated_by=request.user
            )
            
            messages.success(request, f'Skill "{name}" has been added successfully!')
            
        except Exception as e:
            messages.error(request, f'Error adding skill: {str(e)}')
    
    return redirect('manageskills')


@login_required
def update_skill(request):
    if request.method == 'POST':
        try:
            skill_id = request.POST.get('skill_id')
            skill = get_object_or_404(Skill, id=skill_id)
            
            skill.name = request.POST.get('name')
            skill.category = request.POST.get('category')
            skill.icon = request.POST.get('icon', 'fas fa-code')
            skill.proficiency = int(request.POST.get('proficiency', 50))
            skill.description = request.POST.get('description', '')
            skill.updated_by = request.user
            
            if skill.proficiency < 0 or skill.proficiency > 100:
                messages.error(request, 'Proficiency must be between 0 and 100.')
                return redirect('manageskills')
            
            skill.save()
            
            messages.success(request, f'Skill "{skill.name}" has been updated successfully!')
            
        except Skill.DoesNotExist:
            messages.error(request, 'Skill not found.')
        except Exception as e:
            messages.error(request, f'Error updating skill: {str(e)}')
    
    return redirect('manageskills')


@login_required
def delete_skill(request):
    if request.method == 'POST':
        try:
            skill_id = request.POST.get('skill_id')
            skill = get_object_or_404(Skill, id=skill_id)
            skill_name = skill.name
            
            skill.is_active = False
            skill.updated_by = request.user
            skill.save()
            
            messages.success(request, f'Skill "{skill_name}" has been deleted successfully!')
            
        except Skill.DoesNotExist:
            messages.error(request, 'Skill not found.')
        except Exception as e:
            messages.error(request, f'Error deleting skill: {str(e)}')
    
    return redirect('manageskills')