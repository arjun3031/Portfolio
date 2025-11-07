# app/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse, HttpResponseRedirect
from django.db.models import Avg, Count
from django.utils import timezone
from datetime import datetime, date
import os
import re
import logging
from django.db import models
from datetime import timedelta
from axes.decorators import axes_dispatch
from axes.helpers import get_client_ip_address, get_failure_limit
from axes.models import AccessAttempt
from .models import *
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.urls import reverse
from axes.helpers import get_client_ip_address

logger = logging.getLogger('app')

def sanitize_input(text, max_length=150):
    if not text:
        return ""
    
    text = text.strip()
    text = re.sub(r'[;\'"\\]', '', text)
    text = text[:max_length] 
    return text

def get_homepage_context():
    try:
        hero = HeroContent.objects.last()
    except Exception as e:
        logger.error(f"Error fetching hero data: {str(e)}")
        hero = None
    
    try:
        skills = Skill.objects.filter(is_active=True)
    except Exception as e:
        logger.error(f"Error fetching skills: {str(e)}")
        skills = []
    
    try:
        experiences = WorkExperience.objects.all().order_by('order')
    except Exception as e:
        logger.error(f"Error fetching experiences: {str(e)}")
        experiences = []

    try:
        projects = Project.objects.filter(is_active=True, is_featured=True).order_by('order')
    except Exception as e:
        logger.error(f"Error fetching projects: {str(e)}")
        projects = []

    try:
        educations = Education.objects.all().order_by('order')
    except Exception as e:
        logger.error(f"Error fetching education: {str(e)}")
        educations = []
    
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
    
    projects_list = []
    for project in projects:
        projects_list.append({
            'title': project.title,
            'description': project.description,
            'technologies': project.get_tech_list(),
            'status': project.get_status_display(),
            'github_url': project.github_url,
            'demo_url': project.demo_url,
        })

    context = {
        'hero': hero,
        'skills': skills,
        'experiences': experiences,
        'projects': projects,
        'educations': educations,
        'chatbot_skills': skills_list,
        'chatbot_skills_by_category': skills_by_category,
        'chatbot_experiences': experiences_list,
        'chatbot_projects': projects_list,
    }
    return context

@never_cache
def homepage(request):
    context = get_homepage_context()
    return render(request, 'homepage.html', context)


