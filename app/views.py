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
from datetime import datetime


# Create your views here.

def homepage(request):
    hero = HeroContent.objects.last()
    skills = Skill.objects.filter(is_active=True)
    experiences = WorkExperience.objects.all().order_by('order')
    
    skills_list = []
    skills_by_category = {}
    
    for skill in skills:
        skills_list.append({
            'name': skill.name,
            'category': skill.category,
            'proficiency': skill.proficiency,
            'icon': skill.icon
        })
        
        if skill.category not in skills_by_category:
            skills_by_category[skill.category] = []
        skills_by_category[skill.category].append(skill.name)
    
    experiences_list = []
    for exp in experiences:
        experiences_list.append({
            'company': exp.company_name,
            'title': exp.job_title,
            'location': exp.location,
            'start_date': exp.start_date.strftime('%b %Y'),
            'end_date': exp.end_date.strftime('%b %Y') if exp.end_date else 'Present',
            'is_current': exp.is_current,
            'description': exp.description,
            'technologies': exp.technologies
        })
    
    context = {
        'hero': hero,
        'skills': skills,
        'experiences': experiences,
        'chatbot_skills': skills_list,
        'chatbot_skills_by_category': skills_by_category,
        'chatbot_experiences': experiences_list,
    }
    return render(request, 'homepage.html', context)

@login_required(login_url='admin_login')
def adminhome(request):
    from datetime import date
    
    skills_count = Skill.objects.filter(is_active=True).count()
    experiences_count = WorkExperience.objects.all().count()
    projects_count = 0 
    top_skills = Skill.objects.filter(is_active=True).order_by('-proficiency')[:5]
    
    recent_experiences = WorkExperience.objects.all().order_by('-start_date')[:5]
    
    skills_by_category = Skill.objects.filter(is_active=True).values('category').annotate(count=Count('id'))
    
    avg_prof = Skill.objects.filter(is_active=True).aggregate(Avg('proficiency'))
    average_proficiency = avg_prof['proficiency__avg'] or 0
    
    current_experience = WorkExperience.objects.filter(is_current=True).first()
    current_company = current_experience.company_name if current_experience else None
    
    total_months = 0
    for exp in WorkExperience.objects.all():
        start = exp.start_date
        end = exp.end_date if exp.end_date else date.today()
        
        months_diff = (end.year - start.year) * 12 + (end.month - start.month)
        total_months += months_diff
    
    years = total_months // 12
    months = total_months % 12
    
    if years > 0 and months > 0:
        total_duration = f"{years}y {months}m"
    elif years > 0:
        total_duration = f"{years} year{'s' if years > 1 else ''}"
    elif months > 0:
        total_duration = f"{months} month{'s' if months > 1 else ''}"
    else:
        total_duration = "0 months"
    
    last_updated = None
    hero = HeroContent.objects.last()
    if hero and hero.updated_at:
        last_updated = hero.updated_at
    
    context = {
        'skills_count': skills_count,
        'experiences_count': experiences_count,
        'projects_count': projects_count,
        'top_skills': top_skills,
        'recent_experiences': recent_experiences,
        'skills_by_category': skills_by_category,
        'average_proficiency': average_proficiency,
        'current_company': current_company,
        'total_duration': total_duration,
        'last_updated': last_updated,
        'total_views': 0,
    }
    
    return render(request, 'adminhome.html', context)

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

@login_required
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

@login_required
def managecontent(request):
    hero, created = HeroContent.objects.get_or_create(id=1)
    return render(request, 'managecontent.html', {'hero': hero})

@login_required
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

@login_required
def manage_experience(request):
    experiences = WorkExperience.objects.all()
    context = {
        'experiences': experiences
    }
    return render(request, 'manageexperience.html', context)

@login_required
def add_experience(request):
    if request.method == 'POST':
        try:
            # Handle the checkbox for current job
            is_current = request.POST.get('is_current') == 'on'
            
            # Parse dates
            start_date = datetime.strptime(request.POST.get('start_date'), '%Y-%m-%d').date()
            end_date = None
            if not is_current and request.POST.get('end_date'):
                end_date = datetime.strptime(request.POST.get('end_date'), '%Y-%m-%d').date()
            
            # Create new experience
            experience = WorkExperience(
                company_name=request.POST.get('company_name'),
                job_title=request.POST.get('job_title'),
                location=request.POST.get('location'),
                start_date=start_date,
                end_date=end_date,
                is_current=is_current,
                description=request.POST.get('description'),
                technologies=request.POST.get('technologies'),
                order=int(request.POST.get('order', 0)),
                updated_by=request.user
            )
            
            # Handle logo upload
            if request.FILES.get('company_logo'):
                experience.company_logo = request.FILES['company_logo']
            
            experience.save()
            messages.success(request, 'Work experience added successfully!')
            
        except Exception as e:
            messages.error(request, f'Error adding experience: {str(e)}')
    
    return redirect('manage_experience')

@login_required
def update_experience(request, pk):
    if request.method == 'POST':
        try:
            experience = get_object_or_404(WorkExperience, pk=pk)
            
            is_current = request.POST.get('is_current') == 'on'
            
            start_date = datetime.strptime(request.POST.get('start_date'), '%Y-%m-%d').date()
            end_date = None
            if not is_current and request.POST.get('end_date'):
                end_date = datetime.strptime(request.POST.get('end_date'), '%Y-%m-%d').date()
            
            experience.company_name = request.POST.get('company_name')
            experience.job_title = request.POST.get('job_title')
            experience.location = request.POST.get('location')
            experience.start_date = start_date
            experience.end_date = end_date
            experience.is_current = is_current
            experience.description = request.POST.get('description')
            experience.technologies = request.POST.get('technologies')
            experience.order = int(request.POST.get('order', 0))
            experience.updated_by = request.user
            
            if request.FILES.get('company_logo'):
                experience.company_logo = request.FILES['company_logo']
            
            experience.save()
            messages.success(request, 'Work experience updated successfully!')
            
        except Exception as e:
            messages.error(request, f'Error updating experience: {str(e)}')
    
    return redirect('manage_experience')

@login_required
def delete_experience(request, pk):
    if request.method == 'POST':
        try:
            experience = get_object_or_404(WorkExperience, pk=pk)
            experience.delete()
            messages.success(request, 'Work experience deleted successfully!')
        except Exception as e:
            messages.error(request, f'Error deleting experience: {str(e)}')
    
    return redirect('manage_experience')