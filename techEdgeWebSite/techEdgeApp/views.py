from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Vue pour la page d'accueil
def index(request):
    return render(request, 'index.html')

# Vue pour la page "À propos"
def about(request):
    return render(request, 'about.html')

# Vue pour la page "Services"
def service(request):
    return render(request, 'service.html')

# Vue pour la page "Projets"
def project(request):
    return render(request, 'project.html')

# Vue pour la page "Fonctionnalités"
def feature(request):
    return render(request, 'feature.html')

# Vue pour la page "Équipe"
def team(request):
    return render(request, 'team.html')

# Vue pour la page "Témoignages"
def testimonial(request):
    return render(request, 'testimonial.html')

# Vue pour la page "Contact"
def contact(request):
    return render(request, 'contact.html')

# Vue pour la page d'erreur 404
def error_404(request, exception=None):
    return render(request, '404.html', status=404)