@never_cache
@csrf_protect
@axes_dispatch
def admin_login(request):
    from datetime import timedelta
    from django.utils import timezone
    
    ip_address = get_client_ip_address(request)
    
    if request.user.is_authenticated:
        return redirect('adminhome')
    
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        
        if not username or not password:
            messages.error(
                request, 
                "Username and password are required.", 
                extra_tags='login'
            )
            logger.warning(f"Empty login attempt from IP: {ip_address}")
            context = get_homepage_context()
            context['show_login_modal'] = True
            return render(request, 'homepage.html', context)
        
        username = sanitize_input(username, max_length=150)
        
        if len(username) < 3:
            messages.error(
                request,
                "Invalid username format.",
                extra_tags='login'
            )
            context = get_homepage_context()
            context['show_login_modal'] = True
            return render(request, 'homepage.html', context)
        
        logger.info(f"Login attempt for username: {username} from IP: {ip_address}")
        
        try:
            user = authenticate(request, username=username, password=password)
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            messages.error(
                request,
                "An error occurred. Please try again.",
                extra_tags='login'
            )
            context = get_homepage_context()
            context['show_login_modal'] = True
            return render(request, 'homepage.html', context)
        
        if user is not None:
            if not user.is_superuser:
                logger.warning(f"Non-superuser login attempt: {username} from IP: {ip_address}")
                messages.error(
                    request,
                    "You do not have permission to access this area.",
                    extra_tags='login'
                )
                context = get_homepage_context()
                context['show_login_modal'] = True
                return render(request, 'homepage.html', context)
            
            if not user.is_active:
                logger.warning(f"Inactive user login attempt: {username} from IP: {ip_address}")
                messages.error(
                    request,
                    "This account has been deactivated.",
                    extra_tags='login'
                )
                context = get_homepage_context()
                context['show_login_modal'] = True
                return render(request, 'homepage.html', context)
            
            login(request, user)
            
            request.session['login_ip'] = ip_address
            request.session['user_agent'] = request.META.get('HTTP_USER_AGENT', '')
            request.session['login_time'] = str(timezone.now())
            request.session.set_expiry(3600)
            request.session.cycle_key()
            
            logger.info(f"✓ Successful login: {username} from IP: {ip_address}")
            
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            return redirect('adminhome')
        
        else:
            try:
                cooloff_time = timezone.now() - timedelta(hours=1)
                
                attempts = AccessAttempt.objects.filter(
                    ip_address=ip_address,
                    attempt_time__gte=cooloff_time
                ).aggregate(total_failures=models.Sum('failures_since_start'))
                
                current_attempts = (attempts['total_failures'] or 0) + 1
                
            except Exception as e:
                logger.error(f"Error checking login attempts: {str(e)}")
                current_attempts = 1
            
            failure_limit = get_failure_limit(request, None)
            remaining_attempts = max(0, failure_limit - current_attempts)
            
            if remaining_attempts > 0:
                messages.error(
                    request,
                    f"Invalid username or password. {remaining_attempts} attempt(s) remaining.",
                    extra_tags='login'
                )
                logger.warning(
                    f"✗ Failed login attempt {current_attempts}/{failure_limit}: "
                    f"{username} from IP: {ip_address}"
                )
                context = get_homepage_context()
                context['show_login_modal'] = True
                return render(request, 'homepage.html', context)
            else:
                messages.error(
                    request,
                    "Too many failed login attempts. Your account has been locked for 1 hour.",
                    extra_tags='login locked'
                )
                logger.warning(
                    f"⚠ ACCOUNT LOCKED: {username} from IP: {ip_address} "
                    f"after {failure_limit} failed attempts"
                )
                context = get_homepage_context()
                context['show_locked_modal'] = True
                return render(request, 'homepage.html', context)
    
    return redirect('homepage')


def account_locked(request):
    context = get_homepage_context()
    context['show_locked_modal'] = True
    return render(request, 'homepage.html', context)


@login_required(login_url='admin_login')
@never_cache
def admin_logout(request):
    username = request.user.username
    ip_address = get_client_ip_address(request)
    
    logger.info(f"User logout: {username} from IP: {ip_address}")
    
    request.session.flush()
    
    auth.logout(request)
    
    messages.success(request, "You have been successfully logged out.")
    return redirect('homepage')


@never_cache
def csrf_failure(request, reason=""):
    ip_address = get_client_ip_address(request)
    logger.warning(f"CSRF failure: {reason} from IP: {ip_address}")
    
    messages.error(request, "Security token expired. Please refresh the page and try again.")
    return redirect('homepage')

@login_required(login_url='admin_login')
@never_cache
def adminhome(request):
    if not request.user.is_superuser:
        messages.error(request, "You do not have permission to access this area.")
        return redirect('homepage')
    
    skills_count = Skill.objects.filter(is_active=True).count()
    experiences_count = WorkExperience.objects.all().count()
    projects_count = Project.objects.filter(is_active=True).count()
    top_skills = Skill.objects.filter(is_active=True).order_by('-proficiency')[:5]
    
    recent_experiences = WorkExperience.objects.all().order_by('-start_date')[:5]
    recent_projects = Project.objects.filter(is_active=True).order_by('-created_at')[:5]
    
    skills_by_category = Skill.objects.filter(is_active=True).values('category').annotate(count=Count('category'))
    
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
        'recent_projects': recent_projects,
        'skills_by_category': skills_by_category,
        'average_proficiency': average_proficiency,
        'current_company': current_company,
        'total_duration': total_duration,
        'last_updated': last_updated,
        'total_views': 0,
    }
    
    return render(request, 'adminhome.html', context)


