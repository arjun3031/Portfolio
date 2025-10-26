from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# models.py
from django.db import models

class HeroContent(models.Model):
    name = models.CharField(max_length=100, default="Arjun K M")
    subtitle = models.CharField(max_length=200, default="I'm a Software Engineer")
    description = models.TextField(default="A passionate Software Engineer specializing in building exceptional digital experiences. Currently focused on creating innovative solutions using modern technologies and best practices.")
    resume = models.FileField(upload_to='resume/', blank=True, null=True)

    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
