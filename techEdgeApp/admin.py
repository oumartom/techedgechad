from django.contrib import admin
from django.shortcuts import get_object_or_404, render
from django.utils.html import format_html
from .models import Service, TeamMember, Project, Testimonial, Fact, Training, TrainingCategory, TrainingRegistration, UserProfile
from .models import Subscriber
from .models import Subscriber
admin.site.register(Subscriber)


from .models import BlogCategory, BlogPost

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'published_date', 'is_published', 'views_count')
    list_filter = ('category', 'is_published', 'published_date')
    list_editable = ('is_published',)
    search_fields = ('title', 'short_description', 'content')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('views_count', 'published_date', 'updated_date')
    
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'short_description', 'content', 'image', 'category')
        }),
        ('Informations de publication', {
            'fields': ('author', 'is_published', 'published_date', 'updated_date', 'views_count')
        }),
    )
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_featured', 'display_order', 'image_preview')
    list_editable = ('is_featured', 'display_order')
    list_filter = ('is_featured',)
    search_fields = ('title', 'short_description')
    prepopulated_fields = {'slug': ('title',)}
    
    def image_preview(self, obj):
        from django.utils.html import format_html
        return format_html('<img src="{}" width="50" />', obj.image.url) if obj.image else "-"
    image_preview.short_description = 'Aperçu'

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'position_type', 'is_active', 'preview_image')
    list_editable = ('is_active',)
    list_filter = ('position_type', 'is_active')
    search_fields = ('name', 'position')
    
    def preview_image(self, obj):
        return format_html('<img src="{}" width="50" style="border-radius:50%;" />', obj.image.url) if obj.image else '-'
    preview_image.short_description = 'Photo'

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'client_name', 'is_featured', 'preview_image')
    list_editable = ('is_featured',)
    list_filter = ('category', 'is_featured')
    search_fields = ('title', 'client_name', 'short_description')
    
    def preview_image(self, obj):
        return format_html('<img src="{}" width="50" />', obj.image.url) if obj.image else '-'
    preview_image.short_description = 'Image'

# admin.py
@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'profession', 'company', 'rating_stars', 'is_featured', 'preview_image')
    list_editable = ('is_featured',)
    list_filter = ('rating', 'is_featured', 'created_at')
    search_fields = ('client_name', 'company', 'profession', 'content')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Informations client', {
            'fields': ('client_name', 'profession', 'company', 'image')
        }),
        ('Témoignage', {
            'fields': ('content', 'rating', 'is_featured', 'display_order')
        }),
        ('Métadonnées', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def rating_stars(self, obj):
        return '★' * obj.rating + '☆' * (5 - obj.rating)
    rating_stars.short_description = 'Note'
    
    def preview_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius:50%; object-fit:cover;" />', 
                obj.image.url
            )
        return format_html(
            '<div style="width:50px; height:50px; border-radius:50%; background:#ddd; display:flex; align-items:center; justify-content:center;">'
            '<i class="fas fa-user"></i>'
            '</div>'
        )
    preview_image.short_description = 'Photo'

@admin.register(Fact)
class FactAdmin(admin.ModelAdmin):
    list_display = ('title', 'value', 'suffix', 'get_icon_display', 'display_order')
    list_editable = ('display_order',)
    search_fields = ('title',)
    
@admin.register(TrainingCategory)
class TrainingCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'available_seats', 'price')
    prepopulated_fields = {'slug': ('title',)}
# @admin.register(Training)
# class TrainingAdmin(admin.ModelAdmin):
#     list_display = ('title', 'category', 'price', 'start_date', 'is_active', 'current_participants')
#     list_filter = ('category', 'is_active', 'start_date')
#     search_fields = ('title', 'short_description')
#     prepopulated_fields = {'slug': ('title',)}

# @admin.register(TrainingRegistration)
# class TrainingRegistrationAdmin(admin.ModelAdmin):
#     list_display = ('user', 'training', 'registration_date', 'status')
#     list_filter = ('status', 'registration_date', 'training')
#     search_fields = ('user__username', 'training__title')    
@admin.register(TrainingRegistration)
class TrainingRegistrationAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_user_full_name', 'user_email', 'user_phone', 'training', 'registration_date', 'status')
    list_filter = ('status', 'registration_date', 'training')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'user_email', 'training__title')
    readonly_fields = ('registration_date', 'user_first_name', 'user_last_name', 'user_email', 'user_phone')
    list_per_page = 20
    
    fieldsets = (
        ('Informations utilisateur', {
            'fields': ('user', 'user_first_name', 'user_last_name', 'user_email', 'user_phone')
        }),
        ('Informations formation', {
            'fields': ('training', 'registration_date', 'status', 'notes')
        }),
    )
    
    def get_user_full_name(self, obj):
        return f"{obj.user_first_name} {obj.user_last_name}"
    get_user_full_name.short_description = 'Nom complet'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'training') 
    def registration_details(self, request, object_id):
        registration = get_object_or_404(TrainingRegistration, id=object_id)
        context = {
            'title': f'Détails de l\'inscription - {registration}',
            'registration': registration,
            'opts': self.model._meta,
        }
        return render(request, 'admin/training_registration_details.html', context)
    
from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_username', 'get_email', 'phone', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'phone', 'user__email')
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 20
    
    # Ajoutez ces méthodes pour afficher les infos de l'utilisateur
    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Nom utilisateur'
    get_username.admin_order_field = 'user__username'
    
    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'
    get_email.admin_order_field = 'user__email'
    
    def get_first_name(self, obj):
        return obj.user.first_name
    get_first_name.short_description = 'Prénom'
    
    def get_last_name(self, obj):
        return obj.user.last_name
    get_last_name.short_description = 'Nom'
    
    fieldsets = (
        ('Liaison utilisateur', {
            'fields': ('user',)
        }),
        ('Informations de contact', {
            'fields': ('phone',)
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
# admin.py
# @admin.register(ProjectCategory)
# class ProjectCategoryAdmin(admin.ModelAdmin):
#     list_display = ('name', 'slug', 'display_order', 'is_active', 'project_count')
#     list_editable = ('display_order', 'is_active')
#     prepopulated_fields = {'slug': ('name',)}
    
#     def project_count(self, obj):
#         return obj.project_set.count()
#     project_count.short_description = 'Nombre de projets'