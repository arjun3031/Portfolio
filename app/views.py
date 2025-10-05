from django.shortcuts import render
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.

def homepage(request):
    return render(request,'homepage.html')

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        subject = f"New Contact Form Submission from {name}"
        body = f"""
        You have received a new message from your portfolio site.

        Name: {name}
        Email: {email}
        Message:
        {message}
        """

        try:
            send_mail(
                subject,
                body,
                email,  # sender
                ['arjunkm202@gmail.com'],  # your email (receiver)
                fail_silently=False,
            )
            messages.success(request, "Thank you for your message! I will get back to you soon.")
        except Exception as e:
            messages.error(request, f"Error sending message: {e}")

        return redirect('contact')
    return render(request, 'homepage.html')
