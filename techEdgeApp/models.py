import datetime
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.conf import settings
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.utils import timezone

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='profile',  # ← C'EST IMPORTANT : 'profile' et non 'userprofile'
        verbose_name="Utilisateur"
    )
    phone = models.CharField(
        "Téléphone", 
        max_length=20, 
        blank=True,
        default=""
    )
    created_at = models.DateTimeField("Date de création", auto_now_add=True)
    updated_at = models.DateTimeField("Dernière modification", auto_now=True)
    
    class Meta:
        verbose_name = "Profil utilisateur"
        verbose_name_plural = "Profils utilisateur"
    
    def __str__(self):
        return f"Profil de {self.user.username}"

# Signals pour créer automatiquement le profil
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
        
def get_image_field():
    """Retourne le champ approprié selon la configuration"""
    use_cloudinary = getattr(settings, 'USE_CLOUDINARY', False)
    
    if use_cloudinary:
        return CloudinaryField('image', folder='services/', null=True, blank=True)
    else:
        return models.ImageField("Image", upload_to='services/', null=True, blank=True)


def get_photo_field(folder_name, verbose_name):
    """Retourne le champ approprié selon la configuration"""
    use_cloudinary = getattr(settings, 'USE_CLOUDINARY', False)
    
    if use_cloudinary:
        return CloudinaryField(verbose_name, folder=folder_name, null=True, blank=True)
    else:
        return models.ImageField(verbose_name, upload_to=folder_name, null=True, blank=True)


class Service(models.Model):
    title = models.CharField("Titre", max_length=100)
    short_description = models.CharField("Description courte", max_length=200, blank=True)
    long_description = models.TextField("Description longue", blank=True)
    icon_class = models.CharField("Classe d'icône", max_length=50, blank=True,
                                 help_text="Ex: fa fa-laptop-code")
    image = CloudinaryField('image', null=True, blank=True)   # ✅ modifié
    slug = models.SlugField(unique=True, blank=True)
    is_featured = models.BooleanField("Mettre en avant", default=False,
                                    help_text="Cocher pour afficher ce service en page d'accueil")
    display_order = models.PositiveIntegerField("Ordre d'affichage", default=0)
    
    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"
        ordering = ['-is_featured', 'display_order']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('service_detail', kwargs={'slug': self.slug})


class TeamMember(models.Model):
    POSITION_CHOICES = [
        ('management', 'Management'),
        ('technical', 'Technique'),
        ('design', 'Design'),
        ('training', 'Formation'),
    ]
    
    name = models.CharField("Nom complet", max_length=100)
    position = models.CharField("Poste", max_length=100)
    position_type = models.CharField("Type de poste", max_length=20,
                                    choices=POSITION_CHOICES, default='technical')
    bio = models.TextField("Biographie", blank=True)
    image = CloudinaryField('image', null=True, blank=True)   # ✅ modifié
    facebook = models.URLField("Facebook", blank=True)
    twitter = models.URLField("Twitter", blank=True)
    linkedin = models.URLField("LinkedIn", blank=True)
    instagram = models.URLField("Instagram", blank=True)
    email = models.EmailField("Email", blank=True)
    phone = models.CharField("Téléphone", max_length=20, blank=True)
    display_order = models.PositiveIntegerField("Ordre d'affichage", default=0)
    is_active = models.BooleanField("Actif", default=True)
    
    class Meta:
        verbose_name = "Membre d'équipe"
        verbose_name_plural = "Membres d'équipe"
        ordering = ['display_order', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.position}"


