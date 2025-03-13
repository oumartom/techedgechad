from django.shortcuts import render


from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .form import ContactForm


# Create your views here.
def index(request):
    return render(request, 'index.html',{})

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