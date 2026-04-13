from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings


class User(AbstractUser):
    CANDIDATE = "candidate"
    RECRUITER = "recruiter"

    ROLE_CHOICES = [
        (CANDIDATE, "Candidate"),
        (RECRUITER, "Recruiter"),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=CANDIDATE)

    def __str__(self):
        return f"{self.username} ({self.role})"


class Profile(models.Model):
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    full_name = models.CharField(max_length=120, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    skills = models.CharField(max_length=250, blank=True)

    resume = models.FileField(upload_to="resumes/", blank=True, null=True)
    profile_pic = models.ImageField(upload_to="profile_pics/", blank=True, null=True)

    experience = models.TextField(blank=True)
    education = models.TextField(blank=True)
    linkedin = models.URLField(blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_profile(sender, instance, created, **kwargs):
    
    Profile.objects.get_or_create(user=instance)