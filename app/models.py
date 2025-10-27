from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.

# models.py
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
