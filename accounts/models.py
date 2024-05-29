from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    photo_url = models.URLField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

class Contributor(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    contribution = models.TextField(help_text="Detailed description of the contributions made by the individual.")
    title = models.CharField(max_length=255, blank=True, help_text="Professional title of the contributor.")
    area_of_expertise = models.CharField(max_length=255, blank=True, help_text="Area of expertise of the contributor.")
    personal_website = models.URLField(blank=True, null=True, help_text="Personal or professional website URL.")
    linkedin_profile = models.URLField(blank=True, null=True, help_text="LinkedIn profile URL.")
    contact_email = models.EmailField(blank=True, null=True, help_text="Contact email address.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.title}"
