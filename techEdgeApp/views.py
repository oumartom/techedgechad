from django.shortcuts import render, get_object_or_404
from .models import Service, TeamMember, Project, Testimonial, Fact


from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .form import ContactForm
from .models import Service, Project
from techEdgeApp import models
from .models import Service
# Create your views here.
def index(request):
    services = Service.objects.filter(is_featured=True)[:6]
    team_members = TeamMember.objects.filter(is_active=True).order_by('display_order')[:4]
    featured_projects = Project.objects.filter(is_featured=True)[:6]
    testimonials = Testimonial.objects.filter(is_featured=True).order_by('display_order')
    facts = Fact.objects.all().order_by('display_order')
    featured_services = Service.objects.filter(is_featured=True)[:6] if Service.objects.filter(is_featured=True).exists() else Service.objects.all()[:6]
    context = {
        'services': services,
        'team_members': team_members,
        'featured_projects': featured_projects,
        'testimonials': testimonials,
        'facts': facts,
        'featured_services': featured_services,
    }
    return render(request, 'index.html', context)

# Vue pour la page "À propos"
def about(request):
    return render(request, 'about.html')

# Vue pour la page "Services"
# def service(request):
#     all_services = Service.objects.all().order_by('display_order')
#     return render(request, 'service.html', {'service': all_services})

def service(request):
    services_list = Service.objects.all().order_by('display_order')
    context = {
        'services': services_list  # Ceci est la variable qui sera utilisée dans le template
    }
    return render(request, 'service.html', context)
# Vue pour la page "Projets"
# def project(request):
#     project = Project.objects.all().order_by('-project_date', 'display_order')
#     return render(request, 'project.html', {'project': project})
def project(request):
    #projects_list = Project.objects.all().order_by('-is_featured', 'display_order')
    all_projects = Project.objects.all().order_by('-is_featured', 'display_order', '-project_date')
    return render(request, 'project.html', {'projects': all_projects})
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    related_projects = Project.objects.exclude(pk=project.pk).filter(category=project.category)[:3]
    return render(request, 'project_detail.html', {
        'project': project,
        'related_projects': related_projects
    })
    
def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug)
    related_services = Service.objects.exclude(id=service.id).order_by('?')[:3]  # 3 services aléatoires
    return render(request, 'service_detail.html', {
        'service': service,
        'related_services': related_services
    })

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    related_projects = Project.objects.exclude(id=project.id).filter(category=project.category).order_by('?')[:3]
    return render(request, 'project_detail.html', {
        'project': project,
        'related_projects': related_projects
    })
# Vue pour la page "Fonctionnalités"
def feature(request):
    return render(request, 'feature.html')

# Vue pour la page "Équipe"
def team(request):
    team_members = TeamMember.objects.filter(is_active=True).order_by('display_order')
    return render(request, 'team.html', {'team_members': team_members})

# Vue pour la page "Témoignages"
def testimonial(request):
    return render(request, 'testimonial.html')

# Vue pour la page "Contact"
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Récupérer les données du formulaire
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            # Envoyer un email (exemple)
            send_mail(
                f"{subject} - Message de {name}",
                f"De : {name} <{email}>\n\n{message}",
                email,  # Expéditeur
                [settings.EMAIL_HOST_USER],  # Destinataire
                fail_silently=False,
            )

            # Rediriger vers une page de confirmation
            return render(request, 'contact.html', {'message_name': name})
    else:
        form = ContactForm()

    return render(request, 'contact.html',{'form': form})

# def contact(request):
    if request.method == "POST":
        message_name = request.POST['name']
        message_email = request.POST['email']
        objet = request.POST['subject']
        message = request.POST['message'] 
        
        send_mail(
            message_name,
            message,
            message_email,
            ['oumartom45@gmail.com'],
            
        )
        return render(request, 'contact.html',{'name': message_name})
    else:
        return render(request, 'contact.html')

# Vue pour la page d'erreur 404
def error_404(request, exception=None):
    return render(request, '404.html', status=404)