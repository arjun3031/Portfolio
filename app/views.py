from django.shortcuts import render
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,auth
from django.contrib.auth import update_session_auth_hash


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

def change_password(request):
    if not request.user.is_superuser:
        messages.error(request, "You are not authorized.", extra_tags='change')
        return redirect('homepage')

    if request.method == 'POST':
        current_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        user = request.user

        if not user.check_password(current_password):
            messages.error(request, 'Current password is incorrect.', extra_tags='change')
            return redirect('homepage')

        if new_password != confirm_password:
            messages.error(request, 'New passwords do not match.', extra_tags='change')
            return redirect('homepage')

        if len(new_password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.', extra_tags='change')
            return redirect('homepage')

        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)

        messages.success(request, 'Password changed successfully!', extra_tags='change')
        return redirect('homepage')

    return render(request, 'homepage.html')