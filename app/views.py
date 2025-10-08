from django.shortcuts import render
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.

def homepage(request):
    return render(request,'homepage.html')


