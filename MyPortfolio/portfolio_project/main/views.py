from django.shortcuts import render, get_object_or_404
from .models import Project, Skill, Experience, ProfileDetails, ContactMessage, Certificate

def home(request):
    try:
        featured_projects = Project.objects.filter(featured=True)[:4]
        featured_skills = Skill.objects.filter(proficiency__gte=85)[:5]
        profile = ProfileDetails.objects.first()
    except:
        featured_projects = []
        featured_skills = []
        profile = None
    
    context = {
        'featured_projects': featured_projects,
        'featured_skills': featured_skills,
        'profile': profile,
    }
    return render(request, 'main/home.html', context)


def projects(request):
    try:
        projects = Project.objects.all()
    except:
        projects = []
    
    context = {'projects': projects}
    return render(request, 'main/projects.html', context)


def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    try:
        related_projects = Project.objects.exclude(pk=pk)[:3]
    except:
        related_projects = []
    
    context = {
        'project': project,
        'related_projects': related_projects,
    }
    return render(request, 'main/project_detail.html', context)


def about(request):
    try:
        profile = ProfileDetails.objects.first()
        backend_skills = Skill.objects.filter(category='backend')
        frontend_skills = Skill.objects.filter(category='frontend')
        experiences = Experience.objects.all()
        certificates = Certificate.objects.all()[:6]
    except:
        profile = None
        backend_skills = []
        frontend_skills = []
        experiences = []
        certificates = []
    
    context = {
        'profile': profile,
        'backend_skills': backend_skills,
        'frontend_skills': frontend_skills,
        'experiences': experiences,
        'certificates': certificates,
    }
    return render(request, 'main/about.html', context)


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()
        
        errors = {}
        if not name:
            errors['name'] = 'Name is required'
        if not email:
            errors['email'] = 'Email is required'
        if not subject:
            errors['subject'] = 'Subject is required'
        if not message:
            errors['message'] = 'Message is required'
        
        try:
            profile = ProfileDetails.objects.first()
        except:
            profile = None
        
        if errors:
            return render(request, 'main/contact.html', {
                'errors': errors,
                'form_data': request.POST,
                'profile': profile,
            })
        
        try:
            ContactMessage.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message,
                status='new'
            )
            return render(request, 'main/contact.html', {
                'success': True,
                'message': 'Thank you! Your message has been sent successfully.',
                'profile': profile,
            })
        except Exception as e:
            errors['general'] = 'Error sending message. Please try again.'
            return render(request, 'main/contact.html', {
                'errors': errors,
                'profile': profile,
            })
    
    try:
        profile = ProfileDetails.objects.first()
    except:
        profile = None
    
    return render(request, 'main/contact.html', {'profile': profile})