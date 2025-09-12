from django.shortcuts import render, get_object_or_404
from .models import Service, TeamMember, Project, Testimonial, Fact

from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .form import ContactForm,SubscriberForm,CommentForm,CustomUserCreationForm,TrainingRegistrationForm
from .models import Service, Project
from techEdgeApp import models
from .models import Service
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import BlogPost, BlogCategory
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from .models import BlogPost, BlogLike, BlogComment

from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.contrib.auth import logout

from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib import messages

from .models import Training, TrainingCategory, TrainingRegistration

from .models import Training, TrainingCategory, TrainingRegistration


def training_list(request):
    categories = TrainingCategory.objects.all()
    trainings = Training.objects.filter(is_active=True).order_by('-created_at')
    
    # Filtrer par catégorie si spécifié
    category_slug = request.GET.get('category')
    if category_slug:
        trainings = trainings.filter(category__slug=category_slug)
    
    context = {
        'trainings': trainings,
        'categories': categories,
        'selected_category': category_slug,
    }
    return render(request, 'training/training_list.html', context)

def training_detail(request, slug):
    training = get_object_or_404(Training, slug=slug, is_active=True)
    user_has_registered = False
    registration_form = TrainingRegistrationForm()
    
    if request.user.is_authenticated:
        user_has_registered = TrainingRegistration.objects.filter(
            user=request.user, training=training
        ).exists()
    
    # Formations similaires
    similar_trainings = Training.objects.filter(
        category=training.category, 
        is_active=True
    ).exclude(id=training.id)[:4]
    
    context = {
        'training': training,
        'user_has_registered': user_has_registered,
        'registration_form': registration_form,
        'similar_trainings': similar_trainings,
    }
    return render(request, 'training/training_detail.html', context)

@login_required
def register_for_training(request, slug):
    training = get_object_or_404(Training, slug=slug, is_active=True)
    
    # Vérifier si l'utilisateur est déjà inscrit
    if TrainingRegistration.objects.filter(user=request.user, training=training).exists():
        messages.warning(request, 'Vous êtes déjà inscrit à cette formation.')
        return redirect('training_detail', slug=training.slug)
    
    # Vérifier si la formation est complète
    if not training.is_available():
        messages.error(request, 'Désolé, cette formation est complète.')
        return redirect('training_detail', slug=training.slug)
    
    if request.method == 'POST':
        form = TrainingRegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.user = request.user
            registration.training = training
            registration.save()
            
            # Mettre à jour le compteur de participants
            training.current_participants += 1
            training.save()
            
            messages.success(request, 'Votre inscription a été enregistrée avec succès !')
            return redirect('training_detail', slug=training.slug)
    else:
        form = TrainingRegistrationForm()
    
    context = {
        'training': training,
        'form': form,
    }
    return render(request, 'training/register_training.html', context)

@login_required
def my_trainings(request):
    registrations = TrainingRegistration.objects.filter(user=request.user).order_by('-registration_date')
    context = {
        'registrations': registrations,
    }
    return render(request, 'training/my_trainings.html', context)
# def training_list(request):
#     trainings = Training.objects.all()
#     categories = TrainingCategory.objects.all()
#     selected_category = request.GET.get('category')
#     if selected_category:
#         trainings = trainings.filter(category__slug=selected_category)
#     return render(request, 'training/training_detail.html', {
#         'trainings': trainings,
#         'categories': categories,
#         'selected_category': selected_category,
#     })
# def training_list(request):
#     # Filtrer par catégorie si un slug est passé en GET
#     selected_category = request.GET.get('category')
#     categories = TrainingCategory.objects.all()  # Pour les boutons de filtre

#     trainings = Training.objects.filter(is_active=True)  # seulement les formations actives
#     if selected_category:
#         trainings = trainings.filter(category__slug=selected_category)

#     context = {
#         'trainings': trainings,
#         'categories': categories,
#         'selected_category': selected_category
#     }
#     return render(request, 'training/training_detail.html', context)

# def training_detail(request, slug):
#     training = get_object_or_404(Training, slug=slug, is_active=True)
#     user_has_registered = False
#     registration_form = TrainingRegistrationForm()
    
#     if request.user.is_authenticated:
#         user_has_registered = TrainingRegistration.objects.filter(
#             user=request.user, training=training
#         ).exists()
    
#     # Formations similaires
#     similar_trainings = Training.objects.filter(
#         category=training.category, 
#         is_active=True
#     ).exclude(id=training.id)[:4]
    
