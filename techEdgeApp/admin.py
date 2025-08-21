from django.contrib import admin
from django.utils.html import format_html
from .models import Service, TeamMember, Project, Testimonial, Fact
from .models import Subscriber
from .models import Subscriber
admin.site.register(Subscriber)
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
    
# admin.py
# @admin.register(ProjectCategory)
# class ProjectCategoryAdmin(admin.ModelAdmin):
#     list_display = ('name', 'slug', 'display_order', 'is_active', 'project_count')
#     list_editable = ('display_order', 'is_active')
#     prepopulated_fields = {'slug': ('name',)}
    
#     def project_count(self, obj):
#         return obj.project_set.count()
#     project_count.short_description = 'Nombre de projets'