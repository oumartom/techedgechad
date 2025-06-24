from django.contrib import admin
from django.utils.html import format_html
from .models import Service, TeamMember, Project, Testimonial, Fact

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

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'profession', 'company', 'rating', 'is_featured', 'preview_image')
    list_editable = ('is_featured', 'rating')
    list_filter = ('rating', 'is_featured')
    search_fields = ('client_name', 'company', 'profession')
    
    def preview_image(self, obj):
        return format_html('<img src="{}" width="50" style="border-radius:50%;" />', obj.image.url) if obj.image else '-'
    preview_image.short_description = 'Photo'

@admin.register(Fact)
class FactAdmin(admin.ModelAdmin):
    list_display = ('title', 'value', 'suffix', 'get_icon_display', 'display_order')
    list_editable = ('display_order',)
    search_fields = ('title',)