#     context = {
#         'training': training,
#         'user_has_registered': user_has_registered,
#         'registration_form': registration_form,
#         'similar_trainings': similar_trainings,
#     }
#     return render(request, 'training/training_detail.html', context)
from django.shortcuts import render, get_object_or_404, redirect
from .models import Training, TrainingRegistration

# from django.contrib.auth.decorators import login_required

# @login_required
# def training_detail(request, slug):
#     training = get_object_or_404(Training, slug=slug)
#     user_has_registered = request.user.is_authenticated and TrainingRegistration.objects.filter(
#         training=training, user=request.user).exists()
#     registration_form = TrainingRegistrationForm()  # form vide
#     similar_trainings = Training.objects.exclude(id=training.id)[:4]

#     context = {
#         'training': training,
#         'user_has_registered': user_has_registered,
#         'registration_form': registration_form,
#         'similar_trainings': similar_trainings,
#     }
#     return render(request, 'training_detail.html', context)

# def training_detail(request, slug):
#     training = get_object_or_404(Training, slug=slug)
#     user_has_registered = TrainingRegistration.objects.filter(user=request.user, training=training).exists()
#     registration_form = TrainingRegistrationForm()

#     if request.method == "POST" and not user_has_registered:
#         registration_form = TrainingRegistrationForm(request.POST)
#         if registration_form.is_valid():
#             registration = registration_form.save(commit=False)
#             registration.user = request.user
#             registration.training = training
#             registration.save()
#             return redirect('training_detail', slug=training.slug)

#     # Récupérer formations similaires
#     similar_trainings = Training.objects.filter(category=training.category).exclude(id=training.id)[:4]

#     context = {
#         'training': training,
#         'registration_form': registration_form,
#         'user_has_registered': user_has_registered,
#         'similar_trainings': similar_trainings,
#     }
#     return render(request, 'training_detail.html', context)

# @login_required
# def register_for_training(request, slug):
#     training = get_object_or_404(Training, slug=slug, is_active=True)
    
#     # Vérifier si l'utilisateur est déjà inscrit
#     if TrainingRegistration.objects.filter(user=request.user, training=training).exists():
#         messages.warning(request, 'Vous êtes déjà inscrit à cette formation.')
#         return redirect('training_detail', slug=training.slug)
    
#     # Vérifier si la formation est complète
#     if not training.is_available():
#         messages.error(request, 'Désolé, cette formation est complète.')
#         return redirect('training_detail', slug=training.slug)
    
#     if request.method == 'POST':
#         form = TrainingRegistrationForm(request.POST)
#         if form.is_valid():
#             registration = form.save(commit=False)
#             registration.user = request.user
#             registration.training = training
#             registration.save()
            
#             # Mettre à jour le compteur de participants
#             training.current_participants += 1
#             training.save()
            
#             messages.success(request, 'Votre inscription a été enregistrée avec succès !')
#             return redirect('training_detail', slug=training.slug)
#     else:
#         form = TrainingRegistrationForm()
    
#     context = {
#         'training': training,
#         'form': form,
#     }
#     return render(request, 'training/register_training.html', context)

# @login_required
# def my_trainings(request):
#     registrations = TrainingRegistration.objects.filter(user=request.user).order_by('-registration_date')
#     context = {
#         'registrations': registrations,
#     }
#     return render(request, 'training/my_trainings.html', context)
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('index')
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # ou une autre page
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# def register(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             messages.success(request, 'Compte créé avec succès ! Bienvenue !')
            
#             # Redirection vers la page précédente ou l'accueil
#             next_url = request.POST.get('next', 'index')
#             return redirect(next_url)
#     else:
#         form = CustomUserCreationForm()
    
#     context = {
#         'form': form,
#         'next': request.GET.get('next', 'index')
#     }
#     return render(request, 'registration/register.html', context)
def custom_logout(request):
    logout(request)
    messages.success(request, 'Vous avez été déconnecté avec succès.')
    return redirect('index')

def blog(request):
    posts_list = BlogPost.objects.filter(is_published=True).order_by('-published_date')
    categories = BlogCategory.objects.all()
    
    # Pagination
    paginator = Paginator(posts_list, 6)  # 6 articles par page
    page = request.GET.get('page')
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    # Articles récents (sidebar)
    recent_posts = BlogPost.objects.filter(is_published=True).order_by('-published_date')[:5]
    
    return render(request, 'blog.html', {
        'posts': posts,
        'categories': categories,
        'recent_posts': recent_posts
    })