class Project(models.Model):
    PROJECT_CATEGORIES = [
        ('web', 'Développement Web'),
        ('mobile', 'Application Mobile'),
        ('system', 'Système de Gestion'),
        ('training', 'Formation'),
        ('consulting', 'Consulting'),
    ]
    title = models.CharField("Titre", max_length=100)
    short_description = models.CharField("Description courte", max_length=200)
    long_description = models.TextField("Description détaillée")
    image = CloudinaryField('image', null=True, blank=True)   # ✅ modifié
    category = models.CharField(
        "Catégorie",
        max_length=20,
        choices=PROJECT_CATEGORIES,
        blank=True,
        null=True
    )
    client_name = models.CharField("Client", max_length=100, blank=True)
    project_date = models.DateField("Date du projet", blank=True, null=True)
    project_url = models.URLField("URL du projet", blank=True)
    is_featured = models.BooleanField("En vedette", default=False)
    display_order = models.PositiveIntegerField("Ordre d'affichage", default=0)
    
    class Meta:
        verbose_name = "Projet"
        verbose_name_plural = "Projets"
        ordering = ['-is_featured', 'display_order']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('project_detail', args=[str(self.pk)])


class Testimonial(models.Model):
    client_name = models.CharField("Nom du client", max_length=100)
    company = models.CharField("Entreprise", max_length=100, blank=True)
    profession = models.CharField("Profession", max_length=100)
    content = models.TextField("Témoignage")
    image = CloudinaryField('image', null=True, blank=True)   # ✅ modifié
    rating = models.PositiveSmallIntegerField("Note (1-5)", default=5)
    is_featured = models.BooleanField("En vedette", default=False)
    display_order = models.PositiveIntegerField("Ordre d'affichage", default=0)
    created_at = models.DateTimeField("Date de création", auto_now_add=True)
    
    class Meta:
        verbose_name = "Témoignage"
        verbose_name_plural = "Témoignages"
        ordering = ['-is_featured', 'display_order']
    
    def __str__(self):
        return f"{self.client_name} - {self.profession}"


class Fact(models.Model):
    ICON_CHOICES = [
        ('certificate', 'Certificat'),
        ('users-cog', 'Utilisateurs'),
        ('users', 'Clients'),
        ('check', 'Validation'),
        ('project', 'Projet'),
    ]
    
    title = models.CharField("Titre", max_length=100)
    value = models.IntegerField("Valeur")
    icon = models.CharField("Icône", max_length=20, choices=ICON_CHOICES, default='certificate')
    suffix = models.CharField("Suffixe", max_length=5, blank=True, default='+',
                             help_text="Ex: +, %, etc.")
    display_order = models.PositiveIntegerField("Ordre d'affichage", default=0)
    
    class Meta:
        verbose_name = "Fait marquant"
        verbose_name_plural = "Faits marquants"
        ordering = ['display_order']
    
    def __str__(self):
        return self.title
    
    def get_icon_class(self):
        return f"fa fa-{self.icon}"


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    date_subscribed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class BlogCategory(models.Model):
    name = models.CharField("Nom", max_length=100)
    slug = models.SlugField("Slug", unique=True)
    description = models.TextField("Description", blank=True)
    
    class Meta:
        verbose_name = "Catégorie d'article"
        verbose_name_plural = "Catégories d'articles"
    
    def __str__(self):
        return self.name


class BlogPost(models.Model):
    title = models.CharField("Titre", max_length=200)
    slug = models.SlugField("Slug", unique=True)
    short_description = models.CharField("Description courte", max_length=300)
    content = models.TextField("Contenu")
    image = CloudinaryField('image', null=True, blank=True)   # ✅ modifié
    category = models.ForeignKey(
        BlogCategory,
        on_delete=models.SET_NULL,
        verbose_name="Catégorie",
        null=True,
        blank=True
    )
    # Ajoutez ces champs pour les likes
    likes = models.ManyToManyField(User, through='BlogLike', related_name='blog_likes', blank=True)
    likes_count = models.PositiveIntegerField(default=0)
    author = models.CharField("Auteur", max_length=100, default="TechEdge Team")
    published_date = models.DateTimeField("Date de publication", auto_now_add=True)
    updated_date = models.DateTimeField("Dernière modification", auto_now=True)
    is_published = models.BooleanField("Publié", default=False)
    views_count = models.PositiveIntegerField("Nombre de vues", default=0)
    
    class Meta:
        verbose_name = "Article de blog"
        verbose_name_plural = "Articles de blog"
        ordering = ['-published_date']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog_detail', args=[str(self.slug)])
    
    def increment_views(self):
        self.views_count += 1
        self.save()
        
    
class BlogLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'post')  # Un like par utilisateur par article

class BlogComment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    content = models.TextField("Commentaire", max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField("Actif", default=True)
    
    class Meta:
        ordering = ['created_at']
        verbose_name = "Commentaire"
        verbose_name_plural = "Commentaires"
    
    def __str__(self):
        return f"Commentaire de {self.user} sur {self.post.title}"
    
    def get_replies(self):
        return self.replies.filter(is_active=True)
    
class TrainingCategory(models.Model):
    name = models.CharField("Nom", max_length=100)
    slug = models.SlugField("Slug", unique=True)
    description = models.TextField("Description", blank=True)
    icon = models.CharField("Icône", max_length=50, default="fas fa-graduation-cap")
    
    class Meta:
        verbose_name = "Catégorie de formation"
        verbose_name_plural = "Catégories de formation"
    
    def __str__(self):
        return self.name

class Training(models.Model):
    title = models.CharField("Titre", max_length=200)
    slug = models.SlugField("Slug", unique=True)
    short_description = models.CharField("Description courte", max_length=300)
    full_description = models.TextField("Description complète")
    category = models.ForeignKey(TrainingCategory, on_delete=models.CASCADE, verbose_name="Catégorie")
    duration = models.CharField("Durée", max_length=50, help_text="Ex: 3 mois, 40 heures")
    price = models.DecimalField("Prix", max_digits=10, decimal_places=2, default=0)
    image = CloudinaryField('image')
    is_active = models.BooleanField("Active", default=True)
    start_date = models.DateField("Date de début", null=True, blank=True)
    end_date = models.DateField("Date de fin", null=True, blank=True)
    max_participants = models.PositiveIntegerField("Nombre maximum de participants", default=20)
    current_participants = models.PositiveIntegerField("Participants actuels", default=0)
    created_at = models.DateTimeField("Date de création", auto_now_add=True)
    
    class Meta:
        verbose_name = "Formation"
        verbose_name_plural = "Formations"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('training_detail', args=[str(self.slug)])
    
    def is_available(self):
        return self.is_active and self.current_participants < self.max_participants
    
    def available_seats(self):
        return self.max_participants - self.current_participants

class TrainingRegistration(models.Model):
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('confirmed', 'Confirmé'),
        ('cancelled', 'Annulé'),
        ('completed', 'Terminé'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Utilisateur")
    training = models.ForeignKey(Training, on_delete=models.CASCADE, verbose_name="Formation")
    
    # Informations supplémentaires (en cas de modification du profil)
    user_first_name = models.CharField("Prénom", max_length=100, blank=True)
    user_last_name = models.CharField("Nom", max_length=100, blank=True)
    user_email = models.EmailField("Email", blank=True)
    user_phone = models.CharField("Téléphone", max_length=20, blank=True)
    
    registration_date = models.DateTimeField("Date d'inscription", auto_now_add=True)
    status = models.CharField("Statut", max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField("Notes", blank=True)
    
    class Meta:
        verbose_name = "Inscription à une formation"
        verbose_name_plural = "Inscriptions aux formations"
        unique_together = ['user', 'training']
    
    def __str__(self):
        return f"{self.user.username} - {self.training.title}"
    
    def save(self, *args, **kwargs):
    # Sauvegarder les informations utilisateur actuelles
        if self.user:
            self.user_first_name = self.user.first_name or ""
            self.user_last_name = self.user.last_name or ""
            self.user_email = self.user.email or ""
            
            # Récupérer le téléphone du profil
            try:
                if hasattr(self.user, 'profile') and self.user.profile.phone:
                    self.user_phone = self.user.profile.phone
                else:
                    self.user_phone = "Non renseigné"
            except Exception:
                self.user_phone = "Non renseigné"
        
        super().save(*args, **kwargs)

# class TrainingRegistration(models.Model):
#     STATUS_CHOICES = [
#         ('pending', 'En attente'),
#         ('confirmed', 'Confirmé'),
#         ('cancelled', 'Annulé'),
#         ('completed', 'Terminé'),
#     ]
    
#     user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Utilisateur")
#     training = models.ForeignKey(Training, on_delete=models.CASCADE, verbose_name="Formation")
#     registration_date = models.DateTimeField("Date d'inscription", auto_now_add=True)
#     status = models.CharField("Statut", max_length=20, choices=STATUS_CHOICES, default='pending')
#     notes = models.TextField("Notes", blank=True)
    
#     class Meta:
#         verbose_name = "Inscription à une formation"
#         verbose_name_plural = "Inscriptions aux formations"
#         unique_together = ['user', 'training']  # Un utilisateur ne peut s'inscrire qu'une fois
    
#     def __str__(self):
#         return f"{self.user.username} - {self.training.title}"

# from django.db import models
# from django.utils.text import slugify
# from django.utils import timezone
# class Training(models.Model):
#     title = models.CharField(max_length=200)
#     slug = models.SlugField(unique=True, blank=True)
#     short_description = models.CharField(max_length=255)
#     full_description = models.TextField()
#     image = models.ImageField(upload_to='trainings/')
#     duration = models.CharField(max_length=100)
#     start_date = models.DateField("Date de début", null=True, blank=True)
#     end_date = models.DateField("Date de fin", null=True, blank=True)
#     # end_date = models.DateField(default=datetime.date(2025, 12, 31))
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     available_seats = models.PositiveIntegerField(default=0)
#     is_active = models.BooleanField(default=True)
#     created_at = models.DateTimeField(default=timezone.now)
#     updated_at = models.DateTimeField(auto_now=True)
#     def save(self, *args, **kwargs):
#         if not self.slug:
#             self.slug = slugify(self.title)
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return self.title

#     def get_absolute_url(self):
#         from django.urls import reverse
#         return reverse('training_detail', kwargs={'slug': self.slug})

# class Training(models.Model):
#     title = models.CharField("Titre", max_length=200)
#     slug = models.SlugField("Slug", unique=True)
#     short_description = models.CharField("Description courte", max_length=300)
#     full_description = models.TextField("Description complète")
#     category = models.ForeignKey(TrainingCategory, on_delete=models.CASCADE, verbose_name="Catégorie")
#     duration = models.CharField("Durée", max_length=50, help_text="Ex: 3 mois, 40 heures")
#     price = models.DecimalField("Prix", max_digits=10, decimal_places=2, default=0)
#     image = CloudinaryField('image')
#     is_active = models.BooleanField("Active", default=True)
#     start_date = models.DateField("Date de début", null=True, blank=True)
#     end_date = models.DateField("Date de fin", null=True, blank=True)
#     max_participants = models.PositiveIntegerField("Nombre maximum de participants", default=20)
#     current_participants = models.PositiveIntegerField("Participants actuels", default=0)
#     created_at = models.DateTimeField("Date de création", auto_now_add=True)
    
#     class Meta:
#         verbose_name = "Formation"
#         verbose_name_plural = "Formations"
#         ordering = ['-created_at']
    
#     def __str__(self):
#         return self.title
    
#     def get_absolute_url(self):
#         return reverse('training_detail', args=[str(self.slug)])
    
#     def is_available(self):
#         return self.is_active and self.current_participants < self.max_participants
    
#     def available_seats(self):
#         return self.max_participants - self.current_participants

# class TrainingRegistration(models.Model):
#     STATUS_CHOICES = [
#         ('pending', 'En attente'),
#         ('confirmed', 'Confirmé'),
#         ('cancelled', 'Annulé'),
#         ('completed', 'Terminé'),
#     ]
    
#     user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Utilisateur")
#     training = models.ForeignKey(Training, on_delete=models.CASCADE, verbose_name="Formation")
#     registration_date = models.DateTimeField("Date d'inscription", auto_now_add=True)
#     status = models.CharField("Statut", max_length=20, choices=STATUS_CHOICES, default='pending')
#     notes = models.TextField("Notes", blank=True)
    
#     class Meta:
#         verbose_name = "Inscription à une formation"
#         verbose_name_plural = "Inscriptions aux formations"
#         unique_together = ['user', 'training']  # Un utilisateur ne peut s'inscrire qu'une fois
    
#     def __str__(self):
#         return f"{self.user.username} - {self.training.title}"

        
    # from django.db import models
# from django.utils.text import slugify
# from django.urls import reverse
# from cloudinary.models import CloudinaryField

# # class ProjectCategory(models.Model):
# #     name = models.CharField("Nom de la catégorie", max_length=100)
# #     slug = models.SlugField("Slug", unique=True)
# #     description = models.TextField("Description", blank=True)
# #     icon = models.CharField("Icône FontAwesome", max_length=50, default="fas fa-folder")
# #     display_order = models.PositiveIntegerField("Ordre d'affichage", default=0)
# #     is_active = models.BooleanField("Active", default=True)

# #     class Meta:
# #         verbose_name = "Catégorie de projet"
# #         verbose_name_plural = "Catégories de projet"
# #         ordering = ['display_order', 'name']

# #     def __str__(self):
# #         return self.name

# #     def save(self, *args, **kwargs):
# #         if not self.slug:
# #             self.slug = slugify(self.name)
# #         super().save(*args, **kwargs)

# class Service(models.Model):
#     title = models.CharField("Titre", max_length=100)
#     short_description = models.CharField("Description courte", max_length=200, blank=True)
#     long_description = models.TextField("Description longue", blank=True)
#     icon_class = models.CharField("Classe d'icône", max_length=50, blank=True, 
#                                  help_text="Ex: fa fa-laptop-code")
#     image = CloudinaryField('Image', folder='services/', null=True, blank=True)
#     #image = models.ImageField("Image", upload_to='services/')
#     slug = models.SlugField(unique=True, blank=True)
#     is_featured = models.BooleanField("Mettre en avant", default=False,
#                                     help_text="Cocher pour afficher ce service en page d'accueil")
#     display_order = models.PositiveIntegerField("Ordre d'affichage", default=0)
    
#     class Meta:
#         verbose_name = "Service"
#         verbose_name_plural = "Services"
#         ordering = ['display_order', 'title']
#         ordering = ['-is_featured', 'display_order']
    
#     def save(self, *args, **kwargs):
#         if not self.slug:
#             self.slug = slugify(self.title)
#         super().save(*args, **kwargs)
    
#     def __str__(self):
#         return self.title
    
#     def get_absolute_url(self):
#         return reverse('service_detail', kwargs={'slug': self.slug})

# class TeamMember(models.Model):
#     POSITION_CHOICES = [
#         ('management', 'Management'),
#         ('technical', 'Technique'),
#         ('design', 'Design'),
#         ('training', 'Formation'),
#     ]
    
#     name = models.CharField("Nom complet", max_length=100)
#     position = models.CharField("Poste", max_length=100)
#     position_type = models.CharField("Type de poste", max_length=20, 
#                                     choices=POSITION_CHOICES, default='technical')
#     bio = models.TextField("Biographie", blank=True)
#     # image = models.ImageField("Photo", upload_to='team/')

#     image = CloudinaryField('Photo', folder='team/', null=True, blank=True)
#     facebook = models.URLField("Facebook", blank=True)
#     twitter = models.URLField("Twitter", blank=True)
#     linkedin = models.URLField("LinkedIn", blank=True)
#     instagram = models.URLField("Instagram", blank=True)
#     email = models.EmailField("Email", blank=True)
#     phone = models.CharField("Téléphone", max_length=20, blank=True)
#     display_order = models.PositiveIntegerField("Ordre d'affichage", default=0)
#     is_active = models.BooleanField("Actif", default=True)
    
#     class Meta:
#         verbose_name = "Membre d'équipe"
#         verbose_name_plural = "Membres d'équipe"
#         ordering = ['display_order', 'name']
    
#     def __str__(self):
#         return f"{self.name} - {self.position}"

# class Project(models.Model):
#     PROJECT_CATEGORIES = [
#         ('web', 'Développement Web'),
#         ('mobile', 'Application Mobile'),
#         ('system', 'Système de Gestion'),
#         ('training', 'Formation'),
#         ('consulting', 'Consulting'),
#     ]
#     title = models.CharField("Titre", max_length=100)
#     short_description = models.CharField("Description courte", max_length=200)
#     long_description = models.TextField("Description détaillée")
#     # image = models.ImageField("Image principale", upload_to='projects/')
#     image = CloudinaryField('Image principale', folder='projects/',null=True, blank=True)
#     category = models.CharField(
#     "Catégorie", 
#     max_length=20, 
#     choices=PROJECT_CATEGORIES, 
#     blank=True, 
#     null=True
# )
#     client_name = models.CharField("Client", max_length=100, blank=True)
#     project_date = models.DateField("Date du projet", blank=True, null=True)
#     project_url = models.URLField("URL du projet", blank=True)
#     is_featured = models.BooleanField("En vedette", default=False)
#     display_order = models.PositiveIntegerField("Ordre d'affichage", default=0)
    
#     class Meta:
#         verbose_name = "Projet"
#         verbose_name_plural = "Projets"
#         ordering = ['-is_featured', 'display_order']
    
#     def __str__(self):
#         return self.title
#     def get_absolute_url(self):
#         return reverse('project_detail', args=[str(self.pk)])

# class Testimonial(models.Model):
#     client_name = models.CharField("Nom du client", max_length=100)
#     company = models.CharField("Entreprise", max_length=100, blank=True)
#     profession = models.CharField("Profession", max_length=100)
#     content = models.TextField("Témoignage")
#     # image = models.ImageField("Photo", upload_to='testimonials/', blank=True)
#     image = CloudinaryField('Photo', folder='testimonials/',null=True, blank=True)
#     rating = models.PositiveSmallIntegerField("Note (1-5)", default=5)
#     is_featured = models.BooleanField("En vedette", default=False)
#     display_order = models.PositiveIntegerField("Ordre d'affichage", default=0)
#     created_at = models.DateTimeField("Date de création", auto_now_add=True)
    
#     class Meta:
#         verbose_name = "Témoignage"
#         verbose_name_plural = "Témoignages"
#         ordering = ['-is_featured', 'display_order']
    
#     def __str__(self):
#         return f"{self.client_name} - {self.profession}"

# class Fact(models.Model):
#     ICON_CHOICES = [
#         ('certificate', 'Certificat'),
#         ('users-cog', 'Utilisateurs'),
#         ('users', 'Clients'),
#         ('check', 'Validation'),
#         ('project', 'Projet'),
#     ]
    
#     title = models.CharField("Titre", max_length=100)
#     value = models.IntegerField("Valeur")
#     icon = models.CharField("Icône", max_length=20, choices=ICON_CHOICES, default='certificate')
#     suffix = models.CharField("Suffixe", max_length=5, blank=True, default='+',
#                              help_text="Ex: +, %, etc.")
#     display_order = models.PositiveIntegerField("Ordre d'affichage", default=0)
    
#     class Meta:
#         verbose_name = "Fait marquant"
#         verbose_name_plural = "Faits marquants"
#         ordering = ['display_order']
    
#     def __str__(self):
#         return self.title
    
#     def get_icon_class(self):
#         return f"fa fa-{self.icon}"
    
# class Subscriber(models.Model):
#     email = models.EmailField(unique=True)
#     date_subscribed = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.email