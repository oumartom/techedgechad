from django.shortcuts import render, get_object_or_404
from .models import Service, TeamMember, Project, Testimonial, Fact

from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .form import ContactForm,SubscriberForm
from .models import Service, Project
from techEdgeApp import models
from .models import Service
# views.py


# import openai
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import json
# from django.conf import settings
# # Create your views here.

# @csrf_exempt
# def chatbot(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         user_message = data.get('message')
#         print("Message reçu:", user_message)  # ⬅️ debug

#         if not user_message:
#             return JsonResponse({'error': 'Message vide'}, status=400)

#         try:
#             openai.api_key = settings.OPENAI_API_KEY
            
#             response = openai.ChatCompletion.create(
#                 model="gpt-3.5-turbo",
#                 messages=[
#                     {"role": "system", "content": "Tu es TechEdge Assistant, un expert en solutions informatiques."},
#                     {"role": "user", "content": user_message},
#                 ]
#             )
#             assistant_reply = response['choices'][0]['message']['content']
#             print("Réponse:", assistant_reply)  # ⬅️ debug
#             return JsonResponse({'reply': assistant_reply})
#         except Exception as e:
#             print("Erreur OpenAI:", str(e))  # ⬅️ debug
#             return JsonResponse({'error': str(e)}, status=500)
#     else:
#         return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

def index(request):
    if not all([settings.CLOUDINARY_CLOUD_NAME, settings.CLOUDINARY_API_KEY, settings.CLOUDINARY_API_SECRET]):
        print("ATTENTION: Configuration Cloudinary incomplète")
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
    team_members = TeamMember.objects.all()  # récupère les membres
    return render(request, 'about.html', {'team_members': team_members})
def subscribe_newsletter(request):
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')  # ou afficher un message de succès
    return redirect('index')

def service(request):
    services_list = Service.objects.all().order_by('display_order')
    context = {
        'services': services_list  # Ceci est la variable qui sera utilisée dans le template
    }
    return render(request, 'service.html', context)

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
    related_projects = Project.objects.exclude(pk=pk)[:3]  # Exemple
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
    
    testimonials = Testimonial.objects.filter(is_featured=True).order_by('display_order')
    return render(request, 'testimonial.html', {'testimonials': testimonials})
# Vue pour la page "Contact"
# Vue pour la page "Contact"
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

            # CORRECTION : Utiliser EmailMessage au lieu de send_mail
            from django.core.mail import EmailMessage
            
            email_message = EmailMessage(
                subject=f"{subject} - Message de {name}",  # Sujet
                body=f"Nom: {name}\nEmail: {email}\n\nMessage:\n{message}",  # Corps du message
                from_email=settings.EMAIL_HOST_USER,  # Expéditeur = ton email LWS ✅
                to=[settings.EMAIL_HOST_USER],  # Destinataire = ton email LWS ✅
                reply_to=[f"{name} <{email}>"]  # Pour répondre à l'utilisateur ✅
            )
            
            email_message.send(fail_silently=False)

            # Rediriger vers une page de confirmation
            return render(request, 'contact.html', {'message_name': name})
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})
# def contact(request):
#     if request.method == 'POST':
#         form = ContactForm(request.POST)
#         if form.is_valid():
#             # Récupérer les données du formulaire
#             name = form.cleaned_data['name']
#             email = form.cleaned_data['email']
#             subject = form.cleaned_data['subject']
#             message = form.cleaned_data['message']

#             # Envoyer un email (exemple)
#             send_mail(
#                 f"{subject} - Message de {name}",
#                 f"De : {name} <{email}>\n\n{message}",
#                 email,  # Expéditeur
#                 [settings.EMAIL_HOST_USER],  # Destinataire
#                 fail_silently=False,
#             )

#             # Rediriger vers une page de confirmation
#             return render(request, 'contact.html', {'message_name': name})
#     else:
#         form = ContactForm()

#     return render(request, 'contact.html',{'form': form})

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
            ['techedgecenter@gmail.com'],
            
        )
        return render(request, 'contact.html',{'name': message_name})
    else:
        return render(request, 'contact.html')

