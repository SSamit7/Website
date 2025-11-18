from django.db import models
from django.urls import reverse

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    long_description = models.TextField(blank=True, null=True, help_text="Detailed description for project detail page")
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    link = models.URLField()
    github_link = models.URLField(blank=True, null=True, help_text="Link to GitHub repository")
    technologies = models.TextField(default='', help_text="Comma-separated technologies")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('main:project_detail', kwargs={'pk': self.pk})
    
    def get_technologies(self):
        return [t.strip() for t in self.technologies.split(',') if t.strip()]


class Skill(models.Model):
    CATEGORIES = (
        ('backend', 'Backend'),
        ('frontend', 'Frontend'),
        ('tools', 'Tools & Platforms'),
    )
    
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORIES)
    proficiency = models.IntegerField(default=80, help_text="0-100")
    
    class Meta:
        ordering = ['category', '-proficiency']

    def __str__(self):
        return f"{self.name} ({self.proficiency}%)"


class Experience(models.Model):
    position = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.position} at {self.company}"


class SocialLink(models.Model):
    platform = models.CharField(max_length=50)
    url = models.URLField()
    icon = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.platform


# NEW MODELS - ADD THESE

class ProfileDetails(models.Model):
    """Manage your portfolio profile information"""
    
    full_name = models.CharField(max_length=200)
    title = models.CharField(max_length=200, help_text="e.g., Full Stack Developer")
    bio = models.TextField(help_text="Short bio for the about page")
    profile_image = models.ImageField(upload_to='profile/', blank=True, null=True)
    
    years_experience = models.IntegerField(default=5)
    location = models.CharField(max_length=200, default="Remote")
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    
    cv_file = models.FileField(upload_to='documents/', blank=True, null=True, help_text="Upload your CV/Resume")
    
    about_intro = models.TextField(help_text="Introduction paragraph for about page")
    about_story = models.TextField(blank=True, help_text="Your story - additional details")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Profile Details"
        verbose_name_plural = "Profile Details"

    def __str__(self):
        return self.full_name


class ContactMessage(models.Model):
    """Store contact form submissions"""
    
    STATUS_CHOICES = (
        ('new', 'New'),
        ('read', 'Read'),
        ('replied', 'Replied'),
        ('spam', 'Spam'),
    )
    
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=300)
    message = models.TextField()
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    reply = models.TextField(blank=True, null=True, help_text="Your reply to the message")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    read_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"

    def __str__(self):
        return f"{self.name} - {self.subject}"


class Certificate(models.Model):
    """Store your certifications and achievements"""
    
    title = models.CharField(max_length=200)
    issuer = models.CharField(max_length=200)
    issued_date = models.DateField()
    credential_url = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='certificates/', blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-issued_date']

    def __str__(self):
        return f"{self.title} - {self.issuer}"