@login_required(login_url='admin_login')
@never_cache
def change_password(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    
    if request.method == 'POST':
        old_password = request.POST.get('old_password', '').strip()
        new_password = request.POST.get('new_password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()
        
        ip_address = get_client_ip_address(request)
        
        if not old_password or not new_password or not confirm_password:
            messages.error(request, 'All fields are required.', extra_tags='change')
            logger.warning(f"Password change failed - empty fields: {request.user.username} from IP: {ip_address}")
            return HttpResponseRedirect('/adminhome/?modal=change')
        
        if not request.user.check_password(old_password):
            messages.error(request, 'Current password is incorrect.', extra_tags='change')
            logger.warning(f"Password change failed - wrong password: {request.user.username} from IP: {ip_address}")
            return HttpResponseRedirect('/adminhome/?modal=change')
        
        if new_password != confirm_password:
            messages.error(request, 'New passwords do not match.', extra_tags='change')
            return HttpResponseRedirect('/adminhome/?modal=change')
        
        if len(new_password) < 10:
            messages.error(request, 'Password must be at least 10 characters long.', extra_tags='change')
            return HttpResponseRedirect('/adminhome/?modal=change')
        
        if old_password == new_password:
            messages.error(request, 'New password must be different from current password.', extra_tags='change')
            return HttpResponseRedirect('/adminhome/?modal=change')
        
        if not any(char.isdigit() for char in new_password):
            messages.error(request, 'Password must contain at least one number.', extra_tags='change')
            return HttpResponseRedirect('/adminhome/?modal=change')
        
        if not any(char.isupper() for char in new_password):
            messages.error(request, 'Password must contain at least one uppercase letter.', extra_tags='change')
            return HttpResponseRedirect('/adminhome/?modal=change')
        
        request.user.set_password(new_password)
        request.user.save()
        
        logger.info(f"✓ Password changed successfully: {request.user.username} from IP: {ip_address}")
        
        request.session.flush()
        
        messages.success(request, 'Password changed successfully! Please login again.', extra_tags='login')
        return redirect('admin_login')
    
    return redirect('adminhome')

@login_required(login_url='admin_login')
@never_cache
def managecontent(request):
    if not request.user.is_superuser:
        messages.error(request, "You do not have permission to access this area.")
        return redirect('homepage')
    
    hero, created = HeroContent.objects.get_or_create(id=1)
    return render(request, 'managecontent.html', {'hero': hero})


@login_required(login_url='admin_login')
@never_cache
@csrf_protect
def update_content(request):
    if not request.user.is_superuser:
        messages.error(request, "You do not have permission to perform this action.")
        return redirect('homepage')
    
    if request.method == 'POST':
        hero = HeroContent.objects.first()
        if hero:
            hero.name = sanitize_input(request.POST.get('name', ''), 200)
            hero.subtitle = sanitize_input(request.POST.get('subtitle', ''), 300)
            hero.description = request.POST.get('description', '')[:1000]
            hero.about = request.POST.get('about', '')[:2000]
            
            hero.updated_by = request.user
            hero.updated_at = timezone.now()

            if 'resume' in request.FILES:
                hero.resume = request.FILES['resume']

            if 'image' in request.FILES:
                hero.image = request.FILES['image']

            hero.save()
            
            logger.info(f"Content updated by: {request.user.username}")
            messages.success(request, 'Content updated successfully!')
        else:
            messages.error(request, 'Content not found!')

        return redirect('managecontent')
    else:
        return redirect('managecontent')

@login_required(login_url='admin_login')
@never_cache
def manageskills(request):
    if not request.user.is_superuser:
        messages.error(request, "You do not have permission to access this area.")
        return redirect('homepage')
    
    skills = Skill.objects.filter(is_active=True)
    categories = skills.values('category').annotate(count=Count('category'))
    avg_proficiency = skills.aggregate(Avg('proficiency'))['proficiency__avg'] or 0
    
    context = {
        'skills': skills,
        'categories': categories,
        'average_proficiency': avg_proficiency,
    }
    return render(request, 'manageskills.html', context)


@login_required(login_url='admin_login')
@csrf_protect
def add_skill(request):
    if not request.user.is_superuser:
        messages.error(request, "You do not have permission to perform this action.")
        return redirect('homepage')
    
    if request.method == 'POST':
        try:
            name = sanitize_input(request.POST.get('name', ''), 100)
            category = sanitize_input(request.POST.get('category', ''), 50)
            icon = request.POST.get('icon', 'fas fa-code')[:100]
            proficiency = int(request.POST.get('proficiency', 50))
            description = request.POST.get('description', '')[:500]
            
            if proficiency < 0 or proficiency > 100:
                messages.error(request, 'Proficiency must be between 0 and 100.')
                return redirect('manageskills')
            
            if not name or not category:
                messages.error(request, 'Name and category are required.')
                return redirect('manageskills')
            
            skill = Skill.objects.create(
                name=name,
                category=category,
                icon=icon,
                proficiency=proficiency,
                description=description,
                updated_by=request.user
            )
            
            logger.info(f"Skill added: {name} by {request.user.username}")
            messages.success(request, f'Skill "{name}" has been added successfully!')
            
        except ValueError:
            messages.error(request, 'Invalid proficiency value.')
        except Exception as e:
            logger.error(f"Error adding skill: {str(e)}")
            messages.error(request, f'Error adding skill: {str(e)}')
    
    return redirect('manageskills')


@login_required(login_url='admin_login')
@csrf_protect
def update_skill(request):
    if not request.user.is_superuser:
        messages.error(request, "You do not have permission to perform this action.")
        return redirect('homepage')
    
    if request.method == 'POST':
        try:
            skill_id = request.POST.get('skill_id')
            skill = get_object_or_404(Skill, id=skill_id)           
            skill.name = sanitize_input(request.POST.get('name', ''), 100)
            skill.category = sanitize_input(request.POST.get('category', ''), 50)
            skill.icon = request.POST.get('icon', 'fas fa-code')[:100]
            skill.proficiency = int(request.POST.get('proficiency', 50))
            skill.description = request.POST.get('description', '')[:500]
            skill.updated_by = request.user
            
            if skill.proficiency < 0 or skill.proficiency > 100:
                messages.error(request, 'Proficiency must be between 0 and 100.')
                return redirect('manageskills')
            
            skill.save()
            
            logger.info(f"Skill updated: {skill.name} by {request.user.username}")
            messages.success(request, f'Skill "{skill.name}" has been updated successfully!')
            
        except Skill.DoesNotExist:
            messages.error(request, 'Skill not found.')
        except ValueError:
            messages.error(request, 'Invalid proficiency value.')
        except Exception as e:
            logger.error(f"Error updating skill: {str(e)}")
            messages.error(request, f'Error updating skill: {str(e)}')
    
    return redirect('manageskills')


@login_required(login_url='admin_login')
@csrf_protect
def delete_skill(request):
    if not request.user.is_superuser:
        messages.error(request, "You do not have permission to perform this action.")
        return redirect('homepage')
    
    if request.method == 'POST':
        try:
            skill_id = request.POST.get('skill_id')
            skill = get_object_or_404(Skill, id=skill_id)
            skill_name = skill.name
            
            skill.is_active = False
            skill.updated_by = request.user
            skill.save()
            
            logger.info(f"Skill deleted: {skill_name} by {request.user.username}")
            messages.success(request, f'Skill "{skill_name}" has been deleted successfully!')
            
        except Skill.DoesNotExist:
            messages.error(request, 'Skill not found.')
        except Exception as e:
            logger.error(f"Error deleting skill: {str(e)}")
            messages.error(request, f'Error deleting skill: {str(e)}')
    
    return redirect('manageskills')

@login_required(login_url='admin_login')
@never_cache
def manage_experience(request):
    if not request.user.is_superuser:
        messages.error(request, "You do not have permission to access this area.")
        return redirect('homepage')
    
    experiences = WorkExperience.objects.all()
    context = {
        'experiences': experiences
    }
    return render(request, 'manageexperience.html', context)


@login_required(login_url='admin_login')
@csrf_protect
def add_experience(request):
    if not request.user.is_superuser:
        messages.error(request, "You do not have permission to perform this action.")
        return redirect('homepage')
    
    if request.method == 'POST':
        try:
            is_current = request.POST.get('is_current') == 'on'
            start_date = datetime.strptime(request.POST.get('start_date'), '%Y-%m-%d').date()
            end_date = None
            if not is_current and request.POST.get('end_date'):
                end_date = datetime.strptime(request.POST.get('end_date'), '%Y-%m-%d').date()
            
            company_name = sanitize_input(request.POST.get('company_name', ''), 200)
            job_title = sanitize_input(request.POST.get('job_title', ''), 200)
            location = sanitize_input(request.POST.get('location', ''), 200)
            
            if not company_name or not job_title:
                messages.error(request, 'Company name and job title are required.')
                return redirect('manage_experience')

            
            experience = WorkExperience(
                company_name=company_name,
                job_title=job_title,
                location=location,
                start_date=start_date,
                end_date=end_date,
                is_current=is_current,
                description=request.POST.get('description', '')[:1000],
                technologies=request.POST.get('technologies', '')[:500],
                order=int(request.POST.get('order', 0)),
                updated_by=request.user
            )
            
            if request.FILES.get('company_logo'):
                experience.company_logo = request.FILES['company_logo']
            
            experience.save()
            
            logger.info(f"Experience added: {company_name} by {request.user.username}")
            messages.success(request, 'Work experience added successfully!')
            
        except ValueError as e:
            messages.error(request, f'Invalid date format: {str(e)}')
        except Exception as e:
            logger.error(f"Error adding experience: {str(e)}")
            messages.error(request, f'Error adding experience: {str(e)}')
    
    return redirect('manage_experience')


@login_required(login_url='admin_login')
@csrf_protect
def update_experience(request, pk):
    if not request.user.is_superuser:
        messages.error(request, "You do not have permission to perform this action.")
        return redirect('homepage')
    
    if request.method == 'POST':
        try:
            experience = get_object_or_404(WorkExperience, pk=pk)
            
            is_current = request.POST.get('is_current') == 'on'
            
            start_date = datetime.strptime(request.POST.get('start_date'), '%Y-%m-%d').date()
            end_date = None
            if not is_current and request.POST.get('end_date'):
                end_date = datetime.strptime(request.POST.get('end_date'), '%Y-%m-%d').date()
            
            experience.company_name = sanitize_input(request.POST.get('company_name', ''), 200)
            experience.job_title = sanitize_input(request.POST.get('job_title', ''), 200)
            experience.location = sanitize_input(request.POST.get('location', ''), 200)
            experience.start_date = start_date
            experience.end_date = end_date
            experience.is_current = is_current
            experience.description = request.POST.get('description', '')[:1000]
            experience.technologies = request.POST.get('technologies', '')[:500]
            experience.order = int(request.POST.get('order', 0))
            experience.updated_by = request.user
            
            if request.FILES.get('company_logo'):
                experience.company_logo = request.FILES['company_logo']
            
            experience.save()
            
            logger.info(f"Experience updated: {experience.company_name} by {request.user.username}")
            messages.success(request, 'Work experience updated successfully!')
            
        except ValueError as e:
            messages.error(request, f'Invalid date format: {str(e)}')
        except Exception as e:
            logger.error(f"Error updating experience: {str(e)}")
            messages.error(request, f'Error updating experience: {str(e)}')
    
    return redirect('manage_experience')


@login_required(login_url='admin_login')
@csrf_protect
def delete_experience(request, pk):
    if not request.user.is_superuser:
        messages.error(request, "You do not have permission to perform this action.")
        return redirect('homepage')
    
    if request.method == 'POST':
        try:
            experience = get_object_or_404(WorkExperience, pk=pk)
            company_name = experience.company_name
            experience.delete()
            
            logger.info(f"Experience deleted: {company_name} by {request.user.username}")
            messages.success(request, 'Work experience deleted successfully!')
        except Exception as e:
            logger.error(f"Error deleting experience: {str(e)}")
            messages.error(request, f'Error deleting experience: {str(e)}')

@login_required(login_url='admin_login')
@never_cache
def manage_projects(request):
    if not request.user.is_superuser:
        messages.error(request, "You do not have permission to access this area.")
        return redirect('homepage')
    
    projects = Project.objects.filter(is_active=True)
    context = {
        'projects': projects
    }
    return render(request, 'manageprojects.html', context)


@login_required(login_url='admin_login')
@csrf_protect
def add_project(request):
    if not request.user.is_superuser:
        messages.error(request, "You do not have permission to perform this action.")
        return redirect('homepage')
    
    if request.method == 'POST':
        try:
            title = sanitize_input(request.POST.get('title', ''), 200)
            description = request.POST.get('description', '')[:1000]
            detailed_description = request.POST.get('detailed_description', '')[:5000]
            technologies = request.POST.get('technologies', '')[:500]
            icon_class = request.POST.get('icon_class', 'fas fa-project-diagram')[:100]
            status = request.POST.get('status', 'completed')
            
            if not title:
                messages.error(request, 'Project title is required.')
                return redirect('manage_projects')
            
            project = Project(
                title=title,
                description=description,
                detailed_description=detailed_description,
                technologies=technologies,
                project_url=request.POST.get('project_url', ''),
                github_url=request.POST.get('github_url', ''),
                demo_url=request.POST.get('demo_url', ''),
                icon_class=icon_class,
                status=status,
                order=int(request.POST.get('order', 0)),
                is_featured=request.POST.get('is_featured') == 'on',
                updated_by=request.user
            )
            
            if request.POST.get('start_date'):
                project.start_date = datetime.strptime(request.POST.get('start_date'), '%Y-%m-%d').date()
            if request.POST.get('end_date'):
                project.end_date = datetime.strptime(request.POST.get('end_date'), '%Y-%m-%d').date()
            
            if request.FILES.get('image'):
                project.image = request.FILES['image']
            
            project.save()
            
            logger.info(f"Project added: {title} by {request.user.username}")
            messages.success(request, f'Project "{title}" has been added successfully!')
            
        except ValueError as e:
            messages.error(request, f'Invalid date format: {str(e)}')
        except Exception as e:
            logger.error(f"Error adding project: {str(e)}")
            messages.error(request, f'Error adding project: {str(e)}')
    
    return redirect('manage_projects')


@login_required(login_url='admin_login')
@csrf_protect
def update_project(request, pk):
    if not request.user.is_superuser:
        messages.error(request, "You do not have permission to perform this action.")
        return redirect('homepage')
    
    if request.method == 'POST':
        try:
            project = get_object_or_404(Project, pk=pk)
            
            project.title = sanitize_input(request.POST.get('title', ''), 200)
            project.description = request.POST.get('description', '')[:1000]
            project.detailed_description = request.POST.get('detailed_description', '')[:5000]
            project.technologies = request.POST.get('technologies', '')[:500]
            project.project_url = request.POST.get('project_url', '')
            project.github_url = request.POST.get('github_url', '')
            project.demo_url = request.POST.get('demo_url', '')
            project.icon_class = request.POST.get('icon_class', 'fas fa-project-diagram')[:100]
            project.status = request.POST.get('status', 'completed')
            project.order = int(request.POST.get('order', 0))
            project.is_featured = request.POST.get('is_featured') == 'on'
            project.updated_by = request.user
            
            if request.POST.get('start_date'):
                project.start_date = datetime.strptime(request.POST.get('start_date'), '%Y-%m-%d').date()
            if request.POST.get('end_date'):
                project.end_date = datetime.strptime(request.POST.get('end_date'), '%Y-%m-%d').date()
            
            if request.FILES.get('image'):
                project.image = request.FILES['image']
            
            project.save()
            
            logger.info(f"Project updated: {project.title} by {request.user.username}")
            messages.success(request, f'Project "{project.title}" has been updated successfully!')
            
        except ValueError as e:
            messages.error(request, f'Invalid date format: {str(e)}')
        except Exception as e:
            logger.error(f"Error updating project: {str(e)}")
            messages.error(request, f'Error updating project: {str(e)}')
    
    return redirect('manage_projects')


@login_required(login_url='admin_login')
@csrf_protect
def delete_project(request, pk):
    if not request.user.is_superuser:
        messages.error(request, "You do not have permission to perform this action.")
        return redirect('homepage')
    
    if request.method == 'POST':
        try:
            project = get_object_or_404(Project, pk=pk)
            project_title = project.title
            
            project.is_active = False
            project.updated_by = request.user
            project.save()
            
            logger.info(f"Project deleted: {project_title} by {request.user.username}")
            messages.success(request, f'Project "{project_title}" has been deleted successfully!')
        except Exception as e:
            logger.error(f"Error deleting project: {str(e)}")
            messages.error(request, f'Error deleting project: {str(e)}')
    
    return redirect('manage_projects')

@login_required(login_url='admin_login')
@never_cache
def manage_education(request):
    if not request.user.is_superuser:
        messages.error(request, "You do not have permission to access this area.")
        return redirect('homepage')
    
    educations = Education.objects.all().order_by('order')
    context = {
        'educations': educations
    }
    return render(request, 'manageeducation.html', context)


@login_required(login_url='admin_login')
@csrf_protect
def add_education(request):
    if not request.user.is_superuser:
        messages.error(request, "You do not have permission to perform this action.")
        return redirect('homepage')
    
    if request.method == 'POST':
        try:
            degree = sanitize_input(request.POST.get('degree', ''), 100)
            institution = sanitize_input(request.POST.get('institution', ''), 200)
            board_or_university = sanitize_input(request.POST.get('board_or_university', ''), 200)
            
            if not degree or not institution:
                messages.error(request, 'Degree and institution are required.')
                return redirect('manage_education')
            
            education = Education(
                degree=degree,
                institution=institution,
                board_or_university=board_or_university,
                start_year=request.POST.get('start_year', '')[:10],
                end_year=request.POST.get('end_year', '')[:10],
                description=request.POST.get('description', '')[:1000],
                order=int(request.POST.get('order', 0)),
                updated_by=request.user
            )
            
            education.save()
            
            logger.info(f"Education added: {degree} by {request.user.username}")
            messages.success(request, f'Education "{degree}" has been added successfully!')
            
        except Exception as e:
            logger.error(f"Error adding education: {str(e)}")
            messages.error(request, f'Error adding education: {str(e)}')
    
    return redirect('manage_education')


@login_required(login_url='admin_login')
@csrf_protect
def update_education(request, pk):
    if not request.user.is_superuser:
        messages.error(request, "You do not have permission to perform this action.")
        return redirect('homepage')
    
    if request.method == 'POST':
        try:
            education = get_object_or_404(Education, pk=pk)
            
            education.degree = sanitize_input(request.POST.get('degree', ''), 100)
            education.institution = sanitize_input(request.POST.get('institution', ''), 200)
            education.board_or_university = sanitize_input(request.POST.get('board_or_university', ''), 200)
            education.start_year = request.POST.get('start_year', '')[:10]
            education.end_year = request.POST.get('end_year', '')[:10]
            education.description = request.POST.get('description', '')[:1000]
            education.order = int(request.POST.get('order', 0))
            education.updated_by = request.user
            
            education.save()
            
            logger.info(f"Education updated: {education.degree} by {request.user.username}")
            messages.success(request, f'Education "{education.degree}" has been updated successfully!')
            
        except Exception as e:
            logger.error(f"Error updating education: {str(e)}")
            messages.error(request, f'Error updating education: {str(e)}')
    
    return redirect('manage_education')


@login_required(login_url='admin_login')
@csrf_protect
def delete_education(request, pk):
    if not request.user.is_superuser:
        messages.error(request, "You do not have permission to perform this action.")
        return redirect('homepage')
    
    if request.method == 'POST':
        try:
            education = get_object_or_404(Education, pk=pk)
            degree_name = education.degree
            education.delete()
            
            logger.info(f"Education deleted: {degree_name} by {request.user.username}")
            messages.success(request, f'Education "{degree_name}" has been deleted successfully!')
        except Exception as e:
            logger.error(f"Error deleting education: {str(e)}")
            messages.error(request, f'Error deleting education: {str(e)}')
    
    return redirect('manage_education')