def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    
    # Incrémenter les vues
    post.increment_views()
    
    # Comments
    comments = post.comments.filter(is_active=True, parent__isnull=True)
    comment_form = CommentForm()
    
    # Check if user liked the post
    user_liked = False
    if request.user.is_authenticated:
        user_liked = BlogLike.objects.filter(user=request.user, post=post).exists()
    
    # Articles similaires
    similar_posts = BlogPost.objects.filter(
        category=post.category, 
        is_published=True
    ).exclude(id=post.id)[:3]
    
    # Articles récents
    recent_posts = BlogPost.objects.filter(is_published=True).exclude(id=post.id).order_by('-published_date')[:5]
    
    context = {
        'post': post,
        'similar_posts': similar_posts,
        'recent_posts': recent_posts,
        'comments': comments,
        'comment_form': comment_form,
        'user_liked': user_liked,
        'likes_count': post.likes_count,
    }
    return render(request, 'blog_detail.html', context)
@login_required
@require_POST
def like_blog_post(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    user = request.user
    
    # Vérifier si l'utilisateur a déjà liké
    like, created = BlogLike.objects.get_or_create(user=user, post=post)
    
    if not created:
        # unlike
        like.delete()
        post.likes_count = max(0, post.likes_count - 1)
        liked = False
    else:
        # like
        post.likes_count += 1
        liked = True
    
    post.save()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'liked': liked,
            'likes_count': post.likes_count
        })
    
    return redirect('blog_detail', slug=post.slug)

@login_required
def add_comment(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            
            # Gestion des réponses (commentaires imbriqués)
            parent_id = request.POST.get('parent_id')
            if parent_id:
                try:
                    parent_comment = BlogComment.objects.get(id=parent_id)
                    comment.parent = parent_comment
                except BlogComment.DoesNotExist:
                    pass
            
            comment.save()
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'comment_id': comment.id,
                    'user_name': comment.user.username,
                    'content': comment.content,
                    'created_at': comment.created_at.strftime('%d %b %Y à %H:%M'),
                    'parent_id': comment.parent.id if comment.parent else None
                })
            
            messages.success(request, 'Votre commentaire a été ajouté !')
            return redirect('blog_detail', slug=post.slug)
    
    return redirect('blog_detail', slug=post.slug)
def blog_category(request, category_slug):
    category = get_object_or_404(BlogCategory, slug=category_slug)
    posts_list = BlogPost.objects.filter(category=category, is_published=True).order_by('-published_date')
    
    # Pagination
    paginator = Paginator(posts_list, 6)
    page = request.GET.get('page')
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    # Articles récents (sidebar)
    recent_posts = BlogPost.objects.filter(is_published=True).order_by('-published_date')[:5]
    
    # Catégories
    categories = BlogCategory.objects.all()
    
    return render(request, 'blog_category.html', {
        'category': category,
        'posts': posts,
        'categories': categories,
        'recent_posts': recent_posts
    })


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

from django.conf import settings

from .models import Service, TeamMember, Project, Testimonial, Fact, BlogPost

def index(request):
    # Vérification Cloudinary sécurisée
    use_cloudinary = getattr(settings, 'USE_CLOUDINARY', False)
    
    if not use_cloudinary:
        print("ℹ️  Mode développement: Stockage local activé")
    else:
        print("✅ Cloudinary configuré pour la production")
    
    services = Service.objects.filter(is_featured=True)[:6]
    team_members = TeamMember.objects.filter(is_active=True).order_by('display_order')[:4]
    featured_projects = Project.objects.filter(is_featured=True)[:6]
    testimonials = Testimonial.objects.filter(is_featured=True).order_by('display_order')
    facts = Fact.objects.all().order_by('display_order')
    
    # Services featured avec fallback
    if Service.objects.filter(is_featured=True).exists():
        featured_services = Service.objects.filter(is_featured=True)[:6]
    else:
        featured_services = Service.objects.all()[:6]
    
    # Articles de blog
    latest_blog_posts = BlogPost.objects.filter(is_published=True).order_by('-published_date')[:3]
    
    context = {
        'services': services,
        'team_members': team_members,
        'featured_projects': featured_projects,
        'testimonials': testimonials,
        'facts': facts,
        'featured_services': featured_services,
        'latest_blog_posts': latest_blog_posts,
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
    all_projects = Project.objects.all().order_by('-is_featured', 'display_order', '-project_date')
    
    # Récupérer les catégories depuis le modèle
    project_categories = Project.PROJECT_CATEGORIES
    
    return render(request, 'project.html', {
        'projects': all_projects,
        'project_categories': project_categories
    })

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

