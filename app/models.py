from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import secrets
import hashlib
from django.utils import timezone
from datetime import timedelta

# Create your models here.

from django.db import models

class HeroContent(models.Model):
    name = models.CharField(max_length=100, default="Arjun K M")
    subtitle = models.CharField(max_length=200, default="I'm a Software Engineer")
    description = models.TextField(default="A passionate Software Engineer specializing in building exceptional digital experiences. Currently focused on creating innovative solutions using modern technologies and best practices.")
    resume = models.FileField(upload_to='resume/', blank=True, null=True)
    about = models.TextField(default="Hi")
    image = models.ImageField(upload_to='images', blank=True, null=True)
    status = models.TextField(default="Updated")

    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Skill(models.Model):    
    CATEGORY_CHOICES = [
        ('Programming Languages', 'Programming Languages'),
        ('Frontend Development', 'Frontend Development'),
        ('Backend Development', 'Backend Development'),
        ('Database', 'Database'),
        ('DevOps & Tools', 'DevOps & Tools'),
        ('Design', 'Design'),
        ('Other', 'Other'),
    ]
    
    name = models.CharField(max_length=100, help_text="Name of the skill or language")
    category = models.CharField(
        max_length=50, 
        choices=CATEGORY_CHOICES,
    )
    icon = models.CharField(
        max_length=50, 
        default='fas fa-code',
    )
    proficiency = models.IntegerField(
        default=50,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    description = models.TextField(
        blank=True, 
        null=True,
    )
    order = models.IntegerField(
        default=0,
    )
    is_active = models.BooleanField(
        default=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='updated_skills'
    )

    class Meta:
        ordering = ['order', '-proficiency', 'name']
        verbose_name = 'Skill'
        verbose_name_plural = 'Skills'

    def __str__(self):
        return f"{self.name} ({self.category})"

    def get_proficiency_level(self):
        if self.proficiency >= 90:
            return "Expert"
        elif self.proficiency >= 75:
            return "Advanced"
        elif self.proficiency >= 50:
            return "Intermediate"
        elif self.proficiency >= 25:
            return "Beginner"
        else:
            return "Learning"

class WorkExperience(models.Model):
    company_name = models.CharField(max_length=200)
    job_title = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField()
    technologies = models.CharField(max_length=500, help_text="Comma-separated technologies")
    company_logo = models.ImageField(upload_to='experience_logos/', null=True, blank=True)
    order = models.IntegerField(default=0, help_text="Display order (lower numbers appear first)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['order', '-start_date']
        verbose_name = 'Work Experience'
        verbose_name_plural = 'Work Experiences'

    def __str__(self):
        return f"{self.job_title} at {self.company_name}"

    def get_duration(self):
        from datetime import date
        end = self.end_date if self.end_date else date.today()
        duration = end - self.start_date
        years = duration.days // 365
        months = (duration.days % 365) // 30
        
        if years > 0 and months > 0:
            return f"{years} year{'s' if years > 1 else ''} {months} month{'s' if months > 1 else ''}"
        elif years > 0:
            return f"{years} year{'s' if years > 1 else ''}"
        else:
            return f"{months} month{'s' if months > 1 else ''}"
